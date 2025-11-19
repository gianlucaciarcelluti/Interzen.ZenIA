"""
POC Streamlit: Classificatore Procedimenti Amministrativi
Sistema per identificare procedimento → provvedimento da istanze di parte
"""

import streamlit as st
import os
from pathlib import Path
from groq_procedural_classifier import ProceduralClassifier
from guardrail_pertinenza import check_context_relevance, get_guardrail_recommendation
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Carica .env
try:
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    env_file = root_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
except Exception:
    load_dotenv()

# Configurazione pagina
st.set_page_config(
    page_title="Classificatore Procedimenti - SP00",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: var(--background-color);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4facfe;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .success-box {
        background-color: rgba(40, 167, 69, 0.15);
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.15);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inizializza session state
if 'classification_history' not in st.session_state:
    st.session_state.classification_history = []
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🏛️ SP00 - Classificatore Procedimenti Amministrativi</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">
        Sistema AI per classificazione istanze di parte → procedimento → provvedimento
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")
    
    # API Key
    groq_api_key_from_env = os.environ.get("GROQ_API_KEY", "")
    
    if groq_api_key_from_env:
        st.success("✅ API Key caricata da .env")
    
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=groq_api_key_from_env,
        help="Inserisci la tua API key di Groq",
        placeholder="gsk_..."
    )
    
    # Selezione modello
    model_options = {
        "llama-3.3-70b-versatile": "🚀 Llama 3.3 70B (Raccomandato)",
        "llama-3.1-8b-instant": "⚡ Llama 3.1 8B (Veloce)",
        "mixtral-8x7b-32768": "💎 Mixtral 8x7B",
    }
    
    selected_model = st.selectbox(
        "Modello AI",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    
    st.divider()
    
    # Configurazione Guardrail
    st.subheader("🛡️ Configurazione Guardrail")
    
    use_llm_guardrail = st.checkbox(
        "Usa LLM per casi borderline",
        value=True,
        help="""
        Guardrail a 2 livelli:
        
        LIVELLO 1 (sempre attivo, gratuito):
        - Verifica keyword PA (istantanea)
        - Blocca casi ovvi fuori contesto
        
        LIVELLO 2 (opzionale, a pagamento):
        - Analisi LLM sofisticata
        - Solo per casi borderline (confidenza 40-70%)
        - Maggiore accuratezza ma costa token
        """
    )
    
    if use_llm_guardrail:
        st.info("""
        ✅ **Guardrail Ibrido Attivo**
        
        - 🔤 Livello 1: Keyword (sempre)
        - 🧠 Livello 2: LLM (solo casi dubbi)
        
        Massima accuratezza con costi ottimizzati!
        """)
    else:
        st.warning("""
        ⚠️ **Solo Guardrail Keyword**
        
        - 🔤 Livello 1: Keyword (solo questo)
        - ❌ Livello 2: LLM disabilitato
        
        Gratuito ma meno accurato su casi complessi.
        """)
    
    st.divider()
    
    # Info sul sistema
    st.subheader("📊 Info Sistema")
    st.markdown("""
    **Classificazione Singola Dimensione:**
    
    **PROCEDIMENTO → PROVVEDIMENTO**
    
    Esempi:
    - Autorizzazione Scarico Acque
      → Determinazione Dirigenziale
    - Variante Urbanistica  
      → Delibera Consiglio
    - Licenza Commerciale
      → Determinazione Dirigenziale
    """)
    
    st.divider()
    
    # Esempi rapidi
    st.subheader("📝 Esempi Rapidi")
    
    examples = {
        "Ambiente - Scarico Acque": """Spettabile Comune, la scrivente ABC S.p.A. richiede autorizzazione allo scarico di acque reflue industriali provenienti dal ciclo produttivo tessile. Portata media: 500 m³/giorno. Si allegano relazione tecnica e planimetria degli impianti.""",
        
        "Urbanistica - Permesso Costruire": """Il sottoscritto Mario Rossi chiede il rilascio del permesso di costruire per la realizzazione di un fabbricato residenziale unifamiliare sito in Via Roma 123. Superficie coperta: 150 mq. Si allegano elaborati progettuali.""",
        
        "Commercio - Licenza": """Il sottoscritto Giuseppe Verdi chiede il rilascio della licenza per l'esercizio di attività commerciale di abbigliamento presso i locali siti in Corso Italia 45. Superficie: 80 mq.""",
        
        "Sociale - Alloggio ERP": """Si richiede assegnazione alloggio di edilizia residenziale pubblica per nucleo familiare composto da 4 persone. Reddito ISEE allegato. In possesso dei requisiti previsti dalla normativa regionale.""",
    }
    
    for label, text in examples.items():
        if st.button(f"📄 {label}", use_container_width=True):
            st.session_state.current_text = text
            st.rerun()

# Area principale - Input
st.header("📧 Istanza da Classificare")

istanza_text = st.text_area(
    "Inserisci il testo dell'istanza di parte",
    value=st.session_state.current_text,
    height=200,
    placeholder="Es: Spettabile Comune, si richiede...",
    help="Incolla qui il testo dell'istanza presentata dal cittadino/azienda"
)

# Colonne per bottoni
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    classify_button = st.button("🚀 Classifica Istanza", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Pulisci", use_container_width=True)

with col3:
    if st.session_state.classification_history:
        download_data = pd.DataFrame(st.session_state.classification_history)
        csv = download_data.to_csv(index=False)
        st.download_button(
            label="💾 Scarica",
            data=csv,
            file_name=f"classificazioni_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

if clear_button:
    st.session_state.current_text = ""
    st.rerun()

# Classificazione
if classify_button:
    if not api_key:
        st.error("⚠️ Inserisci la tua Groq API Key nella sidebar!")
    elif not istanza_text.strip():
        st.warning("⚠️ Inserisci un testo da classificare!")
    else:
        # GUARDRAIL: Verifica pertinenza del contesto
        is_relevant, relevance_conf, relevance_reason, guardrail_method, llm_analysis = check_context_relevance(
            istanza_text, 
            api_key=api_key,
            model=selected_model,
            use_llm_for_borderline=use_llm_guardrail
        )
        
        # Mostra risultato guardrail
        if not is_relevant:
            st.error("🚫 **ATTENZIONE: Testo Fuori Contesto!**")
            st.warning(f"""
            **Il testo inserito non sembra pertinente al dominio PA (procedimenti amministrativi).**
            
            **Metodo verifica:** {guardrail_method}
            
            **Motivo:** {relevance_reason}
            
            **Confidenza di pertinenza:** {relevance_conf:.1%}
            
            ⚠️ **La classificazione potrebbe essere un FALSO POSITIVO.** 
            Si raccomanda di inserire testi relativi a:
            - Istanze/richieste verso la PA
            - Procedimenti amministrativi
            - Richieste di autorizzazioni, permessi, licenze
            - Certificati o documenti amministrativi
            """)
            
            # Mostra analisi LLM se disponibile
            if llm_analysis:
                with st.expander("🧠 Analisi Dettagliata LLM"):
                    st.markdown(llm_analysis)
            
            st.divider()
        else:
            st.success(f"✅ Testo pertinente al dominio PA (confidenza: {relevance_conf:.1%})")
            with st.expander("ℹ️ Dettaglio verifica pertinenza"):
                st.info(f"**Metodo:** {guardrail_method}\n\n**Motivo:** {relevance_reason}")
                
                # Mostra analisi LLM se disponibile
                if llm_analysis:
                    st.markdown("---")
                    st.markdown(llm_analysis)
        
        with st.spinner("🔄 Classificazione in corso..."):
            try:
                # Inizializza classifier
                classifier = ProceduralClassifier(api_key=api_key, model=selected_model)
                
                # Classifica
                result = classifier.classify_single(istanza_text)
                
                if not result.get('success'):
                    error_msg = result.get('error', 'Errore sconosciuto')
                    st.error(f"❌ Errore durante la classificazione: {error_msg}")
                else:
                    # Salva nello storico
                    history_entry = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'istanza_preview': istanza_text[:100] + "..." if len(istanza_text) > 100 else istanza_text,
                        'procedimento': result.get('procedimento', 'N/A'),
                        'tipo_provvedimento': result.get('tipo_provvedimento', 'N/A'),
                        'categoria': result.get('categoria', 'N/A'),
                        'confidence': result.get('confidence', 0.0),
                        'model': selected_model
                    }
                    st.session_state.classification_history.insert(0, history_entry)
                    
                    # Mantieni solo ultime 50
                    if len(st.session_state.classification_history) > 50:
                        st.session_state.classification_history = st.session_state.classification_history[:50]
                    
                    st.success("✅ Classificazione completata!")
                    
                    # Alert per testo fuori contesto
                    if not is_relevant:
                        st.error("""
                        🚫 **TESTO FUORI CONTESTO**: La classificazione è probabilmente un falso positivo. 
                        Ignorare i risultati.
                        """)
                        st.divider()
                    
                    # Risultati principali
                    st.header("🎯 Risultati Classificazione")
                    
                    # Metriche principali
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            label="Procedimento",
                            value=result.get('procedimento', 'N/A'),
                            delta=result.get('categoria', '')
                        )
                    
                    with col2:
                        st.metric(
                            label="Provvedimento",
                            value=result.get('tipo_provvedimento', 'N/A')
                        )
                    
                    with col3:
                        conf = result.get('confidence', 0.0)
                        st.metric(
                            label="Confidence",
                            value=f"{conf:.1%}",
                            delta="Alta" if conf >= 0.8 else "Media" if conf >= 0.6 else "Bassa"
                        )
                    
                    with col4:
                        st.metric(
                            label="Termini",
                            value=f"{result.get('termini_giorni', 'N/A')} gg"
                        )
                    
                    # Dettagli procedimento
                    st.divider()
                    st.subheader("📋 Dettagli Procedimento")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Denominazione:** {result.get('procedimento_denominazione', 'N/A')}
                        
                        **Categoria:** {result.get('categoria', 'N/A')}
                        
                        **Sottocategoria:** {result.get('sottocategoria', 'N/A')}
                        
                        **Autorità Competente:** {result.get('autorita_competente', 'N/A')}
                        """)
                    
                    with col2:
                        normativa = result.get('normativa_base', [])
                        st.markdown("**Normativa di Riferimento:**")
                        for norm in normativa:
                            st.markdown(f"- {norm}")
                    
                    # Motivazione
                    st.divider()
                    st.subheader("💡 Motivazione")
                    st.info(result.get('motivazione', 'Nessuna motivazione disponibile'))
                    
                    # Metadata estratti
                    if result.get('metadata_extracted'):
                        st.divider()
                        st.subheader("📊 Metadata Estratti")
                        
                        metadata = result['metadata_extracted']
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Richiedente:**", metadata.get('richiedente', 'N/A'))
                            st.write("**Oggetto:**", metadata.get('oggetto_sintetico', 'N/A'))
                        
                        with col2:
                            keywords = metadata.get('keywords_chiave', [])
                            st.write("**Keywords:**")
                            for kw in keywords:
                                st.write(f"- {kw}")
                    
                    # Dettagli tecnici
                    with st.expander("🔧 Dettagli Tecnici"):
                        st.write("**Modello:**", selected_model)
                        st.write("**Token utilizzati:**", result.get('tokens_used', 'N/A'))
                        st.write("**Latenza:**", f"{result.get('latency', 0):.3f}s")
                        st.write("**Timestamp:**", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        
                        st.subheader("JSON Completo")
                        st.json(result)
                    
                    # Raccomandazioni
                    st.divider()
                    st.subheader("📌 Raccomandazioni")
                    
                    confidence = result.get('confidence', 0.0)
                    
                    # Priorità massima: testo fuori contesto
                    if not is_relevant:
                        st.error(f"""
                        🚫 **TESTO FUORI CONTESTO - Revisione Obbligatoria**
                        
                        - ❌ Il testo non sembra pertinente al dominio PA
                        - ❌ La classificazione è probabilmente un FALSO POSITIVO
                        - ❌ NON utilizzare questi risultati per workflow operativi
                        - ✅ Verificare che il testo riguardi procedimenti amministrativi
                        - ✅ Riformulare inserendo informazioni su istanze/richieste alla PA
                        
                        {get_guardrail_recommendation(is_relevant, relevance_conf)}
                        """)
                    elif confidence >= 0.8:
                        st.success("""
                        ✅ **Alta Confidenza**
                        
                        La classificazione è affidabile. Procedere con il workflow corrispondente.
                        """)
                    elif confidence >= 0.6:
                        st.warning("""
                        ⚠️ **Media Confidenza**
                        
                        La classificazione è probabilmente corretta ma richiede verifica manuale.
                        """)
                    else:
                        st.error("""
                        ❌ **Bassa Confidenza**
                        
                        Revisione manuale obbligatoria. Il sistema non è sicuro della classificazione.
                        """)
                    
            except Exception as e:
                st.error(f"❌ Errore: {str(e)}")
                st.exception(e)

# Storico
if st.session_state.classification_history:
    st.divider()
    st.header("📊 Storico Classificazioni")
    
    history_df = pd.DataFrame(st.session_state.classification_history)
    
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Statistiche
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Totale", len(history_df))
    
    with col2:
        avg_conf = history_df['confidence'].mean()
        st.metric("Conf. Media", f"{avg_conf:.1%}")
    
    with col3:
        most_common = history_df['categoria'].mode()[0] if len(history_df) > 0 else "N/A"
        st.metric("Categoria + Frequente", most_common)
    
    with col4:
        if st.button("🗑️ Pulisci Storico", use_container_width=True):
            st.session_state.classification_history = []
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏛️ <strong>SP00 - Procedural Classifier</strong> | Powered by Groq AI</p>
    <p style="font-size: 0.9rem;">Sistema POC per classificazione procedimenti amministrativi</p>
</div>
""", unsafe_allow_html=True)
