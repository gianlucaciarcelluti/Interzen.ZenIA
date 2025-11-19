"""
POC Streamlit: Classificatore Sinistri Medical Malpractice con Groq
Sistema di classificazione multi-dimensionale con spiegazioni e confidence scores
"""

import streamlit as st
import os
from pathlib import Path
from groq_integration import GroqClassifier
import pandas as pd
from datetime import datetime
import json
import requests


def check_context_relevance_basic(text):
    """
    Verifica VELOCE basata su keyword per filtrare casi ovvi.
    Questo è il primo livello del guardrail (gratuito e istantaneo).
    
    Args:
        text: Testo da verificare
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str, keyword_count: int)
    """
    text_lower = text.lower()
    
    # Termini chiave che indicano pertinenza al dominio medical malpractice
    domain_keywords = {
        # Termini medici/sanitari
        'medico', 'sanitario', 'ospedale', 'clinica', 'paziente', 'chirurgia', 'intervento',
        'diagnosi', 'terapia', 'cura', 'infermiere', 'dottore', 'reparto', 'pronto soccorso',
        'ricovero', 'degenza', 'cartella clinica', 'anamnesi', 'prescrizione', 'farmaco',
        'radiologia', 'laboratorio', 'analisi', 'esame', 'visita', 'ambulatorio',
        
        # Termini assicurativi/sinistri
        'sinistro', 'risarcimento', 'danni', 'responsabilità', 'malpractice', 'malasanità',
        'polizza', 'assicurazione', 'perizia', 'perito', 'ctp', 'danno', 'lesione',
        'indennizzo', 'evento avverso', 'errore medico', 'complicanza', 'negligenza',
        'messa in mora', 'richiesta danni', 'pratica', 'claim',
        
        # Termini procedurali/amministrativi rilevanti
        'segnalazione', 'incident', 'risk', 'audit', 'protocollo', 'procedura',
        'documentazione', 'criticità', 'valutazione', 'follow-up', 'aggiornamento'
    }
    
    # Conta quante keyword sono presenti
    keyword_count = sum(1 for keyword in domain_keywords if keyword in text_lower)
    
    # Calcola la densità di keyword rispetto alla lunghezza del testo
    word_count = len(text.split())
    keyword_density = keyword_count / max(word_count, 1)
    
    # Criteri di pertinenza
    min_keywords = 2  # Almeno 2 keyword nel dominio
    min_density = 0.05  # Almeno 5% delle parole devono essere keyword
    min_length = 20  # Almeno 20 caratteri
    
    # Verifica pertinenza
    is_relevant = (
        keyword_count >= min_keywords and
        keyword_density >= min_density and
        len(text.strip()) >= min_length
    )
    
    # Calcola confidenza (0-1)
    confidence = min(1.0, (keyword_count / 5) * (keyword_density / 0.1))
    
    # Genera ragione
    if not is_relevant:
        if len(text.strip()) < min_length:
            reason = f"Testo troppo breve ({len(text.strip())} caratteri, minimo {min_length})"
        elif keyword_count < min_keywords:
            reason = f"Poche keyword rilevanti trovate ({keyword_count}/{min_keywords} richieste)"
        elif keyword_density < min_density:
            reason = f"Densità keyword troppo bassa ({keyword_density:.2%} vs {min_density:.2%} richiesto)"
        else:
            reason = "Testo non pertinente al contesto"
    else:
        reason = f"Keyword check: {keyword_count} keyword trovate, densità {keyword_density:.2%}"
    
    return is_relevant, confidence, reason, keyword_count


# Costante per il modello LLM di default
DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"

def check_context_relevance_llm(text, api_key, model=DEFAULT_LLM_MODEL):
    """
    Verifica AVANZATA usando LLM per casi borderline o quando serve maggiore accuratezza.
    Questo è il secondo livello del guardrail (a pagamento ma molto accurato).
    
    Args:
        text: Testo da verificare
        api_key: API key di Groq
        model: Modello LLM da usare
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str, llm_analysis: str)
    """
    from groq import Groq
    import json
    import time
    
    try:
        client = Groq(api_key=api_key)
        
        # Prompt ottimizzato per verifica pertinenza
        system_prompt = """Sei un esperto analizzatore di testi per il dominio medical malpractice e assicurazioni sanitarie.

Il tuo compito è determinare se un testo è PERTINENTE a questo dominio specifico.

Un testo è PERTINENTE se riguarda:
- Sinistri medici (eventi avversi, errori medici, complicanze)
- Segnalazioni a compagnie assicurative
- Richieste di risarcimento per danni medici
- Comunicazioni medico/ospedale → compagnia assicurativa
- Risk management sanitario
- Incident reporting medico
- Follow-up di pratiche assicurative sanitarie

Un testo è NON PERTINENTE se:
- È una domanda generica (es: "Che tempo fa?")
- Riguarda argomenti completamente diversi (sport, cucina, tecnologia, ecc.)
- È una conversazione casuale
- Non ha nessun collegamento con medicina, sanità o assicurazioni sanitarie

Rispondi in formato JSON con questa struttura:
{
    "is_relevant": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "spiegazione dettagliata del perché",
    "domain_match": "quale aspetto del dominio corrisponde (se pertinente)"
}

Sii RIGOROSO: solo testi chiaramente legati al dominio medical malpractice/assicurazioni sanitarie sono pertinenti."""

        user_prompt = f"""Analizza questo testo e determina se è pertinente al dominio medical malpractice/assicurazioni sanitarie:

TESTO:
{text}

Rispondi SOLO con il JSON richiesto, senza altre spiegazioni."""

        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Bassa temperatura per risposte deterministiche
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        latency = time.time() - start_time
        
        # Parse JSON response
        content = response.choices[0].message.content or "{}"
        result = json.loads(content)
        
        is_relevant = result.get('is_relevant', False)
        confidence = float(result.get('confidence', 0.5))
        reasoning = result.get('reasoning', 'Nessuna motivazione fornita')
        domain_match = result.get('domain_match', 'N/A')
        
        # Costruisci analisi dettagliata
        token_count = response.usage.total_tokens if response.usage else 0
        llm_analysis = f"""**Analisi LLM ({model}):**
- Pertinente: {'✅ SÌ' if is_relevant else '❌ NO'}
- Confidenza: {confidence:.1%}
- Ragionamento: {reasoning}
- Match dominio: {domain_match}
- Latenza: {latency:.2f}s
- Token usati: {token_count}"""
        
        reason = f"LLM Analysis: {reasoning[:100]}..." if len(reasoning) > 100 else f"LLM Analysis: {reasoning}"
        
        return is_relevant, confidence, reason, llm_analysis
        
    except Exception as e:
        # Fallback in caso di errore LLM
        return None, 0.5, f"Errore LLM: {str(e)}", f"⚠️ Errore durante verifica LLM: {str(e)}"


def check_context_relevance(text, api_key="", model=DEFAULT_LLM_MODEL, use_llm_for_borderline=False):
    """
    GUARDRAIL IBRIDO a due livelli per massima efficienza e accuratezza.
    
    LIVELLO 1 (Keyword-based, veloce e gratuito):
    - Blocca immediatamente casi ovviamente NON pertinenti
    - Approva immediatamente casi ovviamente pertinenti
    
    LIVELLO 2 (LLM-based, accurato ma a pagamento):
    - Usato SOLO per casi borderline (confidenza 40-70%)
    - Fornisce analisi sofisticata quando necessaria
    
    Args:
        text: Testo da verificare
        api_key: API key Groq (opzionale, serve solo per verifica LLM)
        model: Modello LLM da usare per verifica avanzata
        use_llm_for_borderline: Se True, usa LLM per casi borderline
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str, method: str, llm_analysis: str)
    """
    # LIVELLO 1: Verifica keyword (sempre eseguita, veloce e gratuita)
    is_relevant_kw, confidence_kw, reason_kw, keyword_count = check_context_relevance_basic(text)
    
    # Casi OVVI: confidenza molto alta o molto bassa
    # Non serve LLM, il keyword check è sufficiente
    if confidence_kw >= 0.7 or confidence_kw < 0.01 or not use_llm_for_borderline or not api_key:
        method = "🔤 Keyword-based (livello 1)"
        llm_analysis = None
        
        # Aggiungi info keyword alla reason
        reason_final = f"{reason_kw} [Keyword: {keyword_count}]"
        
        return is_relevant_kw, confidence_kw, reason_final, method, llm_analysis
    
    # Casi BORDERLINE (confidenza 40-70%): usa LLM per verifica sofisticata
    # LIVELLO 2: Verifica LLM (solo se necessario)
    method = "🧠 Keyword + LLM (livello 1+2, caso borderline)"
    
    is_relevant_llm, confidence_llm, reason_llm, llm_analysis = check_context_relevance_llm(
        text, api_key, model
    )
    
    # Se LLM fallisce, usa risultato keyword
    if is_relevant_llm is None:
        method = "🔤 Keyword-based (livello 1, LLM fallito)"
        return is_relevant_kw, confidence_kw, f"{reason_kw} (LLM non disponibile)", method, llm_analysis
    
    # Combina risultati: LLM ha priorità ma considera anche keyword
    # Se entrambi concordano, massima confidenza
    # Se discordano, usa confidenza LLM ma abbassata
    
    if is_relevant_kw == is_relevant_llm:
        # Concordano: aumenta confidenza
        final_confidence = min(1.0, (confidence_kw + confidence_llm) / 2 + 0.1)
        final_is_relevant = is_relevant_llm
        final_reason = f"Concordanza Keyword+LLM: {reason_llm}"
    else:
        # Discordano: usa LLM ma con confidenza ridotta
        final_confidence = confidence_llm * 0.8
        final_is_relevant = is_relevant_llm
        final_reason = f"Discordanza (LLM prevale): {reason_llm}"
    
    return final_is_relevant, final_confidence, final_reason, method, llm_analysis


# Carica variabili d'ambiente dal file .env se esiste
try:
    from dotenv import load_dotenv
    
    # Cerca il file .env nella root del progetto (2 livelli sopra)
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent  # src/llm_classifier -> src -> root
    env_file = root_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ File .env caricato da: {env_file}")
    else:
        # Prova anche nella directory corrente
        load_dotenv()
        print("ℹ️ Cercando .env nella directory corrente")
except ImportError:
    # python-dotenv non installato, usa solo variabili d'ambiente di sistema
    pass

# Funzione per recuperare modelli disponibili da Groq
@st.cache_data(ttl=3600)  # Cache per 1 ora
def get_available_models(api_key=None):
    """
    Recupera i modelli disponibili dall'API Groq
    """
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "")
    
    if not api_key:
        # Fallback ai modelli di default se non c'è API key
        return {
            "llama-3.1-8b-instant": "Llama 3.1 8B Instant",
            "llama-3.2-1b-preview": "Llama 3.2 1B Preview",
            "llama-3.2-3b-preview": "Llama 3.2 3B Preview"
        }
    
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            models = {}
            
            # Filtra solo i modelli adatti per chat/completions
            # Escludi whisper (audio), playai-tts (speech), guard (safety)
            exclude_keywords = ['whisper', 'tts', 'guard', 'prompt-guard']
            
            for model in data.get('data', []):
                model_id = model.get('id', '')
                
                # Salta modelli da escludere
                if any(keyword in model_id.lower() for keyword in exclude_keywords):
                    continue
                
                # Crea nome leggibile
                display_name = model_id
                
                # Mappature per nomi più leggibili
                if 'llama-3.1-8b-instant' in model_id:
                    display_name = "⚡ Llama 3.1 8B Instant (Veloce)"
                elif 'llama-3.3-70b' in model_id:
                    display_name = "🚀 Llama 3.3 70B Versatile (Potente)"
                elif 'llama-4-maverick' in model_id:
                    display_name = "🎯 Llama 4 Maverick 17B"
                elif 'llama-4-scout' in model_id:
                    display_name = "🔍 Llama 4 Scout 17B"
                elif 'deepseek-r1' in model_id:
                    display_name = "🧠 DeepSeek R1 Distill 70B"
                elif 'gemma2-9b' in model_id:
                    display_name = "💎 Gemma 2 9B IT"
                elif 'compound-mini' in model_id:
                    display_name = "⚡ Groq Compound Mini"
                elif 'compound' in model_id and 'mini' not in model_id:
                    display_name = "🔥 Groq Compound"
                elif 'kimi-k2' in model_id:
                    display_name = "🌙 Kimi K2 Instruct"
                elif 'gpt-oss' in model_id:
                    display_name = f"🤖 GPT OSS {model_id.split('-')[-1].upper()}"
                elif 'qwen3' in model_id:
                    display_name = "🇨🇳 Qwen3 32B"
                elif 'allam' in model_id:
                    display_name = "🌍 Allam 2 7B"
                
                models[model_id] = display_name
            
            # Se abbiamo modelli, ritorna quelli
            if models:
                return models
        
    except Exception as e:
        print(f"⚠️ Errore nel recupero modelli: {e}")
    
    # Fallback ai modelli di default
    return {
        "llama-3.1-8b-instant": "⚡ Llama 3.1 8B Instant (Veloce)",
        "llama-3.3-70b-versatile": "🚀 Llama 3.3 70B Versatile (Potente)",
        "gemma2-9b-it": "💎 Gemma 2 9B IT"
    }

# Configurazione pagina
st.set_page_config(
    page_title="Classificatore Sinistri - Groq AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: var(--background-color);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .metric-card h4 {
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        color: var(--text-color);
    }
    .success-box {
        background-color: rgba(40, 167, 69, 0.15);
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .success-box h3, .success-box p {
        color: var(--text-color);
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.15);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box h3, .warning-box p {
        color: var(--text-color);
    }
    .error-box {
        background-color: rgba(220, 53, 69, 0.15);
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box h3, .error-box p {
        color: var(--text-color);
    }
    .info-box {
        background-color: rgba(23, 162, 184, 0.15);
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .info-box h3, .info-box p {
        color: var(--text-color);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    .indicator-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.25rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Inizializza session state (DEVE essere prima della sidebar!)
if 'classification_history' not in st.session_state:
    st.session_state.classification_history = []
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Classificatore Sinistri Medical Malpractice</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">
        Sistema AI per classificazione multi-dimensionale con Groq
    </p>
    <p style="font-size: 0.95rem; margin-top: 0.5rem; opacity: 0.9;">
        🛡️ Guardrail Ibrido Attivo: Verifica keyword + LLM per massima accuratezza
    </p>
    <p style="font-size: 0.85rem; margin-top: 0.25rem; opacity: 0.8;">
        Livello 1 (gratuito): Keyword matching • Livello 2 (opzionale): Analisi LLM casi borderline
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Configurazione
with st.sidebar:
    st.header("⚙️ Configurazione")
    
    # Verifica se esiste un file .env (nella root o nella directory corrente)
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    env_file_root = root_dir / '.env'
    env_file_local = Path('.env')
    
    env_file_exists = env_file_root.exists() or env_file_local.exists()
    groq_api_key_from_env = os.environ.get("GROQ_API_KEY", "")
    
    if groq_api_key_from_env and env_file_root.exists():
        st.success("✅ API Key caricata da .env (root)")
    elif groq_api_key_from_env and env_file_local.exists():
        st.success("✅ API Key caricata da .env (locale)")
    elif groq_api_key_from_env:
        st.info("ℹ️ API Key da variabile d'ambiente")
    
    # API Key
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=groq_api_key_from_env,
        help="Inserisci la tua API key di Groq o salvala nel file .env come GROQ_API_KEY=your-key-here",
        placeholder="gsk_..." if not groq_api_key_from_env else ""
    )
    
    # Selezione modello - carica dinamicamente da API Groq
    model_options = get_available_models(api_key or groq_api_key_from_env)
    
    # Trova l'indice del modello default (migliore dall'analisi)
    default_model = "llama-3.3-70b-versatile"
    default_index = list(model_options.keys()).index(default_model) if default_model in model_options else 0
    
    selected_model = st.selectbox(
        "Modello AI",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=default_index,
        help="Scegli il modello LLM per la classificazione (aggiornato automaticamente dall'API Groq)"
    )
    
    # Pulsante per ricaricare i modelli
    if st.button("🔄 Aggiorna Lista Modelli", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Configurazione Guardrail
    st.subheader("🛡️ Configurazione Guardrail")
    
    use_llm_guardrail = st.checkbox(
        "Usa LLM per casi borderline",
        value=True,
        help="""
        Guardrail a 2 livelli:
        
        LIVELLO 1 (sempre attivo, gratuito):
        - Verifica keyword (istantanea)
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
    **Classificazione Multi-Dimensionale:**
    
    1️⃣ **Tipologia**
    - 0: Sinistro Avvenuto
    - 1: Circostanza Potenziale
    
    2️⃣ **Riferimento Temporale**
    - 0: Fatto Iniziale
    - 1: Follow-up
    """)
    
    st.divider()
    
    # Esempi rapidi
    st.subheader("📝 Esempi Rapidi")
    
    examples = {
        "Sinistro Iniziale (0,0)": "Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente. Il paziente è stato informato e richiede risarcimento. Allego documentazione clinica completa.",
        
        "Sinistro Follow-up (0,1)": "Rif. pratica SIN234567 - Dr. Bianchi. Invio documentazione medica integrativa richiesta dal vs perito. Allego referto specialistico che conferma nesso causale tra procedura e danno lamentato dal paziente. La famiglia ha aggiornato la richiesta risarcitoria.",
        
        "Circostanza Iniziale (1,0)": "Spett.le compagnia, Dr.ssa Verdi, responsabile Qualità. Segnalo near miss verificatosi il 20/03/2024: infermiere ha preparato farmaco per paziente sbagliato ma errore intercettato prima della somministrazione. Nessun danno al paziente. Implementate procedure correttive.",
        
        "Circostanza Follow-up (1,1)": "Rif. segnalazione CIRC789012 del 20/03/2024. Come richiesto invio relazione finale incident reporting. Il near miss è stato analizzato, implementato nuovo protocollo doppio controllo. Nessun danno occorso, situazione risolta."
    }
    
    if st.button("🚨 Sinistro Iniziale", use_container_width=True):
        st.session_state.current_text = examples["Sinistro Iniziale (0,0)"]
        st.rerun()
    
    if st.button("📋 Sinistro Follow-up", use_container_width=True):
        st.session_state.current_text = examples["Sinistro Follow-up (0,1)"]
        st.rerun()
    
    if st.button("⚠️ Circostanza Iniziale", use_container_width=True):
        st.session_state.current_text = examples["Circostanza Iniziale (1,0)"]
        st.rerun()
    
    if st.button("📝 Circostanza Follow-up", use_container_width=True):
        st.session_state.current_text = examples["Circostanza Follow-up (1,1)"]
        st.rerun()

# Area principale - Input
st.header("📧 Testo da Classificare")

# Text area con testo corrente
email_text = st.text_area(
    "Inserisci il testo dell'email da classificare",
    value=st.session_state.current_text,
    height=200,
    placeholder="Es: Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare...",
    help="Incolla qui il testo dell'email da parte del medico/ospedale verso la compagnia assicurativa"
)

# Colonne per bottoni
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    classify_button = st.button("🚀 Classifica Email", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Pulisci", use_container_width=True)

with col3:
    if st.session_state.classification_history:
        download_data = pd.DataFrame(st.session_state.classification_history)
        csv = download_data.to_csv(index=False)
        st.download_button(
            label="💾 Scarica Storico",
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
    elif not email_text.strip():
        st.warning("⚠️ Inserisci un testo da classificare!")
    else:
        # GUARDRAIL: Verifica pertinenza del contesto
        is_relevant, relevance_conf, relevance_reason, guardrail_method, llm_analysis = check_context_relevance(
            email_text, 
            api_key=api_key,
            model=selected_model,
            use_llm_for_borderline=use_llm_guardrail
        )
        
        # Mostra risultato guardrail
        if not is_relevant:
            st.error("🚫 **ATTENZIONE: Testo Fuori Contesto!**")
            st.warning(f"""
            **Il testo inserito non sembra pertinente al dominio di classificazione (sinistri medical malpractice).**
            
            **Metodo verifica:** {guardrail_method}
            
            **Motivo:** {relevance_reason}
            
            **Confidenza di pertinenza:** {relevance_conf:.1%}
            
            ⚠️ **La classificazione potrebbe essere un FALSO POSITIVO.** 
            Si raccomanda di inserire testi relativi a:
            - Sinistri medici
            - Segnalazioni di eventi avversi
            - Richieste di risarcimento
            - Follow-up di pratiche assicurative sanitarie
            """)
            
            # Mostra analisi LLM se disponibile
            if llm_analysis:
                with st.expander("🧠 Analisi Dettagliata LLM"):
                    st.markdown(llm_analysis)
            
            st.divider()
        else:
            st.success(f"✅ Testo pertinente al dominio (confidenza: {relevance_conf:.1%})")
            with st.expander("ℹ️ Dettaglio verifica pertinenza"):
                st.info(f"**Metodo:** {guardrail_method}\n\n**Motivo:** {relevance_reason}")
                
                # Mostra analisi LLM se disponibile
                if llm_analysis:
                    st.markdown("---")
                    st.markdown(llm_analysis)
        
        with st.spinner("🔄 Classificazione in corso..."):
            try:
                # Inizializza classifier
                classifier = GroqClassifier(api_key=api_key, model=selected_model)
                
                # Classifica (progress bar disabilitata per UI Streamlit)
                results = classifier.classify_batch([email_text])
                
                if results.empty or not results.iloc[0]['success']:
                    error_msg = results.iloc[0].get('error', 'Errore sconosciuto') if not results.empty else 'Nessun risultato ricevuto'
                    st.error(f"❌ Errore durante la classificazione: {error_msg}")
                    st.info("💡 Verifica che l'API key sia corretta e che tu abbia credito disponibile su Groq")
                else:
                    result = results.iloc[0]
                    
                    # Salva nello storico
                    history_entry = {
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'email_preview': email_text[:100] + "..." if len(email_text) > 100 else email_text,
                        'tipologia': result['tipologia'],
                        'riferimento': result['riferimento_temporale'],
                        'confidence_tip': result['confidence_tipologia'],
                        'confidence_rif': result['confidence_riferimento'],
                        'model': selected_model
                    }
                    st.session_state.classification_history.insert(0, history_entry)
                    
                    # Mantieni solo ultime 50 classificazioni
                    if len(st.session_state.classification_history) > 50:
                        st.session_state.classification_history = st.session_state.classification_history[:50]
                    
                    st.success("✅ Classificazione completata con successo!")
                    
                    # Alert per testo fuori contesto
                    if not is_relevant:
                        st.error("""
                        🚫 **TESTO FUORI CONTESTO**: La classificazione è probabilmente un falso positivo. 
                        Ignorare i risultati.
                        """)
                        st.divider()
                    
                    # Risultati principali
                    st.header("🎯 Risultati Classificazione")
                    
                    # Metriche principali in colonne
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        tipologia_label = "Sinistro Avvenuto" if result['tipologia'] == 0 else "Circostanza Potenziale"
                        tipologia_icon = "🚨" if result['tipologia'] == 0 else "⚠️"
                        st.metric(
                            label="Tipologia",
                            value=f"{tipologia_icon} {tipologia_label}",
                            delta=f"Classe {result['tipologia']}"
                        )
                    
                    with col2:
                        rif_label = "Fatto Iniziale" if result['riferimento_temporale'] == 0 else "Follow-up"
                        rif_icon = "📨" if result['riferimento_temporale'] == 0 else "📋"
                        st.metric(
                            label="Riferimento Temporale",
                            value=f"{rif_icon} {rif_label}",
                            delta=f"Classe {result['riferimento_temporale']}"
                        )
                    
                    with col3:
                        conf_tip = result['confidence_tipologia']
                        # Determina colore confidenza
                        if conf_tip >= 0.8:
                            conf_color = "Verde"
                            conf_emoji = "✅"
                        elif conf_tip >= 0.6:
                            conf_color = "Giallo"
                            conf_emoji = "⚠️"
                        else:
                            conf_color = "Rosso"
                            conf_emoji = "❌"
                        # Determina livello confidenza
                        if conf_tip >= 0.8:
                            delta_tip = "Alta"
                        elif conf_tip >= 0.6:
                            delta_tip = "Media"
                        else:
                            delta_tip = "Bassa"
                        
                        st.metric(
                            label="Confidence Tipologia",
                            value=f"{conf_emoji} {conf_tip:.1%}",
                            delta=delta_tip
                        )
                    
                    with col4:
                        conf_rif = result['confidence_riferimento']
                        # Determina colore confidenza
                        if conf_rif >= 0.8:
                            conf_color = "Verde"
                            conf_emoji = "✅"
                        elif conf_rif >= 0.6:
                            conf_color = "Giallo"
                            conf_emoji = "⚠️"
                        else:
                            conf_color = "Rosso"
                            conf_emoji = "❌"
                        st.metric(
                            label="Confidence Riferimento",
                            value=f"{conf_emoji} {conf_rif:.1%}",
                            delta="Alta" if conf_rif >= 0.8 else "Media" if conf_rif >= 0.6 else "Bassa"
                        )
                    
                    # Classificazione combinata
                    st.divider()
                    combined_label = f"{tipologia_label} - {rif_label}"
                    combined_code = f"({result['tipologia']}, {result['riferimento_temporale']})"
                    
                    if result['tipologia'] == 0 and result['riferimento_temporale'] == 0:
                        box_class = "error-box"
                        icon = "🚨"
                        description = "Sinistro già verificato - Prima segnalazione del caso"
                    elif result['tipologia'] == 0 and result['riferimento_temporale'] == 1:
                        box_class = "warning-box"
                        icon = "📋"
                        description = "Sinistro già verificato - Aggiornamento/integrazione"
                    elif result['tipologia'] == 1 and result['riferimento_temporale'] == 0:
                        box_class = "info-box"
                        icon = "⚠️"
                        description = "Circostanza potenziale - Prima segnalazione"
                    else:
                        box_class = "success-box"
                        icon = "📝"
                        description = "Circostanza potenziale - Aggiornamento/chiusura"
                    
                    st.markdown(f"""
                    <div class="{box_class}">
                        <h3>{icon} Classificazione Combinata</h3>
                        <p style="font-size: 1.2rem; font-weight: bold; margin: 0.5rem 0;">
                            {combined_label} {combined_code}
                        </p>
                        <p style="margin: 0.5rem 0;">{description}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Spiegazione dettagliata
                    st.header("💡 Ragionamento e Motivazioni")
                    
                    if result.get('spiegazione'):
                        st.info(f"**📝 Spiegazione del Modello AI**\n\n{result['spiegazione']}")
                    
                    # Indicatori chiave
                    if result.get('indicatori_chiave') and isinstance(result['indicatori_chiave'], list):
                        st.subheader("🔑 Indicatori Chiave Identificati")
                        
                        # Mostra indicatori come badge usando colonne
                        cols = st.columns(min(len(result['indicatori_chiave']), 3))
                        for idx, indicator in enumerate(result['indicatori_chiave']):
                            col_idx = idx % 3
                            with cols[col_idx]:
                                st.markdown(f"""
                                <div class="indicator-badge">
                                    {indicator}
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Dettagli tecnici
                    with st.expander("🔧 Dettagli Tecnici"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Classificazione:**")
                            st.write("- Modello utilizzato:", selected_model)
                            st.write("- Token utilizzati:", result.get('tokens_used', 'N/A'))
                            st.write("- Latenza classificazione:", f"{result.get('latency', 0):.3f}s")
                            st.write("- Timestamp:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            st.write("- Success:", "✅" if result['success'] else "❌")
                        
                        with col2:
                            st.write("**Guardrail:**")
                            st.write(f"- Pertinenza: {'✅ SÌ' if is_relevant else '❌ NO'} ({relevance_conf:.1%})")
                            st.write("- Metodo verifica:", guardrail_method)
                            st.write("- Motivazione:", relevance_reason[:50] + "..." if len(relevance_reason) > 50 else relevance_reason)
                            st.write(f"- LLM usato: {'✅ Sì' if llm_analysis else '❌ No'}")
                            
                        # Mostra analisi LLM completa se disponibile
                        if llm_analysis:
                            st.divider()
                            st.markdown("**🧠 Analisi LLM Guardrail Completa:**")
                            st.markdown(llm_analysis)
                        
                        # JSON completo
                        st.subheader("📄 Response JSON Completa")
                        response_dict = result.to_dict()
                        st.json(response_dict)
                    
                    # Raccomandazioni
                    st.header("📌 Raccomandazioni")
                    
                    avg_confidence = (result['confidence_tipologia'] + result['confidence_riferimento']) / 2
                    
                    # Priorità massima: testo fuori contesto
                    if not is_relevant:
                        st.error("""
                        🚫 **TESTO FUORI CONTESTO - Revisione Obbligatoria**
                        
                        - ❌ Il testo non sembra pertinente al dominio medical malpractice
                        - ❌ La classificazione è probabilmente un FALSO POSITIVO
                        - ❌ NON utilizzare questi risultati per workflow operativi
                        - ✅ Verificare che il testo riguardi sinistri medici o segnalazioni sanitarie
                        - ✅ Riformulare il testo includendo informazioni mediche/assicurative pertinenti
                        """)
                    elif avg_confidence >= 0.8:
                        st.success("""
                        ✅ **Alta Confidenza nella Classificazione**
                        
                        - La classificazione è affidabile e può essere utilizzata direttamente
                        - I punteggi di confidenza sono elevati per entrambe le dimensioni
                        - Procedi con il workflow corrispondente alla categoria identificata
                        """)
                    elif avg_confidence >= 0.6:
                        st.warning("""
                        ⚠️ **Confidenza Media - Revisione Consigliata**
                        
                        - La classificazione è probabilmente corretta ma richiede verifica
                        - Controlla gli indicatori chiave e la spiegazione fornita
                        - Considera una revisione manuale prima di procedere
                        """)
                    else:
                        st.error("""
                        ❌ **Bassa Confidenza - Revisione Necessaria**
                        
                        - La classificazione potrebbe non essere accurata
                        - Richiesta revisione manuale obbligatoria
                        - Verifica che il testo sia completo e pertinente
                        - Considera di fornire più contesto se possibile
                        """)
                    
            except Exception as e:
                st.error(f"❌ Errore durante la classificazione: {str(e)}")
                st.exception(e)

# Storico classificazioni
if st.session_state.classification_history:
    st.divider()
    st.header("📊 Storico Classificazioni")
    
    # Converti in DataFrame
    history_df = pd.DataFrame(st.session_state.classification_history)
    
    # Aggiungi etichette leggibili
    history_df['Tipologia_Label'] = history_df['tipologia'].map({
        0: '🚨 Sinistro',
        1: '⚠️ Circostanza'
    })
    history_df['Riferimento_Label'] = history_df['riferimento'].map({
        0: '📨 Iniziale',
        1: '📋 Follow-up'
    })
    
    # Mostra tabella
    display_df = history_df[[
        'timestamp',
        'email_preview',
        'Tipologia_Label',
        'Riferimento_Label',
        'confidence_tip',
        'confidence_rif',
        'model'
    ]].copy()
    
    display_df.columns = [
        'Data/Ora',
        'Anteprima Email',
        'Tipologia',
        'Riferimento',
        'Conf. Tip.',
        'Conf. Rif.',
        'Modello'
    ]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Statistiche
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Totale Classificazioni", len(history_df))
    
    with col2:
        avg_conf_tip = history_df['confidence_tip'].mean()
        st.metric("Avg Conf. Tipologia", f"{avg_conf_tip:.1%}")
    
    with col3:
        avg_conf_rif = history_df['confidence_rif'].mean()
        st.metric("Avg Conf. Riferimento", f"{avg_conf_rif:.1%}")
    
    with col4:
        if st.button("🗑️ Pulisci Storico", use_container_width=True):
            st.session_state.classification_history = []
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏥 <strong>Classificatore Sinistri Medical Malpractice</strong> | Powered by Groq AI</p>
    <p style="font-size: 0.9rem;">Sistema di classificazione multi-dimensionale per email medico/ospedale → compagnia assicurativa</p>
</div>
""", unsafe_allow_html=True)
