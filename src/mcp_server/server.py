"""
MCP Server per la generazione di determine amministrative.
Implementa i tools definiti nelle specifiche tecniche.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

import httpx
from mcp import ServerSession, types
from mcp.server import Server, InitializationOptions
from mcp.server.stdio import stdio_server

from core.config import config
from core.models import *
from core.logging_utils import log_truncated

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client per comunicare con Ollama"""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        # Aumentiamo il timeout a 600 secondi (10 minuti)
        self.client = httpx.AsyncClient(timeout=600.0)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Genera una risposta usando il modello Ollama"""
        try:
            logger.info(f"🤖 OLLAMA REQUEST - Modello: {self.model}")
            logger.info(f"📊 OLLAMA REQUEST - Lunghezza prompt: {len(prompt)} caratteri")
            logger.info(f"📊 OLLAMA REQUEST - System prompt: {'Sì' if system_prompt else 'No'}")
            
            if system_prompt:
                logger.debug(f"📝 OLLAMA REQUEST - System prompt: {system_prompt[:200]}...")
            logger.debug(f"📝 OLLAMA REQUEST - User prompt: {prompt[:500]}...")
            
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": prompt
            })
            
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 4096
                }
            }
            
            logger.info(f"🚀 OLLAMA REQUEST - Invio richiesta a {self.base_url}/api/chat")
            # Log payload request body in debug (troncato)
            from core.logging_utils import log_truncated
            log_truncated(logger, logging.DEBUG, "OLLAMA - Request payload", payload, max_chars=2000)
            
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            
            logger.info(f"✅ OLLAMA RESPONSE - Status: {response.status_code}")
            response.raise_for_status()
            
            result = response.json()
            # Log response body (troncato)
            log_truncated(logger, logging.DEBUG, "OLLAMA - Response JSON", result, max_chars=2000)
            
            content = result.get("message", {}).get("content", "")
            
            if not content:
                logger.warning("⚠️ OLLAMA RESPONSE - Contenuto vuoto!")
                raise ValueError("Ollama ha restituito una risposta vuota")
            
            logger.info(f"✅ OLLAMA RESPONSE - Generazione completata: {len(content)} caratteri")
            logger.debug(f"📝 OLLAMA RESPONSE - Contenuto: {content[:500]}...")
            return content
        
        except httpx.TimeoutException:
            logger.error("Timeout nella richiesta a Ollama")
            raise Exception("Timeout nella generazione - il modello potrebbe essere sovraccarico")
        except httpx.HTTPStatusError as e:
            logger.error(f"Errore HTTP Ollama: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Errore HTTP {e.response.status_code}: {e.response.text}")
        except json.JSONDecodeError as e:
            logger.error(f"Errore parsing JSON risposta Ollama: {str(e)}")
            raise Exception("Risposta Ollama non valida (JSON malformato)")
        except Exception as e:
            logger.error(f"Errore nella generazione Ollama: {str(e)}")
            raise


class DeterminaTools:
    """Implementazione dei tools MCP per la generazione determine"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
    
    async def fascicolo_analyzer(self, fascicolo_content: str, document_types: List[str]) -> Dict[str, Any]:
        """Analizza fascicolo procedimentale e estrae informazioni strutturate"""
        
        # Limita la lunghezza del contenuto per evitare timeout
        max_content_length = 8000  # Circa 8K caratteri
        if len(fascicolo_content) > max_content_length:
            logger.warning(f"Fascicolo troppo lungo ({len(fascicolo_content)} chars), troncamento a {max_content_length}")
            fascicolo_content = fascicolo_content[:max_content_length] + "...[CONTENUTO TRONCATO]"
        
        system_prompt = """
        Sei un esperto di procedure amministrative italiane. 
        Analizza il fascicolo fornito ed estrai:
        1. Tipo di procedimento (autorizzazione, concessione, licenza, etc.)
        2. Dati del richiedente (nome, cognome, codice fiscale se presente)
        3. Oggetto della richiesta
        4. Documenti allegati identificati
        5. Date rilevanti
        6. Importi o valori economici
        7. Riferimenti normativi citati
        
        Rispondi SOLO in formato JSON valido.
        """
        
        prompt = f"""
        Analizza questo fascicolo procedimentale:
        
        CONTENUTO FASCICOLO:
        {fascicolo_content}
        
        TIPI DOCUMENTO PRESENTI:
        {', '.join(document_types)}
        
        Estrai le informazioni richieste in formato JSON con questa struttura:
        {{
            "procedimento_type": "tipo_procedimento",
            "richiedente": {{
                "nome": "nome",
                "cognome": "cognome", 
                "codice_fiscale": "codice_fiscale_se_presente"
            }},
            "oggetto_richiesta": "descrizione_oggetto",
            "documenti_identificati": ["lista", "documenti"],
            "date_rilevanti": ["date_trovate"],
            "importi": ["importi_trovati"],
            "riferimenti_normativi": ["leggi_e_regolamenti"],
            "urgenza": false,
            "note": "osservazioni_aggiuntive"
        }}
        """
        
        try:
            logger.info("Inizio analisi fascicolo...")
            logger.debug(f"Fascicolo content length: {len(fascicolo_content)} caratteri")
            
            response = await self.ollama.generate(prompt, system_prompt)
            
            logger.info("Risposta ricevuta da Ollama, parsing JSON...")
            
            # Pulisci la risposta per estrarre solo il JSON
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()
            
            if not response:
                raise ValueError("Risposta vuota dopo pulizia")
            
            logger.debug(f"JSON da parsare: {response[:200]}...")
            result = json.loads(response)
            
            logger.info("Analisi fascicolo completata con successo")
            return {
                "success": True,
                "analysis": result,
                "processing_time": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            error_msg = f"Errore parsing JSON nell'analisi fascicolo: {str(e)}"
            logger.error(error_msg)
            logger.error(f"JSON problematico: {response[:500] if 'response' in locals() else 'N/A'}")
            return {
                "success": False,
                "error": error_msg,
                "analysis": None
            }
        except Exception as e:
            error_msg = f"Errore nell'analisi fascicolo: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "analysis": None
            }
    
    async def legal_framework_validator(
                self, procedimento_type: str, ente_competente: str,                 
                normativa_riferimento: List[Dict[str, str]]
                ) -> Dict[str, Any]:
        """Valida conformità normativa e identifica framework legale applicabile"""
        
        system_prompt = """
        Sei un esperto legale di diritto amministrativo italiano.
        Valuta la conformità del procedimento amministrativo rispetto alla normativa vigente.
        Verifica competenze, procedure e requisiti normativi.
        """
        
        prompt = f"""
        Valuta questo procedimento amministrativo:
        
        TIPO PROCEDIMENTO: {procedimento_type}
        ENTE COMPETENTE: {ente_competente}
        NORMATIVA DI RIFERIMENTO: {', '.join(normativa_riferimento)}
        
        Fornisci una valutazione in formato JSON:
        {{
            "conformita_generale": "conforme|non_conforme|da_verificare",
            "competenza_ente": {{
                "valida": true/false,
                "motivazione": "spiegazione"
            }},
            "normativa_applicabile": ["leggi_pertinenti"],
            "requisiti_procedurali": ["requisiti_da_verificare"],
            "tempi_procedimento": "tempi_previsti",
            "documenti_richiesti": ["documenti_necessari"],
            "criticita": ["eventuali_problemi"],
            "raccomandazioni": ["suggerimenti"]
        }}
        """
        
        try:
            response = await self.ollama.generate(prompt, system_prompt)
            logger.info("Risposta ricevuta da Ollama, parsing JSON...")
            
            # Log della risposta grezza per debug
            logger.debug(f"Risposta grezza Ollama: {repr(response[:500])}")
            
            # Pulisci la risposta - gestisci meglio il parsing JSON
            response = response.strip()
            
            # Trova il primo blocco JSON valido
            json_start = -1
            json_end = -1
            
            # Cerca ```json
            if '```json' in response:
                json_start = response.find('```json') + 7
                # Cerca la fine del blocco
                json_end = response.find('```', json_start)
                if json_end != -1:
                    response = response[json_start:json_end].strip()
            elif response.startswith('{') and '}' in response:
                # Se inizia con { trova l'ultimo }
                json_end = response.rfind('}')
                if json_end != -1:
                    response = response[:json_end + 1].strip()
            else:
                # Prova a estrarre JSON da testo che inizia con spiegazione
                lines = response.split('\n')
                json_lines = []
                in_json = False
                brace_count = 0
                
                for line in lines:
                    if line.strip().startswith('{'):
                        in_json = True
                        brace_count = 0
                    
                    if in_json:
                        json_lines.append(line)
                        brace_count += line.count('{') - line.count('}')
                        
                        if brace_count <= 0 and line.strip().endswith('}'):
                            break
                
                if json_lines:
                    response = '\n'.join(json_lines).strip()
            
            # Controllo se la risposta è vuota dopo la pulizia
            if not response:
                logger.error("Risposta vuota dopo pulizia del formato")
                raise ValueError("Risposta vuota dal modello")
            
            logger.debug(f"Risposta pulita: {repr(response[:200])}")
            result = json.loads(response)
            
            return {
                "success": True,
                "validation": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Errore JSON parsing nella validazione legale: {str(e)}")
            logger.error(f"Contenuto che ha causato l'errore: {repr(response[:1000])}")
            return {
                "success": False,
                "error": f"Errore parsing JSON: {str(e)}",
                "validation": None,
                "raw_response": response[:500] if 'response' in locals() else "N/A"
            }
        except Exception as e:
            logger.error(f"Errore nella validazione legale: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "validation": None
            }
    
    async def content_generator(self, section_type: str, context_data: Dict[str, Any], 
                              template_style: str = "formale") -> Dict[str, Any]:
        """Genera contenuto specifico per sezioni della determina"""
        
        system_prompt = f"""
        Sei un esperto redattore di atti amministrativi italiani.
        Genera contenuto per la sezione '{section_type}' di una determina amministrativa.
        Usa uno stile {template_style} e linguaggio tecnico-giuridico appropriato.
        Rispetta le forme e le convenzioni degli atti amministrativi italiani.
        """
        
        # Template specifici per sezione
        section_templates = {
            "premesse": """
            Genera le PREMESSE della determina includendo:
            - Richiamo alle competenze dell'ente
            - Riferimenti normativi pertinenti
            - Richiamo all'istanza di parte
            - Iter procedimentale seguito
            """,
            "motivazione": """
            Genera la MOTIVAZIONE della determina includendo:
            - Analisi della richiesta
            - Valutazione tecnico-giuridica
            - Verifica dei requisiti
            - Considerazioni sugli allegati
            """,
            "dispositivo": """
            Genera il DISPOSITIVO della determina con:
            - Decisione finale chiara
            - Eventuali prescrizioni
            - Termini e condizioni
            - Clausole standard di efficacia
            """
        }
        
        template = section_templates.get(section_type, "Genera contenuto appropriato per questa sezione.")
        
        prompt = f"""
        {template}
        
        DATI DI CONTESTO:
        {json.dumps(context_data, indent=2, ensure_ascii=False)}
        
        Genera il contenuto richiesto in formato JSON:
        {{
            "contenuto": "testo_della_sezione",
            "riferimenti_normativi": ["normative_citate"],
            "note_redazionali": "eventuali_note"
        }}
        """
        
        try:
            # Log descrittivo: quale sezione stiamo richiedendo e un breve contesto
            try:
                fascicolo_id = context_data.get('fascicolo', {}).get('id') if isinstance(context_data.get('fascicolo'), dict) else None
                num_docs = len(context_data.get('fascicolo', {}).get('documenti', [])) if isinstance(context_data.get('fascicolo'), dict) else None
            except Exception:
                fascicolo_id = None
                num_docs = None

            logger.info(f"OLLAMA - Generazione sezione '{section_type}' | fascicolo_id={fascicolo_id} | docs={num_docs}")
            response = await self.ollama.generate(prompt, system_prompt)
            logger.info("Risposta ricevuta da Ollama per content_generator, parsing JSON...")
            
            # Log della risposta grezza per debug
            logger.debug(f"Risposta grezza content_generator: {repr(response[:500])}")
            
            # Pulisci la risposta - gestisci meglio il parsing JSON
            response = response.strip()
            
            # Trova il primo blocco JSON valido
            json_start = -1
            json_end = -1
            
            # Cerca ```json
            if '```json' in response:
                json_start = response.find('```json') + 7
                # Cerca la fine del blocco
                json_end = response.find('```', json_start)
                if json_end != -1:
                    response = response[json_start:json_end].strip()
            elif response.startswith('{') and '}' in response:
                # Se inizia con { trova l'ultimo }
                json_end = response.rfind('}')
                if json_end != -1:
                    response = response[:json_end + 1].strip()
            else:
                # Prova a estrarre JSON da testo che inizia con spiegazione
                lines = response.split('\n')
                json_lines = []
                in_json = False
                brace_count = 0
                
                for line in lines:
                    if line.strip().startswith('{'):
                        in_json = True
                        brace_count = 0
                    
                    if in_json:
                        json_lines.append(line)
                        brace_count += line.count('{') - line.count('}')
                        
                        if brace_count <= 0 and line.strip().endswith('}'):
                            break
                
                if json_lines:
                    response = '\n'.join(json_lines).strip()
            
            # Controllo se la risposta è vuota dopo la pulizia
            if not response:
                logger.error("Risposta vuota dopo pulizia del formato in content_generator")
                raise ValueError("Risposta vuota dal modello")
            
            logger.debug(f"Risposta pulita content_generator: {repr(response[:200])}")
            result = json.loads(response)

            # Aggiungiamo un dettaglio di cosa è stato richiesto per tracciare le chiamate di generazione
            return {
                "success": True,
                "section_type": section_type,
                "content": result,
                "generation_detail": {
                    "requested_section": section_type,
                    "fascicolo_id": fascicolo_id,
                    "num_documents": num_docs
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Errore JSON parsing in content_generator: {str(e)}")
            logger.error(f"Contenuto che ha causato l'errore: {repr(response[:1000])}")
            return {
                "success": False,
                "error": f"Errore parsing JSON: {str(e)}",
                "content": None,
                "raw_response": response[:500] if 'response' in locals() else "N/A"
            }
        except Exception as e:
            logger.error(f"Errore nella generazione contenuto: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    async def document_composer(self, sections: Dict[str, Any], template_id: str, 
                              ente_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Compone documento finale della determina"""
        
        system_prompt = """
        Sei un esperto compositore di atti amministrativi italiani.
        Assembla le sezioni fornite in un documento di determina coerente e completo.
        Assicurati che il linguaggio sia uniforme e che la struttura rispetti le convenzioni.
        """
        
        prompt = f"""
        Componi una determina amministrativa completa assemblando queste sezioni:
        
        SEZIONI DISPONIBILI:
        {json.dumps(sections, indent=2, ensure_ascii=False)}
        
        METADATI ENTE:
        {json.dumps(ente_metadata, indent=2, ensure_ascii=False)}
        
        TEMPLATE ID: {template_id}
        
        Genera il documento finale in formato JSON:
        {{
            "intestazione": {{
                "ente": "nome_ente",
                "settore": "settore_competente",
                "numero_determina": "da_assegnare",
                "data": "data_odierna"
            }},
            "oggetto": "oggetto_determina",
            "premesse": "testo_premesse_complete",
            "motivazione": "testo_motivazione_completa", 
            "dispositivo": "testo_dispositivo_completo",
            "allegati": ["elenco_allegati"],
            "riferimenti_normativi": ["tutte_le_norme_citate"],
            "clausole_finali": "clausole_standard",
            "firma": {{
                "ruolo": "ruolo_firmatario",
                "nome": "da_completare"
            }}
        }}
        """
        
        try:
            response = await self.ollama.generate(prompt, system_prompt)
            logger.info("Risposta ricevuta da Ollama per document_composer, parsing JSON...")
            
            # Log della risposta grezza per debug
            logger.debug(f"Risposta grezza document_composer: {repr(response[:500])}")
            
            # Pulisci la risposta - gestisci meglio il parsing JSON
            response = response.strip()
            
            # Trova il primo blocco JSON valido
            json_start = -1
            json_end = -1
            
            # Cerca ```json
            if '```json' in response:
                json_start = response.find('```json') + 7
                # Cerca la fine del blocco
                json_end = response.find('```', json_start)
                if json_end != -1:
                    response = response[json_start:json_end].strip()
            elif response.startswith('{') and '}' in response:
                # Se inizia con { trova l'ultimo }
                json_end = response.rfind('}')
                if json_end != -1:
                    response = response[:json_end + 1].strip()
            else:
                # Prova a estrarre JSON da testo che inizia con spiegazione
                lines = response.split('\n')
                json_lines = []
                in_json = False
                brace_count = 0
                
                for line in lines:
                    if line.strip().startswith('{'):
                        in_json = True
                        brace_count = 0
                    
                    if in_json:
                        json_lines.append(line)
                        brace_count += line.count('{') - line.count('}')
                        
                        if brace_count <= 0 and line.strip().endswith('}'):
                            break
                
                if json_lines:
                    response = '\n'.join(json_lines).strip()
            
            # Controllo se la risposta è vuota dopo la pulizia
            if not response:
                logger.error("Risposta vuota dopo pulizia del formato in document_composer")
                raise ValueError("Risposta vuota dal modello")
            
            logger.debug(f"Risposta pulita document_composer: {repr(response[:200])}")
            result = json.loads(response)
            
            return {
                "success": True,
                "document": result,
                "composed_at": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Errore JSON parsing in document_composer: {str(e)}")
            logger.error(f"Contenuto che ha causato l'errore: {repr(response[:1000])}")
            return {
                "success": False,
                "error": f"Errore parsing JSON: {str(e)}",
                "document": None,
                "raw_response": response[:500] if 'response' in locals() else "N/A"
            }
        except Exception as e:
            logger.error(f"Errore nella composizione documento: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "document": None
            }
    
    async def compliance_checker(self, determina_content: str, 
                               check_level: str = "basic") -> Dict[str, Any]:
        """Verifica conformità legale e qualità del documento"""
        
        system_prompt = """
        Sei un esperto revisore di atti amministrativi italiani.
        Verifica la conformità legale, la coerenza interna e la qualità linguistica della determina.
        Identifica eventuali errori, omissioni o miglioramenti necessari.
        """
        
        check_levels = {
            "basic": "Controllo base di struttura e completezza",
            "full": "Controllo completo di conformità normativa e qualità",
            "expert": "Controllo esperto con analisi approfondita e suggerimenti"
        }
        
        prompt = f"""
        Esegui un controllo di livello '{check_level}' su questa determina:
        {check_levels.get(check_level, "Controllo standard")}
        
        CONTENUTO DETERMINA:
        {determina_content}
        
        Fornisci il risultato della verifica in formato JSON:
        {{
            "conformita_generale": "conforme|parziale|non_conforme",
            "punteggio_qualita": "voto_da_1_a_10",
            "controlli_effettuati": [
                {{
                    "categoria": "struttura|normativa|linguaggio|completezza",
                    "esito": "ok|warning|errore",
                    "descrizione": "dettaglio_controllo",
                    "suggerimento": "eventuale_suggerimento"
                }}
            ],
            "errori_critici": ["lista_errori_gravi"],
            "miglioramenti_suggeriti": ["lista_miglioramenti"],
            "parti_mancanti": ["elementi_da_aggiungere"],
            "coerenza_interna": "valutazione_coerenza"
        }}
        """
        
        try:
            response = await self.ollama.generate(prompt, system_prompt)
            logger.info("Risposta ricevuta da Ollama per compliance_checker, parsing JSON...")
            
            # Log della risposta grezza per debug
            logger.debug(f"Risposta grezza compliance_checker: {repr(response[:500])}")
            
            # Pulisci la risposta - gestisci meglio il parsing JSON
            response = response.strip()
            
            # Trova il primo blocco JSON valido
            json_start = -1
            json_end = -1
            
            # Cerca ```json
            if '```json' in response:
                json_start = response.find('```json') + 7
                # Cerca la fine del blocco
                json_end = response.find('```', json_start)
                if json_end != -1:
                    response = response[json_start:json_end].strip()
            elif response.startswith('{') and '}' in response:
                # Se inizia con { trova l'ultimo }
                json_end = response.rfind('}')
                if json_end != -1:
                    response = response[:json_end + 1].strip()
            else:
                # Prova a estrarre JSON da testo che inizia con spiegazione
                lines = response.split('\n')
                json_lines = []
                in_json = False
                brace_count = 0
                
                for line in lines:
                    if line.strip().startswith('{'):
                        in_json = True
                        brace_count = 0
                    
                    if in_json:
                        json_lines.append(line)
                        brace_count += line.count('{') - line.count('}')
                        
                        if brace_count <= 0 and line.strip().endswith('}'):
                            break
                
                if json_lines:
                    response = '\n'.join(json_lines).strip()
            
            # Controllo se la risposta è vuota dopo la pulizia
            if not response:
                logger.error("Risposta vuota dopo pulizia del formato in compliance_checker")
                raise ValueError("Risposta vuota dal modello")
            
            logger.debug(f"Risposta pulita compliance_checker: {repr(response[:200])}")
            result = json.loads(response)
            
            return {
                "success": True,
                "check_level": check_level,
                "compliance_report": result,
                "checked_at": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Errore JSON parsing in compliance_checker: {str(e)}")
            logger.error(f"Contenuto che ha causato l'errore: {repr(response[:1000])}")
            return {
                "success": False,
                "error": f"Errore parsing JSON: {str(e)}",
                "compliance_report": None,
                "raw_response": response[:500] if 'response' in locals() else "N/A"
            }
        except Exception as e:
            logger.error(f"Errore nel controllo conformità: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "compliance_report": None
            }


# Configurazione del server MCP
app = Server("determina-generator-mcp")
ollama_client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
tools = DeterminaTools(ollama_client)


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """Elenca i tools disponibili"""
    return [
        types.Tool(
            name="fascicolo-analyzer",
            description="Analizza fascicolo procedimentale e estrae informazioni strutturate",
            inputSchema={
                "type": "object",
                "properties": {
                    "fascicolo_content": {"type": "string"},
                    "document_types": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["fascicolo_content", "document_types"]
            }
        ),
        types.Tool(
            name="legal-framework-validator",
            description="Valida conformità normativa e identifica framework legale applicabile",
            inputSchema={
                "type": "object",
                "properties": {
                    "procedimento_type": {"type": "string"},
                    "ente_competente": {"type": "string"},
                    "normativa_riferimento": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["procedimento_type", "ente_competente", "normativa_riferimento"]
            }
        ),
        types.Tool(
            name="content-generator",
            description="Genera contenuto specifico per sezioni della determina",
            inputSchema={
                "type": "object",
                "properties": {
                    "section_type": {"type": "string", "enum": ["premesse", "motivazione", "dispositivo"]},
                    "context_data": {"type": "object"},
                    "template_style": {"type": "string"}
                },
                "required": ["section_type", "context_data"]
            }
        ),
        types.Tool(
            name="document-composer",
            description="Compone documento finale della determina",
            inputSchema={
                "type": "object",
                "properties": {
                    "sections": {"type": "object"},
                    "template_id": {"type": "string"},
                    "ente_metadata": {"type": "object"}
                },
                "required": ["sections", "template_id", "ente_metadata"]
            }
        ),
        types.Tool(
            name="compliance-checker",
            description="Verifica conformità legale e qualità del documento",
            inputSchema={
                "type": "object",
                "properties": {
                    "determina_content": {"type": "string"},
                    "check_level": {"type": "string", "enum": ["basic", "full", "expert"]}
                },
                "required": ["determina_content"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Esegue un tool specifico"""
    try:
        logger.info(f"🔧 MCP SERVER - Tool call ricevuto: {name}")
        logger.debug(f"📝 MCP SERVER - Arguments: {json.dumps(arguments, ensure_ascii=False, indent=2)[:500]}...")
        
        if name == "fascicolo-analyzer":
            logger.info("🔍 MCP SERVER - Esecuzione fascicolo-analyzer")
            result = await tools.fascicolo_analyzer(
                arguments["fascicolo_content"],
                arguments["document_types"]
            )
        elif name == "legal-framework-validator":
            logger.info("⚖️ MCP SERVER - Esecuzione legal-framework-validator")
            result = await tools.legal_framework_validator(
                arguments["procedimento_type"],
                arguments["ente_competente"],
                arguments["normativa_riferimento"]
            )
        elif name == "content-generator":
            logger.info("📝 MCP SERVER - Esecuzione content-generator")
            result = await tools.content_generator(
                arguments["section_type"],
                arguments["context_data"],
                arguments.get("template_style", "formale")
            )
        elif name == "document-composer":
            logger.info("📄 MCP SERVER - Esecuzione document-composer")
            result = await tools.document_composer(
                arguments["sections"],
                arguments["template_id"],
                arguments["ente_metadata"]
            )
        elif name == "compliance-checker":
            logger.info("✅ MCP SERVER - Esecuzione compliance-checker")
            result = await tools.compliance_checker(
                arguments["determina_content"],
                arguments.get("check_level", "basic")
            )
        else:
            logger.warning(f"⚠️ MCP SERVER - Tool sconosciuto: {name}")
            raise ValueError(f"Tool sconosciuto: {name}")
        
        logger.info(f"✅ MCP SERVER - Tool {name} completato con successo")
        # Log degli arguments ricevuti (troncati)
        log_truncated(logger, logging.DEBUG, "📥 MCP SERVER - Arguments", arguments, max_chars=1000)
        # Log del risultato (troncato)
        log_truncated(logger, logging.DEBUG, "📦 MCP SERVER - Risultato", result, max_chars=1200)

        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]

    except Exception as e:
        logger.error(f"❌ MCP SERVER - Errore nell'esecuzione del tool {name}: {str(e)}")
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2, ensure_ascii=False)
        )]


async def main():
    """Avvia il server MCP"""
    logger.info("Avvio del server MCP per generazione determine...")
    
    # Create initialization options
    capabilities = types.ServerCapabilities(
        tools=types.ToolsCapability(listChanged=True)
    )
    
    initialization_options = InitializationOptions(
        server_name="determina-generator-mcp",
        server_version="1.0.0",
        capabilities=capabilities
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, initialization_options)


if __name__ == "__main__":
    config.setup_logging()
    asyncio.run(main())
