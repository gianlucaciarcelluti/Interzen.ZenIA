"""
Client MCP diretto che bypassa il protocollo stdio e usa direttamente i tools del server.
Questa è una soluzione alternativa al problema della comunicazione JSON-RPC.
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.config import config
from core.models import *
from core.logging_utils import log_truncated

logger = logging.getLogger(__name__)


def make_json_serializable(obj: Any) -> Any:
    """Converte oggetti non JSON-serializzabili in formati JSON-compatibili"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif hasattr(obj, 'dict'):  # Oggetti Pydantic
        return make_json_serializable(obj.dict())
    else:
        return obj


class MCPConnectionError(Exception):
    """Errore di connessione al server MCP"""
    pass


class MCPToolError(Exception):
    """Errore nell'esecuzione di un tool MCP"""
    pass


class DirectMCPClient:
    """Client MCP diretto che bypassa stdio e usa direttamente i tools"""
    
    def __init__(self):
        self.connected = False
        self.tools = None
    
    async def connect(self) -> None:
        """Connette direttamente ai tools del server MCP"""
        try:
            logger.info("📡 MCP CLIENT - Tentativo di connessione diretta al server MCP...")
            
            # Import diretto dei tools
            from mcp_server.server import DeterminaTools, OllamaClient
            
            # Crea il client Ollama e i tools
            logger.info(f"🔧 MCP CLIENT - Creazione client Ollama: {config.OLLAMA_BASE_URL}, modello: {config.OLLAMA_MODEL}")
            ollama_client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
            self.tools = DeterminaTools(ollama_client)
            
            # Test connessione Ollama
            logger.info("🔍 MCP CLIENT - Test connessione Ollama...")
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{config.OLLAMA_BASE_URL}/api/tags")
                if response.status_code != 200:
                    raise MCPConnectionError(f"Ollama non raggiungibile: status {response.status_code}")
            
            self.connected = True
            logger.info("✅ MCP CLIENT - Connesso al server MCP in modalità diretta")
            
        except Exception as e:
            logger.error(f"❌ MCP CLIENT - Errore nella connessione diretta MCP: {str(e)}")
            raise MCPConnectionError(f"Impossibile connettersi ai tools MCP: {str(e)}")
    
    async def disconnect(self) -> None:
        """Disconnette dal server MCP"""
        logger.info("🔌 MCP CLIENT - Disconnessione dal server MCP diretto")
        self.connected = False
        self.tools = None
        logger.info("✅ MCP CLIENT - Disconnesso dal server MCP diretto")
    
    async def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Invoca un tool specifico direttamente"""
        if not self.connected or self.tools is None:
            raise MCPConnectionError("Non connesso al server MCP")
        
        logger.info(f"🔧 MCP CLIENT - Invocazione tool: {tool_name}")
        # Log dei parametri in modo sicuro e troncato
        log_truncated(logger, logging.DEBUG, "📝 MCP CLIENT - Parametri", parameters, max_chars=800)
        
        try:
            # Assicurati che tutti i parametri siano JSON-serializzabili
            clean_parameters = make_json_serializable(parameters)
            log_truncated(logger, logging.DEBUG, "🧹 MCP CLIENT - Parametri puliti", clean_parameters, max_chars=800)
            
            # Mappa i tool names alle funzioni
            if tool_name == "fascicolo-analyzer":
                logger.info("🔍 MCP CLIENT - Chiamata fascicolo-analyzer")
                result = await self.tools.fascicolo_analyzer(
                    clean_parameters["fascicolo_content"],
                    clean_parameters["document_types"]
                )
            elif tool_name == "legal-framework-validator":
                logger.info("⚖️ MCP CLIENT - Chiamata legal-framework-validator")
                result = await self.tools.legal_framework_validator(
                    clean_parameters["procedimento_type"],
                    clean_parameters["ente_competente"],
                    clean_parameters["normativa_riferimento"]
                )
            elif tool_name == "content-generator":
                logger.info("📝 MCP CLIENT - Chiamata content-generator")
                result = await self.tools.content_generator(
                    clean_parameters["section_type"],
                    clean_parameters["context_data"],
                    clean_parameters.get("template_style", "formale")
                )
            elif tool_name == "document-composer":
                logger.info("📄 MCP CLIENT - Chiamata document-composer")
                result = await self.tools.document_composer(
                    clean_parameters["sections"],
                    clean_parameters["template_id"],
                    clean_parameters["ente_metadata"]
                )
            elif tool_name == "compliance-checker":
                logger.info("✅ MCP CLIENT - Chiamata compliance-checker")
                result = await self.tools.compliance_checker(
                    clean_parameters["determina_content"],
                    clean_parameters.get("check_level", "basic")
                )
            else:
                logger.warning(f"⚠️ MCP CLIENT - Tool sconosciuto: {tool_name}")
                raise MCPToolError(f"Tool sconosciuto: {tool_name}")
            
            logger.info(f"✅ MCP CLIENT - Tool {tool_name} completato con successo")
            log_truncated(logger, logging.DEBUG, "📦 MCP CLIENT - Risultato", result, max_chars=1200)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ MCP CLIENT - Errore nell'invocazione diretta del tool {tool_name}: {str(e)}")
            raise MCPToolError(f"Errore nell'invocazione del tool {tool_name}: {str(e)}")
    
    async def list_available_tools(self) -> List[str]:
        """Ottiene la lista dei tools disponibili"""
        if not self.connected:
            raise MCPConnectionError("Non connesso al server MCP")
        
        # Lista hardcoded dei tools disponibili
        return [
            "fascicolo-analyzer",
            "legal-framework-validator", 
            "content-generator",
            "document-composer",
            "compliance-checker"
        ]


class DeterminaGenerationService:
    """Servizio per la generazione di determine usando MCP diretto"""
    
    def __init__(self, mcp_client: DirectMCPClient):
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
            logger.info(f"🚀 DETERMINA GENERATION - Inizio generazione determina per fascicolo {fascicolo_data.id}")
            logger.info(f"📊 DETERMINA GENERATION - Template: {template_id}, Ente: {ente_metadata.get('nome', 'N/A')}")
            
            # 1. Analizza il fascicolo
            logger.info("🔍 DETERMINA GENERATION - FASE 1: Analisi fascicolo")
            fascicolo_content = "\n".join([doc.contenuto_estratto or "" for doc in fascicolo_data.documenti])
            document_types = [doc.tipo.value for doc in fascicolo_data.documenti]
            logger.debug(f"📝 DETERMINA GENERATION - Contenuto fascicolo: {len(fascicolo_content)} caratteri")
            logger.debug(f"📝 DETERMINA GENERATION - Tipi documento: {document_types}")
            
            analysis_result = await self.analyze_fascicolo(fascicolo_content, document_types)
            
            if not analysis_result.get("success"):
                logger.error(f"❌ DETERMINA GENERATION - Errore nell'analisi fascicolo: {analysis_result.get('error')}")
                return DeterminaGenerationResponse(
                    determina_id=f"det_{fascicolo_data.id}",
                    status=GenerationStatus.ERROR,
                    error_message=f"Errore nell'analisi fascicolo: {analysis_result.get('error')}"
                )
            
            analysis = analysis_result["analysis"]
            logger.info("✅ DETERMINA GENERATION - Analisi fascicolo completata")
            
            # 2. Valida il framework legale
            logger.info("⚖️ DETERMINA GENERATION - FASE 2: Validazione framework legale")
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
            # Prepara context_data con conversione per JSON serialization
            context_data = make_json_serializable({
                "fascicolo": fascicolo_data.dict(),
                "analysis": analysis,
                "validation": validation,
                "ente": ente_metadata
            })
            
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


# Utility per creare e gestire il client diretto
async def create_direct_mcp_client() -> DirectMCPClient:
    """Crea e connette un client MCP diretto"""
    client = DirectMCPClient()
    await client.connect()
    return client


async def create_direct_generation_service() -> DeterminaGenerationService:
    """Crea un servizio di generazione con client MCP diretto"""
    client = await create_direct_mcp_client()
    return DeterminaGenerationService(client)


# Compatibilità con il vecchio client - fallback automatico
async def create_mcp_client(server_script_path: str) -> DirectMCPClient:
    """Crea un client MCP con fallback alla modalità diretta"""
    logger.info("Usando client MCP diretto (bypass stdio)")
    return await create_direct_mcp_client()


async def create_generation_service(server_script_path: str) -> DeterminaGenerationService:
    """Crea un servizio di generazione con fallback alla modalità diretta"""
    logger.info("Usando servizio generazione MCP diretto (bypass stdio)")
    return await create_direct_generation_service()