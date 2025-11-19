"""
Frontend Streamlit per l'applicazione di generazione determine.
Interfaccia utente per upload PDF e visualizzazione output JSON.
"""

import streamlit as st
import asyncio
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, Any, Union

# Import dei moduli locali
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from core.models import *
from core.document_processor import DocumentProcessor
from mcp_client.direct_client import create_direct_generation_service
from core.logging_utils import log_truncated

# Configurazione logging (usa la configurazione centrale che legge .env)
config.setup_logging()
logger = logging.getLogger(__name__)

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Generatore Determine Amministrative",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2e5984;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #cce7ff;
        border: 1px solid #99d1ff;
        color: #004085;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitApp:
    """Classe principale dell'applicazione Streamlit"""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.generation_service = None
        
        # Inizializza sessione
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        if 'fascicolo_data' not in st.session_state:
            st.session_state.fascicolo_data = None
        if 'generated_determina' not in st.session_state:
            st.session_state.generated_determina = None
    
    def render_header(self):
        """Renderizza l'intestazione dell'applicazione"""
        st.markdown('<h1 class="main-header">🏛️ Generatore Determine Amministrative</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <strong>📋 Sistema POC per la generazione automatica di determine amministrative</strong><br>
            Carica i documenti del fascicolo procedimentale e ottieni una bozza di determina strutturata in formato JSON.
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Renderizza la sidebar con configurazioni"""
        st.sidebar.header("⚙️ Configurazioni")
        
        # Configurazione Ollama
        st.sidebar.subheader("🤖 Modello AI")
        ollama_url = st.sidebar.text_input(
            "URL Ollama", 
            value=config.OLLAMA_BASE_URL,
            help="URL del server Ollama (es. http://localhost:11434)"
        )
        
        ollama_model = st.sidebar.selectbox(
            "Modello",
            options=["llama3.2:1b"],
            index=0,
            help="Modello AI da utilizzare per la generazione"
        )
        
        # Configurazione Ente
        st.sidebar.subheader("🏛️ Dati Ente")
        ente_nome = st.sidebar.text_input("Nome Ente", value="Comune di Roma")
        ente_settore = st.sidebar.text_input("Settore", value="Settore Tecnico")
        ente_dirigente = st.sidebar.text_input("Dirigente", value="Dott. Mario Rossi")
        
        # Livello di validazione
        st.sidebar.subheader("✅ Validazione")
        validation_level = st.sidebar.selectbox(
            "Livello controllo",
            options=["basic", "full", "expert"],
            index=1,
            help="Livello di approfondimento del controllo qualità"
        )
        
        # Salva configurazioni in session state
        st.session_state.config = {
            "ollama_url": ollama_url,
            "ollama_model": ollama_model,
            "ente": {
                "nome": ente_nome,
                "settore": ente_settore,
                "dirigente": ente_dirigente
            },
            "validation_level": validation_level
        }
        
        # Stato connessione
        st.sidebar.subheader("🔗 Stato Sistema")
        
        # Controllo automatico dello stato (una sola volta per sessione)
        if 'system_status_checked' not in st.session_state:
            st.session_state.system_status_checked = True
            self.auto_check_system_status(ollama_url)
        
        # Indicatori di stato permanenti
        if hasattr(st.session_state, 'ollama_status'):
            if st.session_state.ollama_status:
                st.sidebar.success("🟢 Ollama: Connesso")
            else:
                st.sidebar.error("🔴 Ollama: Disconnesso")
        
        if hasattr(st.session_state, 'mcp_status'):
            if st.session_state.mcp_status:
                st.sidebar.success("🟢 MCP: Operativo")
            else:
                st.sidebar.warning("🟡 MCP: Modalità Direct")
        
        # Pulsanti di verifica manuale
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔍 Verifica Ollama"):
                self.check_ollama_connection(ollama_url)
        
        with col2:
            if st.button("🔧 Verifica MCP"):
                self.check_mcp_server_status()
    
    def check_ollama_connection(self, url: str):
        """Verifica la connessione a Ollama"""
        try:
            import requests
            response = requests.get(f"{url}/api/tags", timeout=5)
            if response.status_code == 200:
                st.session_state.ollama_status = True
                st.sidebar.success("✅ Ollama connesso")
                models = response.json().get("models", [])
                st.sidebar.write(f"Modelli disponibili: {len(models)}")
            else:
                st.session_state.ollama_status = False
                st.sidebar.error("❌ Ollama non risponde")
        except Exception as e:
            st.session_state.ollama_status = False
            st.sidebar.error(f"❌ Errore connessione: {str(e)}")
    
    def auto_check_system_status(self, ollama_url: str):
        """Controllo automatico dello stato del sistema all'avvio"""
        # Verifica Ollama silenziosamente
        try:
            import requests
            response = requests.get(f"{ollama_url}/api/tags", timeout=3)
            st.session_state.ollama_status = response.status_code == 200
        except:
            st.session_state.ollama_status = False
        
        # Verifica MCP silenziosamente
        try:
            from mcp_client.client import create_mcp_client
            # Non testiamo la connessione effettiva qui per non rallentare l'avvio
            st.session_state.mcp_status = True  # MCP client è disponibile
        except:
            st.session_state.mcp_status = False
    
    def check_mcp_server_status(self):
        """Verifica lo stato del server MCP con diagnostica dettagliata"""
        try:
            # Test di avvio del server MCP
            server_script_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "start_mcp_server.py"  # Usa il script di avvio corretto
            )
            
            # Verifica che il file del server esista
            if not os.path.exists(server_script_path):
                st.session_state.mcp_status = False
                st.sidebar.error("❌ Script server MCP non trovato")
                st.sidebar.error(f"   Percorso: {server_script_path}")
                return

            # Verifica preliminare di Ollama
            ollama_available = False
            try:
                import httpx
                response = httpx.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=5.0)
                if response.status_code == 200:
                    ollama_available = True
                    st.sidebar.success("✅ Ollama: Connesso")
                else:
                    st.sidebar.warning(f"⚠️ Ollama: Status {response.status_code}")
            except Exception as e:
                st.sidebar.error("❌ Ollama: Non raggiungibile")
                st.sidebar.error("   Assicurati che Ollama sia in esecuzione:")
                st.sidebar.code("ollama serve")
                # Non blocchiamo il test MCP anche se Ollama non risponde
                # perché potrebbe essere un problema temporaneo

            # Test di importazione dei moduli necessari
            mcp_client_available = False
            mcp_server_available = False
            
            # Test client MCP
            try:
                from mcp_client.client import create_mcp_client, MCPClient
                mcp_client_available = True
                st.sidebar.success("✅ Client MCP: Disponibile")
            except ImportError as e:
                st.sidebar.error(f"❌ Client MCP: {str(e)}")
            except Exception as e:
                st.sidebar.error(f"❌ Client MCP: Errore {str(e)}")
            
            # Test server MCP
            try:
                from mcp_server.server import DeterminaTools, OllamaClient
                mcp_server_available = True
                st.sidebar.success("✅ Server MCP: Moduli disponibili")
            except ImportError as e:
                st.sidebar.error(f"❌ Server MCP: {str(e)}")
            except Exception as e:
                st.sidebar.error(f"❌ Server MCP: Errore {str(e)}")
            
            if mcp_client_available:
                st.session_state.mcp_status = True
                st.sidebar.info("🔗 Modalità: MCP Protocol")
                
                # Test di connessione al server MCP (asincrono con timeout)
                import asyncio
                async def test_mcp_connection():
                    client = None
                    try:
                        # Prima prova il client diretto (più affidabile)
                        from mcp_client.direct_client import create_direct_mcp_client
                        
                        client = await asyncio.wait_for(
                            create_direct_mcp_client(), 
                            timeout=10.0  # Timeout per connessione diretta
                        )
                        
                        # Test listing tools
                        tools = await asyncio.wait_for(
                            client.list_available_tools(), 
                            timeout=5.0  # Timeout per listing tools
                        )
                        
                        return {
                            'connected': True,
                            'tools_count': len(tools),
                            'tools': tools[:3] if tools else [],  # Prime 3 per non appesantire
                            'error': None,
                            'mode': 'direct'  # Indica che usa il client diretto
                        }
                        
                    except asyncio.TimeoutError:
                        return {
                            'connected': False,
                            'tools_count': 0,
                            'tools': [],
                            'error': 'Timeout connessione - Il server MCP richiede più tempo per avviarsi. Verifica che Ollama sia attivo.'
                        }
                    except Exception as e:
                        error_msg = str(e)
                        if "WouldBlock" in error_msg or "CancelledError" in error_msg:
                            error_msg = "Server non configurato per client esterni"
                        elif "Connection" in error_msg:
                            error_msg = "Server non in esecuzione o non raggiungibile"
                        return {
                            'connected': False,
                            'tools_count': 0,
                            'tools': [],
                            'error': error_msg
                        }
                    finally:
                        if client:
                            try:
                                await client.disconnect()
                            except:
                                pass
                
                # Esegui il test asincrono
                try:
                    if hasattr(asyncio, 'run'):
                        result = asyncio.run(test_mcp_connection())
                    else:
                        # Fallback per versioni più vecchie
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            result = loop.run_until_complete(test_mcp_connection())
                        finally:
                            loop.close()
                    
                    if result['connected']:
                        st.sidebar.success("✅ Server MCP: Connesso")
                        st.sidebar.success(f"🔧 Tools disponibili: {result['tools_count']}")
                        if result.get('mode') == 'direct':
                            st.sidebar.info("🚀 Modalità: Diretto (Ottimizzato)")
                        else:
                            st.sidebar.info("📡 Modalità: Protocollo Standard")
                        if result['tools']:
                            with st.sidebar.expander("📋 Tools principali"):
                                for tool in result['tools']:
                                    st.write(f"• {tool}")
                    else:
                        st.sidebar.warning("⚠️ Server MCP: Non risponde")
                        if result['error']:
                            st.sidebar.error(f"   Errore: {result['error']}")
                        
                        # Suggerimenti per la risoluzione
                        with st.sidebar.expander("💡 Suggerimenti risoluzione"):
                            st.write("🔧 **Diagnosi problema:**")
                            if "Timeout" in result['error']:
                                st.write("⏱️ **Problema**: Server non risponde in tempo")
                                st.write("**Soluzioni**:")
                                st.write("1. Verifica che Ollama sia in esecuzione:")
                                st.code("ollama serve")
                                st.write("2. Il server MCP potrebbe non essere avviato")
                                st.write("3. Ricarica la pagina dopo alcuni secondi")
                            elif "configurato" in result['error']:
                                st.write("⚙️ **Problema**: Server MCP non configurato correttamente")
                                st.write("**Soluzioni**:")
                                st.write("1. Il server MCP è progettato per uso client-server")
                                st.write("2. Non avviarlo manualmente, lascia che l'app lo gestisca")
                                st.write("3. Usa la modalità Direct se MCP non serve")
                            elif "raggiungibile" in result['error']:
                                st.write("🔌 **Problema**: Server non raggiungibile")
                                st.write("**Soluzioni**:")
                                st.write("1. Controlla che Ollama sia attivo")
                                st.write("2. Verifica la configurazione di rete")
                            else:
                                st.write(f"❓ **Errore**: {result['error']}")
                                st.write("**Soluzioni generiche**:")
                                st.write("1. Riavvia l'applicazione")
                                st.write("2. Controlla i log")
                                st.write("3. Verifica la configurazione")
                        
                except Exception as e:
                    st.sidebar.error(f"❌ Test connessione fallito: {str(e)}")
                    
            else:
                st.session_state.mcp_status = False
                st.sidebar.error("❌ Sistema MCP: Non disponibile")
                
        except Exception as e:
            st.session_state.mcp_status = False
            st.sidebar.error(f"❌ Errore verifica MCP: {str(e)}")
    
    def render_upload_section(self):
        """Renderizza la sezione di upload documenti"""
        st.markdown('<h2 class="section-header">📁 Caricamento Documenti</h2>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_files = st.file_uploader(
                "Carica i documenti del fascicolo",
                type=['pdf', 'txt'],
                accept_multiple_files=True,
                help="Seleziona tutti i documenti che compongono il fascicolo procedimentale"
            )
            
            if uploaded_files:
                self.process_uploaded_files(uploaded_files)
        
        with col2:
            if st.session_state.documents:
                st.write(f"**📄 Documenti caricati: {len(st.session_state.documents)}**")
                for i, doc in enumerate(st.session_state.documents):
                    with st.expander(f"📋 {doc['nome']}"):
                        st.write(f"**Tipo:** {doc['tipo']}")
                        st.write(f"**Dimensione:** {doc['dimensione']} bytes")
                        st.write(f"**Caratteri estratti:** {len(doc['contenuto'])}")
                        if st.button(f"🗑️ Rimuovi", key=f"remove_{i}"):
                            st.session_state.documents.pop(i)
                            st.rerun()
    
    def process_uploaded_files(self, uploaded_files):
        """Processa i file caricati ed estrae il contenuto"""
        logger.info(f"📁 FRONTEND - Processamento {len(uploaded_files)} file caricati")
        
        for uploaded_file in uploaded_files:
            logger.info(f"📄 FRONTEND - Processamento file: {uploaded_file.name}")
            
            # Controlla se il file è già stato processato
            if any(doc['nome'] == uploaded_file.name for doc in st.session_state.documents):
                logger.info(f"⚠️ FRONTEND - File {uploaded_file.name} già processato, skip")
                continue
            
            # Salva temporaneamente il file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            logger.debug(f"💾 FRONTEND - File salvato temporaneamente: {tmp_path}")
            
            try:
                # Estrai contenuto
                logger.info(f"🔍 FRONTEND - Estrazione contenuto da {uploaded_file.name}")
                content = self.doc_processor.process_document(tmp_path)
                logger.info(f"✅ FRONTEND - Estratti {len(content)} caratteri da {uploaded_file.name}")
                
                # Classifica tipo documento
                logger.info(f"🏷️ FRONTEND - Classificazione tipo documento per {uploaded_file.name}")
                doc_type = self.doc_processor.classify_document_type(uploaded_file.name, content)
                
                # Aggiungi alla lista
                doc_data = {
                    'nome': uploaded_file.name,
                    'tipo': doc_type.value,
                    'dimensione': len(uploaded_file.getvalue()),
                    'contenuto': content,
                    'data_caricamento': datetime.now()
                }
                
                st.session_state.documents.append(doc_data)
                
            except Exception as e:
                st.error(f"Errore nel processamento di {uploaded_file.name}: {str(e)}")
            
            finally:
                # Pulisci file temporaneo
                os.unlink(tmp_path)
    
    def render_fascicolo_section(self):
        """Renderizza la sezione di configurazione fascicolo"""
        if not st.session_state.documents:
            return
        
        st.markdown('<h2 class="section-header">📋 Configurazione Fascicolo</h2>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Dati Richiedente")
            nome = st.text_input("Nome", value="Mario")
            cognome = st.text_input("Cognome", value="Rossi")
            codice_fiscale = st.text_input("Codice Fiscale", value="RSSMRA80A01H501X")
            email = st.text_input("Email", value="mario.rossi@email.com")
        
        with col2:
            st.subheader("📑 Dati Procedimento")
            procedimento_type = st.selectbox(
                "Tipo Procedimento",
                options=[p.value for p in ProcedimentoType],
                index=0
            )
            
            urgente = st.checkbox("Procedimento urgente")
            note = st.text_area("Note aggiuntive", height=100)
        
        if st.button("💾 Crea Fascicolo", type="primary"):
            self.create_fascicolo_data(nome, cognome, codice_fiscale, email, 
                                     procedimento_type, urgente, note)
    
    def create_fascicolo_data(self, nome: str, cognome: str, codice_fiscale: str, 
                            email: str, procedimento_type: str, urgente: bool, note: str):
        """Crea l'oggetto FascicoloData"""
        try:
            # Crea anagrafica richiedente
            richiedente = AnagraficaRichiedente(
                nome=nome,
                cognome=cognome,
                codice_fiscale=codice_fiscale,
                email=email
            )
            
            # Crea riferimenti documenti
            documenti = []
            for i, doc in enumerate(st.session_state.documents):
                doc_ref = DocumentReference(
                    id=f"doc_{i+1}",
                    nome=doc['nome'],
                    tipo=DocumentType(doc['tipo']),
                    percorso=f"uploaded/{doc['nome']}",
                    dimensione=doc['dimensione'],
                    data_caricamento=doc['data_caricamento'],
                    contenuto_estratto=doc['contenuto']
                )
                documenti.append(doc_ref)
            
            # Crea fascicolo
            fascicolo = FascicoloData(
                id=f"fasc_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                data_apertura=datetime.now(),
                procedimento_type=ProcedimentoType(procedimento_type),
                richiedente=richiedente,
                documenti=documenti,
                note=note,
                urgente=urgente
            )
            
            st.session_state.fascicolo_data = fascicolo
            
            st.markdown("""
            <div class="success-box">
                ✅ <strong>Fascicolo creato con successo!</strong><br>
                Ora puoi procedere con la generazione della determina.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Errore nella creazione del fascicolo: {str(e)}")
    
    def render_generation_section(self):
        """Renderizza la sezione di generazione determina"""
        if not st.session_state.fascicolo_data:
            return
        
        st.markdown('<h2 class="section-header">⚡ Generazione Determina</h2>', 
                   unsafe_allow_html=True)
        
        # Mostra riassunto fascicolo
        with st.expander("📋 Riassunto Fascicolo", expanded=False):
            fascicolo = st.session_state.fascicolo_data
            st.write(f"**ID:** {fascicolo.id}")
            st.write(f"**Richiedente:** {fascicolo.richiedente.nome} {fascicolo.richiedente.cognome}")
            st.write(f"**Tipo Procedimento:** {fascicolo.procedimento_type.value}")
            st.write(f"**Documenti:** {len(fascicolo.documenti)}")
            st.write(f"**Urgente:** {'Sì' if fascicolo.urgente else 'No'}")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🗑️ Cancella Cronologia", use_container_width=True):
                if 'generation_progress' in st.session_state:
                    st.session_state.generation_progress = []
                    st.success("Cronologia cancellata!")
        
        with col2:
            if st.button("🚀 Genera Determina", type="primary", use_container_width=True):
                self.generate_determina()
        
        with col3:
            if 'generation_progress' in st.session_state and st.session_state.generation_progress:
                st.info(f"📊 {len(st.session_state.generation_progress)} operazioni registrate")
    
    def generate_determina(self):
        """Genera la determina usando il servizio MCP con progress tracking"""
        
        logger.info("🚀 FRONTEND - Inizio generazione determina")
        logger.info(f"📊 FRONTEND - Documenti disponibili: {len(st.session_state.documents)}")
        
        # Inizializza il progress tracking
        if 'generation_progress' not in st.session_state:
            st.session_state.generation_progress = []
        
        # Container per il progress tracking
        progress_container = st.container()
        status_container = st.container()
        
        with status_container:
            status_placeholder = st.empty()
        
        with progress_container:
            progress_placeholder = st.empty()
        
        try:
            logger.info("🔄 FRONTEND - Avvio processo asincrono di generazione")
            # Esegui la generazione con progress tracking
            result = asyncio.run(self._async_generate_determina_with_progress(
                progress_placeholder, status_placeholder
            ))
            
            # Gestisci il risultato
            logger.info("📋 FRONTEND - Gestione risultato generazione")
            self._handle_generation_result(result)
                
        except Exception as e:
            logger.error(f"❌ FRONTEND - Errore durante la generazione: {str(e)}")
            st.error(f"Errore nel processo di generazione: {str(e)}")
            logger.error(f"Errore generazione: {str(e)}")
    
    def _handle_generation_result(self, result):
        """Gestisce il risultato della generazione"""
        if isinstance(result, dict):
            # Risultato dal direct service (dict)
            if result.get("success", False):
                st.session_state.generated_determina = result
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Determina generata con successo!</strong><br>
                    Controlla i risultati nella sezione sottostante.
                </div>
                """, unsafe_allow_html=True)
            else:
                error_msg = result.get("error", "Errore sconosciuto")
                st.markdown(f"""
                <div class="error-box">
                    ❌ <strong>Errore nella generazione:</strong><br>
                    {error_msg}
                </div>
                """, unsafe_allow_html=True)
        else:
            # Risultato dal MCP service (DeterminaGenerationResponse)
            if result.status == GenerationStatus.GENERATED:
                st.session_state.generated_determina = result
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Determina generata con successo!</strong><br>
                    Controlla i risultati nella sezione sottostante.
                </div>
                """, unsafe_allow_html=True)
            elif result.status == GenerationStatus.ERROR:
                st.markdown(f"""
                <div class="error-box">
                    ❌ <strong>Errore nella generazione:</strong><br>
                    {result.error_message}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"Generazione parziale: {result.status}")
    
    def _update_progress(self, progress_placeholder, tool_name: str, status: str, details: str = ""):
        """Aggiorna il display del progresso con timing"""
        from datetime import datetime
        
        current_time = datetime.now()
        timestamp = current_time.strftime("%H:%M:%S")
        
        # Inizializza il timing se non esiste
        if 'generation_start_time' not in st.session_state:
            st.session_state.generation_start_time = current_time
            st.session_state.last_step_time = current_time
        
        # Calcola i tempi
        elapsed_total = (current_time - st.session_state.generation_start_time).total_seconds()
        elapsed_step = (current_time - st.session_state.last_step_time).total_seconds()
        
        # Aggiorna il tempo dell'ultimo step
        st.session_state.last_step_time = current_time
        
        # Aggiungi alla cronologia
        if 'generation_progress' not in st.session_state:
            st.session_state.generation_progress = []
            
        st.session_state.generation_progress.append({
            "timestamp": timestamp,
            "tool": tool_name,
            "status": status,
            "details": details,
            "elapsed_step": elapsed_step,
            "elapsed_total": elapsed_total
        })
        
        # Usa componenti Streamlit nativi invece di HTML
        with progress_placeholder.container():
            st.subheader("🔄 Cronologia Generazione con Timing")
            
            # Mostra il tempo totale trascorso
            total_minutes = int(elapsed_total // 60)
            total_seconds = int(elapsed_total % 60)
            st.info(f"⏱️ **Tempo totale trascorso**: {total_minutes:02d}:{total_seconds:02d}")
            
            # Mostra gli ultimi 10 passi
            recent_progress = st.session_state.generation_progress[-10:]
            
            for step in recent_progress:
                # Formatta i tempi
                step_time = f"{step['elapsed_step']:.1f}s"
                total_time = f"{int(step['elapsed_total']//60):02d}:{int(step['elapsed_total']%60):02d}"
                
                # Determina colore e icona
                time_info = f"⏱️ +{step_time} | 🕐 {total_time}"
                
                if "Completato" in step["status"]:
                    st.success(f"✅ **{step['tool']}** - {step['status']} ({step['timestamp']}) | {time_info}")
                elif "corso" in step["status"]:
                    st.info(f"⚙️ **{step['tool']}** - {step['status']} ({step['timestamp']}) | {time_info}")
                elif "Errore" in step["status"]:
                    st.error(f"❌ **{step['tool']}** - {step['status']} ({step['timestamp']}) | {time_info}")
                elif "Iniziato" in step["status"]:
                    st.info(f"🚀 **{step['tool']}** - {step['status']} ({step['timestamp']}) | {time_info}")
                else:
                    st.write(f"📋 **{step['tool']}** - {step['status']} ({step['timestamp']}) | {time_info}")
                
                # Mostra dettagli se disponibili
                if step["details"]:
                    st.caption(f"└─ {step['details']}")
            
            # Mostra statistiche finali
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"📊 Operazioni: {len(st.session_state.generation_progress)}")
            with col2:
                if len(st.session_state.generation_progress) > 1:
                    avg_time = elapsed_total / len(st.session_state.generation_progress)
                    st.caption(f"⏱️ Media: {avg_time:.1f}s/step")
            with col3:
                completed_steps = sum(1 for step in st.session_state.generation_progress if "Completato" in step["status"])
                st.caption(f"✅ Completati: {completed_steps}")
    
    async def _async_generate_determina_with_progress(self, progress_placeholder, status_placeholder):
        """Esegue la generazione asincrona con progress tracking"""
        
        # Reset del timing per una nuova generazione
        from datetime import datetime
        st.session_state.generation_start_time = datetime.now()
        st.session_state.last_step_time = datetime.now()
        st.session_state.generation_progress = []
        
        # Inizializza il progresso
        self._update_progress(progress_placeholder, "Sistema", "🚀 Iniziato", "Inizializzazione del sistema di generazione")
        
        try:
            # Path al server MCP
            server_script_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "mcp_server", "server.py"
            )
            
            # Status update
            status_placeholder.info("🔌 Connessione al servizio MCP...")
            self._update_progress(progress_placeholder, "MCP Client", "⚙️ In corso", "Creazione del client MCP")
            
            # Crea il servizio di generazione MCP
            service = await create_direct_generation_service()
            
            self._update_progress(progress_placeholder, "MCP Client", "✅ Completato", "Client MCP connesso con successo")
            
            # Metadati ente dalla configurazione
            ente_metadata = st.session_state.config["ente"]
            
            # Status update
            status_placeholder.info("📋 Avvio generazione determina...")
            self._update_progress(progress_placeholder, "Generazione", "🚀 Iniziato", "Avvio del processo di generazione completa")
            
            # Genera la determina usando MCP con callback per il progresso
            result = await self._generate_with_tool_tracking(
                service, progress_placeholder, status_placeholder
            )
            
            self._update_progress(progress_placeholder, "Sistema", "✅ Completato", "Generazione determina completata")
            status_placeholder.success("✅ Generazione completata!")
            
            return result
            
        except Exception as e:
            self._update_progress(progress_placeholder, "Sistema", "❌ Errore", f"Errore: {str(e)}")
            status_placeholder.error(f"❌ Errore: {str(e)}")
            raise
    
    async def _generate_with_tool_tracking(self, service, progress_placeholder, status_placeholder):
        """Genera la determina con tracking dettagliato dei tool"""
        from datetime import datetime
        
        # Tool tracking wrapper
        original_invoke = service.mcp_client.invoke_tool
        
        async def tracked_invoke_tool(tool_name, parameters):
            # Update progress per ogni tool
            tool_display_names = {
                "fascicolo-analyzer": "📁 Analisi Fascicolo",
                "legal-framework-validator": "⚖️ Validazione Normativa", 
                "content-generator": "📝 Generazione Contenuti",
                "document-composer": "📄 Composizione Documento",
                "compliance-checker": "✅ Verifica Conformità"
            }
            
            display_name = tool_display_names.get(tool_name, f"🔧 {tool_name}")
            
            # Timing per questo tool specifico
            tool_start_time = datetime.now()
            
            # Avvia tool
            param_size = len(str(parameters)) if parameters else 0
            self._update_progress(progress_placeholder, display_name, "🚀 Iniziato", f"Parametri: {param_size} caratteri")
            status_placeholder.info(f"⚙️ {display_name} in corso...")
            # Log dei parametri inviati (debug troncato)
            log_truncated(logger, logging.DEBUG, f"FRONTEND - Invio {tool_name} parametri", parameters, max_chars=800)
            
            try:
                # Esegui il tool originale
                result = await original_invoke(tool_name, parameters)
                
                # Calcola tempo di esecuzione del tool
                tool_duration = (datetime.now() - tool_start_time).total_seconds()
                
                # Analizza il risultato per dettagli
                # Log del risultato ricevuto (debug troncato)
                log_truncated(logger, logging.DEBUG, f"FRONTEND - Risposta {tool_name}", result, max_chars=1200)
                details = f"Durata: {tool_duration:.1f}s"
                if isinstance(result, dict):
                    if result.get("success"):
                        details += " | Successo"
                        if "analysis" in result:
                            details += f" | Analisi: {len(str(result['analysis']))} caratteri"
                        if result.get("fallback_used"):
                            details += " | ⚠️ Recovery utilizzato"
                    else:
                        error_msg = result.get('error', 'Sconosciuto')[:50]
                        details += f" | Errore: {error_msg}"
                        if result.get("fallback_used"):
                            details += " | 🔄 Fallback applicato"
                
                self._update_progress(progress_placeholder, display_name, "✅ Completato", details)
                return result
                
            except Exception as e:
                tool_duration = (datetime.now() - tool_start_time).total_seconds()
                error_details = f"Durata: {tool_duration:.1f}s | Errore: {str(e)[:50]}"
                self._update_progress(progress_placeholder, display_name, "❌ Errore", error_details)
                raise
        
        # Sostituisci temporaneamente il metodo invoke_tool
        service.mcp_client.invoke_tool = tracked_invoke_tool
        
        try:
            # Esegui la generazione completa
            result = await service.generate_complete_determina(
                st.session_state.fascicolo_data,
                st.session_state.config["ente"]
            )
            return result
        finally:
            # Ripristina il metodo originale
            service.mcp_client.invoke_tool = original_invoke
    
    def prepare_fascicolo_for_service(self, fascicolo: FascicoloData) -> Dict[str, Any]:
        """Converte il FascicoloData in formato dict per il servizio diretto"""
        if not fascicolo:
            return {"content": "", "document_types": []}
        
        # Estrai il contenuto di tutti i documenti
        content_parts = []
        document_types = []
        
        for doc in fascicolo.documenti:
            if doc.contenuto_estratto:
                content_parts.append(f"=== {doc.nome} ===\n{doc.contenuto_estratto}")
            document_types.append(doc.tipo.value if hasattr(doc.tipo, 'value') else str(doc.tipo))
        
        content = "\n\n".join(content_parts)
        
        return {
            "content": content,
            "document_types": list(set(document_types)),  # Rimuovi duplicati
            "fascicolo_id": fascicolo.id,
            "richiedente": {
                "nome": fascicolo.richiedente.nome,
                "cognome": fascicolo.richiedente.cognome,
                "codice_fiscale": fascicolo.richiedente.codice_fiscale,
                "email": fascicolo.richiedente.email
            },
            "procedimento_type": fascicolo.procedimento_type.value if hasattr(fascicolo.procedimento_type, 'value') else str(fascicolo.procedimento_type),
            "urgente": fascicolo.urgente,
            "note": fascicolo.note,
            "data_apertura": fascicolo.data_apertura.isoformat() if fascicolo.data_apertura else None
        }
    
    def render_results_section(self):
        """Renderizza la sezione con i risultati della generazione"""
        if not st.session_state.generated_determina:
            return
        
        st.markdown('<h2 class="section-header">📄 Risultati Generazione</h2>', 
                   unsafe_allow_html=True)
        
        result = st.session_state.generated_determina
        
        # Tabs per organizzare i risultati
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Determina", "✅ Validazione", "📊 Metadati", "💾 Download"])
        
        # Gestisci entrambi i formati: MCP (DeterminaGenerationResponse) e Direct Service (dict)
        if isinstance(result, dict):
            # Formato Direct Service
            with tab1:
                self.render_determina_content_new(result.get("determina", {}))
            
            with tab2:
                self.render_validation_results_new(result.get("determina", {}).get("compliance", {}))
            
            with tab3:
                self.render_metadata_new(result.get("metadata", {}))
            
            with tab4:
                self.render_download_section_new(result)
        else:
            # Formato MCP (DeterminaGenerationResponse)
            with tab1:
                self.render_determina_content_mcp(result.content)
            
            with tab2:
                self.render_validation_results_mcp(result.validation_results)
            
            with tab3:
                self.render_metadata_mcp(result.metadata)
            
            with tab4:
                self.render_download_section_mcp(result)
    
    def render_determina_content_new(self, determina_data: Dict[str, Any]):
        """Renderizza il contenuto della determina nel nuovo formato"""
        if not determina_data:
            st.warning("Nessun contenuto generato")
            return
        
        # Documento finale
        documento = determina_data.get("documento", {}).get("documento", {})
        if documento:
            st.subheader("📝 Intestazione")
            intestazione = documento.get("intestazione", "Non disponibile")
            st.text_area("", value=intestazione, height=100, key="intestazione_view")
            
            st.subheader("📄 Corpo del Documento")
            corpo = documento.get("corpo", "Non disponibile")
            st.text_area("", value=corpo, height=300, key="corpo_view")
            
            st.subheader("⚖️ Dispositivo")
            dispositivo = documento.get("dispositivo", "Non disponibile")
            st.text_area("", value=dispositivo, height=200, key="dispositivo_view")
            
            st.subheader("✍️ Firme")
            firme = documento.get("firme", "Non disponibile")
            st.text_area("", value=firme, height=100, key="firme_view")
        
        # Analisi fascicolo
        analisi = determina_data.get("analisi_fascicolo", {})
        if analisi and analisi.get("success"):
            with st.expander("📂 Analisi Fascicolo"):
                soggetti = analisi.get("soggetti", {})
                if soggetti:
                    st.write("**Soggetti coinvolti:**")
                    st.write(f"- Richiedente: {soggetti.get('richiedente', 'N/A')}")
                    st.write(f"- Beneficiario: {soggetti.get('beneficiario', 'N/A')}")
                    st.write(f"- Responsabile: {soggetti.get('responsabile', 'N/A')}")
                
                procedimento = analisi.get("procedimento", {})
                if procedimento:
                    st.write("**Procedimento:**")
                    st.write(f"- Oggetto: {procedimento.get('oggetto', 'N/A')}")
                    st.write(f"- Tipo: {procedimento.get('tipo', 'N/A')}")
    
    def render_validation_results_new(self, compliance_data: Dict[str, Any]):
        """Renderizza i risultati della validazione nel nuovo formato"""
        if not compliance_data:
            st.info("Nessun risultato di validazione disponibile")
            return
        
        compliance = compliance_data.get("compliance", {})
        if compliance:
            col1, col2, col3 = st.columns(3)
            with col1:
                conforme = compliance.get("conforme", False)
                st.metric("Conformità", "✅ Conforme" if conforme else "❌ Non conforme")
            with col2:
                punteggio = compliance.get("punteggio", 0.0)
                st.metric("Punteggio", f"{punteggio:.2f}")
            with col3:
                verifiche = f"{compliance.get('verifiche_superate', 0)}/{compliance.get('verifiche_totali', 0)}"
                st.metric("Verifiche", verifiche)
        
        dettagli = compliance_data.get("dettagli", {})
        if dettagli:
            # Errori critici
            errori = dettagli.get("errori_critici", [])
            if errori:
                st.subheader("🔴 Errori Critici")
                for errore in errori:
                    st.error(errore)
            
            # Avvertimenti
            avvertimenti = dettagli.get("avvertimenti", [])
            if avvertimenti:
                st.subheader("🟡 Avvertimenti")
                for avvertimento in avvertimenti:
                    st.warning(avvertimento)
            
            # Suggerimenti
            suggerimenti = dettagli.get("suggerimenti", [])
            if suggerimenti:
                st.subheader("💡 Suggerimenti")
                for suggerimento in suggerimenti:
                    st.info(suggerimento)
    
    def render_metadata_new(self, metadata: Dict[str, Any]):
        """Renderizza i metadati nel nuovo formato"""
        if not metadata:
            st.info("Nessun metadato disponibile")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            timestamp = metadata.get("timestamp", "N/A")
            st.write(f"**Data Generazione:** {timestamp}")
            template = metadata.get("template_used", "N/A")
            st.write(f"**Template:** {template}")
        
        with col2:
            ente = metadata.get("ente", "N/A")
            st.write(f"**Ente:** {ente}")
    
    def render_download_section_new(self, result: Dict[str, Any]):
        """Renderizza la sezione download nel nuovo formato"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Download JSON completo
            json_str = json.dumps(result, indent=2, ensure_ascii=False, default=str)
            
            st.download_button(
                label="📥 Scarica JSON Completo",
                data=json_str,
                file_name=f"determina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Download solo contenuto determina
            documento = result.get("determina", {}).get("documento", {}).get("documento", {})
            if documento:
                content_str = f"""INTESTAZIONE:
{documento.get('intestazione', 'Non disponibile')}

CORPO DEL DOCUMENTO:
{documento.get('corpo', 'Non disponibile')}

DISPOSITIVO:
{documento.get('dispositivo', 'Non disponibile')}

FIRME:
{documento.get('firme', 'Non disponibile')}
"""
                
                st.download_button(
                    label="📄 Scarica Testo Determina",
                    data=content_str,
                    file_name=f"determina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
    
    def render_determina_content_mcp(self, content):
        """Renderizza il contenuto della determina per formato MCP"""
        st.markdown("### 📋 Contenuto Determina")
        
        if hasattr(content, 'preambolo') and content.preambolo:
            with st.expander("📝 Preambolo", expanded=True):
                st.markdown(content.preambolo)
        
        if hasattr(content, 'motivazione') and content.motivazione:
            with st.expander("⚖️ Motivazione", expanded=True):
                st.markdown(content.motivazione)
        
        if hasattr(content, 'dispositivo') and content.dispositivo:
            with st.expander("📋 Dispositivo", expanded=True):
                st.markdown(content.dispositivo)
        
        if hasattr(content, 'premesse') and content.premesse:
            with st.expander("📖 Premesse", expanded=False):
                for i, premessa in enumerate(content.premesse, 1):
                    st.markdown(f"**{i}.** {premessa}")

    def render_validation_results_mcp(self, validation_results):
        """Renderizza i risultati di validazione per formato MCP"""
        st.markdown("### ✅ Risultati Validazione")
        
        if hasattr(validation_results, 'compliance_score'):
            score = validation_results.compliance_score
            color = "green" if score >= 0.8 else "orange" if score >= 0.6 else "red"
            st.markdown(f"**Punteggio Conformità:** <span style='color: {color}; font-weight: bold;'>{score:.2%}</span>", 
                       unsafe_allow_html=True)
        
        if hasattr(validation_results, 'issues') and validation_results.issues:
            with st.expander("⚠️ Problemi Rilevati"):
                for issue in validation_results.issues:
                    st.warning(f"• {issue}")
        
        if hasattr(validation_results, 'suggestions') and validation_results.suggestions:
            with st.expander("💡 Suggerimenti"):
                for suggestion in validation_results.suggestions:
                    st.info(f"• {suggestion}")

    def render_metadata_mcp(self, metadata):
        """Renderizza i metadati per formato MCP"""
        st.markdown("### 📊 Metadati")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if hasattr(metadata, 'generation_time'):
                st.metric("⏱️ Tempo Generazione", f"{metadata.generation_time:.2f}s")
            if hasattr(metadata, 'model_used'):
                st.metric("🤖 Modello", metadata.model_used)
        
        with col2:
            if hasattr(metadata, 'timestamp'):
                st.metric("📅 Timestamp", metadata.timestamp)
            if hasattr(metadata, 'version'):
                st.metric("📦 Versione", metadata.version)
        
        if hasattr(metadata, 'processing_info') and metadata.processing_info:
            with st.expander("🔧 Informazioni Elaborazione"):
                for key, value in metadata.processing_info.items():
                    st.text(f"{key}: {value}")

    def render_download_section_mcp(self, result):
        """Sezione download per formato MCP"""
        st.markdown("### Download Documenti")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download dati JSON
            json_data = {
                "content": {
                    "preambolo": getattr(result.content, 'preambolo', ''),
                    "motivazione": getattr(result.content, 'motivazione', ''),
                    "dispositivo": getattr(result.content, 'dispositivo', ''),
                    "premesse": getattr(result.content, 'premesse', [])
                },
                "validation_results": {
                    "compliance_score": getattr(result.validation_results, 'compliance_score', 0),
                    "issues": getattr(result.validation_results, 'issues', []),
                    "suggestions": getattr(result.validation_results, 'suggestions', [])
                },
                "metadata": {
                    "generation_time": getattr(result.metadata, 'generation_time', 0),
                    "model_used": getattr(result.metadata, 'model_used', ''),
                    "timestamp": getattr(result.metadata, 'timestamp', ''),
                    "version": getattr(result.metadata, 'version', ''),
                    "processing_info": getattr(result.metadata, 'processing_info', {})
                }
            }
            
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Scarica JSON Completo",
                data=json_str,
                file_name=f"determina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            # Download solo contenuto determina
            content_str = f"""PREAMBOLO:
{getattr(result.content, 'preambolo', 'Non disponibile')}

MOTIVAZIONE:
{getattr(result.content, 'motivazione', 'Non disponibile')}

DISPOSITIVO:
{getattr(result.content, 'dispositivo', 'Non disponibile')}

PREMESSE:
{chr(10).join(getattr(result.content, 'premesse', []))}
"""
            
            st.download_button(
                label="📄 Scarica Testo Determina",
                data=content_str,
                file_name=f"determina_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    def run(self):
        """Esegue l'applicazione Streamlit"""
        self.render_header()
        self.render_sidebar()
        
        # Sezioni principali
        self.render_upload_section()
        self.render_fascicolo_section()
        self.render_generation_section()
        self.render_results_section()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            🏛️ <strong>Sistema POC Generazione Determine Amministrative</strong><br>
            Powered by Ollama + Llama3.2:1b + MCP + Streamlit
        </div>
        """, unsafe_allow_html=True)


def main():
    """Funzione principale"""
    # Configura l'ambiente
    config.setup_logging()
    config.ensure_directories()
    
    # Avvia l'app
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main()
