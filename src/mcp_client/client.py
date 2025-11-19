"""
MCP Client per comunicare con il server MCP delle determine.
Fornisce un'interfaccia Python per invocare i tools del server.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .direct_client import DirectMCPClient
import subprocess
import tempfile
import os
import time
from datetime import datetime

from core.config import config
from core.models import (
    FascicoloData, DeterminaGenerationResponse, GenerationStatus,
    DeterminaContent, ValidationResult, GenerationMetadata
)
from core.logging_utils import log_truncated

logger = logging.getLogger(__name__)


class MCPConnectionError(Exception):
    """Errore di connessione al server MCP"""
    pass


class MCPToolError(Exception):
    """Errore nell'esecuzione di un tool MCP"""
    pass


class MCPClient:
    """Client per comunicare con il server MCP"""
    
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.process: Optional[asyncio.subprocess.Process] = None
        self.connected = False
    
    async def connect(self) -> None:
        """Connette al server MCP"""
        try:
            # Ottieni il percorso del Python interpreter del virtual environment
            import sys
            python_path = sys.executable
            
            # Aggiungi il percorso del progetto al PYTHONPATH
            src_dir = os.path.dirname(self.server_script_path)
            env = os.environ.copy()
            if 'PYTHONPATH' in env:
                env['PYTHONPATH'] = f"{src_dir}{os.pathsep}{env['PYTHONPATH']}"
            else:
                env['PYTHONPATH'] = src_dir
            
            logger.info(f"Avvio del server MCP: {self.server_script_path}")
            
            # Avvia il processo del server MCP
            self.process = await asyncio.create_subprocess_exec(
                python_path, self.server_script_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            logger.info(f"Processo server MCP avviato con PID: {self.process.pid}")
            
            # Aspetta che il server sia pronto (attende che stampi il messaggio di avvio)
            await self._wait_for_server_ready()
            
            self.connected = True
            logger.info(f"Connesso al server MCP usando Python: {python_path}")
            logger.info(f"PYTHONPATH: {env.get('PYTHONPATH', 'Non impostato')}")
            
        except Exception as e:
            logger.error(f"Errore nella connessione al server MCP: {str(e)}")
            if self.process:
                self.process.terminate()
                await self.process.wait()
            raise MCPConnectionError(f"Impossibile connettersi al server MCP: {str(e)}")
    
    def _check_process_status(self) -> None:
        """Controlla se il processo MCP è ancora in esecuzione"""
        if self.process is None:
            raise MCPConnectionError("Processo server MCP non disponibile")
        if self.process.returncode is not None:
            raise MCPConnectionError(f"Il server MCP è terminato con codice: {self.process.returncode}")
    
    async def _check_stderr_for_errors(self) -> None:
        """Controlla stderr per errori critici"""
        if not self.process or not self.process.stderr:
            return
            
        try:
            line = await asyncio.wait_for(self.process.stderr.readline(), timeout=0.1)
            if line:
                log_line = line.decode().strip()
                logger.debug(f"Server MCP stderr: {log_line}")
                # Se c'è un errore critico, fermati
                if "error" in log_line.lower() or "failed" in log_line.lower():
                    raise MCPConnectionError(f"Errore server MCP: {log_line}")
        except asyncio.TimeoutError:
            pass  # Timeout normale, continua
    
    async def _wait_for_server_ready(self, timeout: float = 10.0) -> None:
        """Aspetta che il server MCP sia pronto a ricevere connessioni"""
        logger.info("In attesa che il server MCP sia pronto...")
        start_time = asyncio.get_event_loop().time()
        
        try:
            while True:
                # Controlla se il processo è ancora in esecuzione
                self._check_process_status()
                
                # Controlla il timeout
                elapsed_time = asyncio.get_event_loop().time() - start_time
                if elapsed_time > timeout:
                    logger.warning("Timeout nell'attesa del server MCP, ma il processo è attivo. Procedo...")
                    return
                
                # Leggi stderr per errori
                await self._check_stderr_for_errors()
                
                # Piccola pausa e verifica che il processo sia stabile
                await asyncio.sleep(0.5)
                
                # Se il processo è stabile per almeno 1 secondo, considera pronto
                if elapsed_time > 1.0:
                    logger.info("Server MCP sembra essere pronto (processo stabile)")
                    return
                
        except Exception as e:
            logger.error(f"Errore nell'attesa del server MCP: {str(e)}")
            raise MCPConnectionError(f"Errore nell'attesa del server: {str(e)}")
    
    async def disconnect(self) -> None:
        """Disconnette dal server MCP"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.connected = False
            logger.info("Disconnesso dal server MCP")
    
    async def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Invoca un tool specifico sul server MCP"""
        if not self.connected or self.process is None:
            raise MCPConnectionError("Non connesso al server MCP")
        
        try:
            # Prepara il messaggio per il server
            message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": parameters
                }
            }
            # Log del messaggio inviato (troncato)
            log_truncated(logger, logging.DEBUG, "MCPClient - Outgoing message", message, max_chars=1000)
            
            # Verifica che stdin sia disponibile
            if self.process.stdin is None:
                raise MCPConnectionError("Stdin del processo MCP non disponibile")
            
            # Invia il messaggio
            message_json = json.dumps(message) + '\n'
            self.process.stdin.write(message_json.encode())
            await self.process.stdin.drain()
            
            # Verifica che stdout sia disponibile
            if self.process.stdout is None:
                raise MCPConnectionError("Stdout del processo MCP non disponibile")
            
            # Leggi la risposta
            response_line = await self.process.stdout.readline()
            if not response_line:
                raise MCPConnectionError("Nessuna risposta dal server MCP")
            
            response = json.loads(response_line.decode())
            # Log della risposta grezza (troncata)
            log_truncated(logger, logging.DEBUG, "MCPClient - Incoming response", response, max_chars=1000)
            
            if "error" in response:
                raise MCPToolError(f"Errore tool {tool_name}: {response['error']}")
            
            # Estrai il risultato dal formato MCP
            result_content = response.get("result", {})
            if isinstance(result_content, list) and len(result_content) > 0:
                text_content = result_content[0].get("text", "{}")
                try:
                    return json.loads(text_content)
                except json.JSONDecodeError:
                    return {"success": False, "error": "Formato risposta non valido", "raw": text_content}
            
            # Se result_content non è un dict, lo convertiamo
            if isinstance(result_content, dict):
                return result_content
            else:
                return {"success": False, "error": "Formato risposta non supportato", "data": result_content}
            
        except Exception as e:
            logger.error(f"Errore nell'invocazione del tool {tool_name}: {str(e)}")
            raise MCPToolError(f"Errore nell'invocazione del tool {tool_name}: {str(e)}")
    
    async def list_available_tools(self) -> List[str]:
        """Ottiene la lista dei tools disponibili"""
        if not self.connected or self.process is None:
            raise MCPConnectionError("Non connesso al server MCP")
        
        try:
            message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            # Verifica che stdin e stdout siano disponibili
            if self.process.stdin is None or self.process.stdout is None:
                raise MCPConnectionError("Stream del processo MCP non disponibili")
            
            message_json = json.dumps(message) + '\n'
            self.process.stdin.write(message_json.encode())
            await self.process.stdin.drain()
            
            # Timeout più lungo per la risposta
            response_line = await asyncio.wait_for(
                self.process.stdout.readline(), 
                timeout=8.0  # Timeout aumentato
            )
            
            if not response_line:
                raise MCPConnectionError("Nessuna risposta dal server MCP")
            
            response = json.loads(response_line.decode())
            
            if "error" in response:
                raise MCPToolError(f"Errore nel listing tools: {response['error']}")
            
            tools = response.get("result", {}).get("tools", [])
            return [tool["name"] for tool in tools if isinstance(tool, dict) and "name" in tool]
            
        except asyncio.TimeoutError:
            logger.error("Timeout nella comunicazione con il server MCP")
            raise MCPToolError("Timeout nella risposta del server MCP")
        except json.JSONDecodeError as e:
            logger.error(f"Errore nel parsing JSON della risposta MCP: {str(e)}")
            raise MCPToolError(f"Risposta MCP non valida: {str(e)}")
        except Exception as e:
            logger.error(f"Errore nel listing tools: {str(e)}")
            raise MCPToolError(f"Errore nel listing tools: {str(e)}")


class DeterminaGenerationService:
    """Servizio per la generazione di determine usando MCP"""
    
    def __init__(self, mcp_client: Any):
        self.mcp_client = mcp_client
    
    async def analyze_fascicolo(self, fascicolo_content: str, document_types: List[str]) -> Dict[str, Any]:
        """Analizza il fascicolo usando il tool MCP"""
        return await self.mcp_client.invoke_tool(
            "fascicolo-analyzer",
            {
                "fascicolo_content": fascicolo_content,
                "document_types": document_types
            }
        )
    
    async def validate_legal_framework(self, procedimento_type: str, ente_competente: str, 
                                     normativa_riferimento: List[str]) -> Dict[str, Any]:
        """Valida il framework legale usando il tool MCP"""
        return await self.mcp_client.invoke_tool(
            "legal-framework-validator",
            {
                "procedimento_type": procedimento_type,
                "ente_competente": ente_competente,
                "normativa_riferimento": normativa_riferimento
            }
        )
    
    async def generate_section_content(self, section_type: str, context_data: Dict[str, Any],
                                     template_style: str = "formale") -> Dict[str, Any]:
        """Genera il contenuto di una sezione usando il tool MCP"""
        return await self.mcp_client.invoke_tool(
            "content-generator",
            {
                "section_type": section_type,
                "context_data": context_data,
                "template_style": template_style
            }
        )
    
    async def compose_document(self, sections: Dict[str, Any], template_id: str,
                              ente_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compone il documento finale usando il tool MCP"""
        return await self.mcp_client.invoke_tool(
            "document-composer",
            {
                "sections": sections,
                "template_id": template_id,
                "ente_metadata": ente_metadata
            }
        )
    
    async def check_compliance(self, determina_content: str, check_level: str = "basic") -> Dict[str, Any]:
        """Verifica la conformità del documento usando il tool MCP"""
        return await self.mcp_client.invoke_tool(
            "compliance-checker",
            {
                "determina_content": determina_content,
                "check_level": check_level
            }
        )
    
    async def generate_complete_determina(self, fascicolo_data: FascicoloData,
                                        ente_metadata: Dict[str, Any],
                                        template_id: str = "standard") -> DeterminaGenerationResponse:
        """
        Genera una determina completa seguendo tutto il workflow
        """
        start_time = time.time()
        tokens_used = 0  # Contatore per i token (approssimativo)
        
        try:
            logger.info(f"Inizio generazione determina per fascicolo {fascicolo_data.id}")
            
            # 1. Analizza il fascicolo
            fascicolo_content = "\n".join([doc.contenuto_estratto or "" for doc in fascicolo_data.documenti])
            document_types = [doc.tipo.value for doc in fascicolo_data.documenti]
            
            analysis_result = await self.analyze_fascicolo(fascicolo_content, document_types)
            
            if not analysis_result.get("success"):
                return DeterminaGenerationResponse(
                    determina_id=f"det_{fascicolo_data.id}",
                    status=GenerationStatus.ERROR,
                    error_message=f"Errore nell'analisi fascicolo: {analysis_result.get('error')}"
                )
            
            analysis = analysis_result["analysis"]
            logger.info("Analisi fascicolo completata")
            
            # 2. Valida il framework legale
            normativa_ref = analysis.get("riferimenti_normativi", [])
            if not normativa_ref:
                normativa_ref = ["L. 241/1990"]  # Default
            
            validation_result = await self.validate_legal_framework(
                analysis.get("procedimento_type", fascicolo_data.procedimento_type.value),
                ente_metadata.get("nome", "Ente Pubblico"),
                normativa_ref
            )
            
            if not validation_result.get("success"):
                return DeterminaGenerationResponse(
                    determina_id=f"det_{fascicolo_data.id}",
                    status=GenerationStatus.ERROR,
                    error_message=f"Errore nella validazione legale: {validation_result.get('error')}"
                )
            
            validation = validation_result["validation"]
            logger.info("Validazione legale completata")
            
            # 3. Genera contenuto per ogni sezione
            context_data = {
                "fascicolo": fascicolo_data.dict(),
                "analysis": analysis,
                "validation": validation,
                "ente": ente_metadata
            }
            
            sections = {}
            for section_type in ["premesse", "motivazione", "dispositivo"]:
                section_result = await self.generate_section_content(
                    section_type, context_data, "formale"
                )
                
                if section_result.get("success"):
                    sections[section_type] = section_result["content"]
                else:
                    logger.warning(f"Errore nella generazione sezione {section_type}: {section_result.get('error')}")
                    sections[section_type] = {"contenuto": f"[Errore nella generazione {section_type}]"}
            
            logger.info("Generazione contenuto sezioni completata")
            
            # 4. Componi il documento finale
            compose_result = await self.compose_document(sections, template_id, ente_metadata)
            
            if not compose_result.get("success"):
                return DeterminaGenerationResponse(
                    determina_id=f"det_{fascicolo_data.id}",
                    status=GenerationStatus.PARTIAL,
                    error_message=f"Errore nella composizione: {compose_result.get('error')}"
                )
            
            document = compose_result["document"]
            logger.info("Composizione documento completata")
            
            # 5. Controllo conformità
            document_text = json.dumps(document, indent=2, ensure_ascii=False)
            compliance_result = await self.check_compliance(document_text, "full")
            
            validation_results = []
            if compliance_result.get("success"):
                compliance_report = compliance_result["compliance_report"]
                
                for controllo in compliance_report.get("controlli_effettuati", []):
                    # Mappa i valori AI ai valori validi per severity
                    esito = controllo.get("esito", "info")
                    if esito in ["ok", "conforme", "valido", "corretto"]:
                        severity = "info"
                        passed = True
                    elif esito in ["warning", "attenzione", "parziale"]:
                        severity = "warning" 
                        passed = False
                    elif esito in ["error", "errore", "non_conforme", "invalido"]:
                        severity = "error"
                        passed = False
                    else:
                        severity = "info"
                        passed = True
                    
                    validation_results.append(ValidationResult(
                        section=controllo.get("categoria", "generale"),
                        issue=controllo.get("descrizione"),
                        severity=severity,
                        suggestion=controllo.get("suggerimento"),
                        passed=passed
                    ))
            
            # 6. Costruisci la risposta finale
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Approssimiamo i token basandoci sulla lunghezza del testo
            fascicolo_content = "\n".join([doc.contenuto_estratto or "" for doc in fascicolo_data.documenti])
            tokens_used = len(fascicolo_content.split()) + len(str(document).split())  # Approssimazione
            
            # Coerce sections and allegati into expected types (strings / list of strings)
            from core.logging_utils import section_to_string, allegati_to_list

            premesse_str = section_to_string(document.get("premesse", ""))
            motivazione_str = section_to_string(document.get("motivazione", ""))
            dispositivo_str = section_to_string(document.get("dispositivo", ""))
            allegati_list = allegati_to_list(document.get("allegati", []))

            determina_content = DeterminaContent(
                premesse=premesse_str,
                motivazione=motivazione_str,
                dispositivo=dispositivo_str,
                allegati=allegati_list,
                riferimenti_normativi=document.get("riferimenti_normativi", [])
            )
            
            metadata = GenerationMetadata(
                generated_at=datetime.now(),
                ai_model=config.OLLAMA_MODEL,
                processing_time_seconds=round(processing_time, 2),
                tokens_used=tokens_used
            )
            
            response = DeterminaGenerationResponse(
                determina_id=f"det_{fascicolo_data.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                status=GenerationStatus.GENERATED,
                content=determina_content,
                validation_results=validation_results,
                metadata=metadata
            )
            
            logger.info(f"Generazione determina completata: {response.determina_id}")
            return response
            
        except Exception as e:
            logger.error(f"Errore nella generazione determina: {str(e)}")
            return DeterminaGenerationResponse(
                determina_id=f"det_{fascicolo_data.id}_error",
                status=GenerationStatus.ERROR,
                error_message=str(e)
            )


# Utility per creare e gestire il client
async def create_mcp_client(server_script_path: str) -> Any:
    """Crea e connette un client MCP con fallback automatico"""
    try:
        # Prova prima il client stdio normale
        client = MCPClient(server_script_path)
        await client.connect()
        
        # Test rapido per verificare che funzioni
        try:
            tools = await asyncio.wait_for(client.list_available_tools(), timeout=5.0)
            if tools:
                logger.info("Client MCP stdio funzionante")
                return client
        except (asyncio.TimeoutError, MCPConnectionError):
            logger.warning("Client MCP stdio non funziona, fallback a modalità diretta")
            await client.disconnect()
    except Exception:
        logger.warning("Client MCP stdio non disponibile")
    
    # Fallback al client diretto
    try:
        from .direct_client import create_direct_mcp_client
        logger.info("Usando client MCP diretto (bypass stdio)")
        return await create_direct_mcp_client()
    except Exception as e:
        logger.error(f"Impossibile creare client MCP: {str(e)}")
        raise MCPConnectionError(f"Nessun client MCP disponibile: {str(e)}")


async def create_generation_service(server_script_path: str) -> Any:
    """Crea un servizio di generazione con client MCP con fallback automatico"""
    try:
        # Prova prima il client stdio normale
        client = await create_mcp_client(server_script_path)
        return DeterminaGenerationService(client)
    except Exception:
        # Fallback al servizio diretto
        try:
            from .direct_client import create_direct_generation_service
            logger.info("Usando servizio generazione MCP diretto (bypass stdio)")
            return await create_direct_generation_service()
        except Exception:
            logger.error("Impossibile creare servizio generazione")
            raise MCPConnectionError("Nessun servizio MCP disponibile")
