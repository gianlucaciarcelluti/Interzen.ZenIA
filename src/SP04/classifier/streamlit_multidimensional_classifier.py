"""
Classificatore Multi-Dimensionale di Email per Sinistri Medical Malpractice
Applicazione Streamlit con Logistic Regression Multi-Output
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
import warnings
import json
import os
from datetime import datetime
from pathlib import Path
warnings.filterwarnings('ignore')

# Import del dataset mock
from medical_provider_dataset import (
    create_mock_dataset,
    get_category_names
)


# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Classificatore Email Sinistri",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path al file delle correzioni manuali (nella stessa cartella dello script)
MANUAL_CORRECTIONS_FILE = Path(__file__).parent / "manual_corrections.json"


def load_manual_corrections():
    """Carica le correzioni manuali dal file JSON."""
    if MANUAL_CORRECTIONS_FILE.exists():
        with open(MANUAL_CORRECTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_manual_correction(text, tipologia, riferimento_temporale, original_prediction):
    """Salva una nuova correzione manuale nel file JSON."""
    corrections = load_manual_corrections()
    
    new_correction = {
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "tipologia": tipologia,
        "riferimento_temporale": riferimento_temporale,
        "original_prediction": original_prediction
    }
    
    corrections.append(new_correction)
    
    # Salva nel file
    MANUAL_CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MANUAL_CORRECTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(corrections, f, indent=2, ensure_ascii=False)
    
    return len(corrections)


def integrate_manual_corrections(df):
    """Integra le correzioni manuali nel dataset."""
    corrections = load_manual_corrections()
    
    if not corrections:
        return df
    
    # Converti le correzioni in DataFrame
    corrections_df = pd.DataFrame([
        {
            'testo': c['text'],
            'tipologia': c['tipologia'],
            'riferimento_temporale': c['riferimento_temporale']
        }
        for c in corrections
    ])
    
    # Aggiungi al dataset esistente
    df_combined = pd.concat([df, corrections_df], ignore_index=True)
    
    return df_combined


@st.cache_resource
def train_model():
    """
    Carica il dataset, prepara i dati e allena il modello Logistic Regression multi-output.
    Viene cachato per evitare re-training ad ogni interazione.
    
    Le correzioni manuali vengono sempre incluse nel training set per garantire
    che il modello impari immediatamente da esse.
    """
    # Carica dataset base
    df_base = create_mock_dataset()
    
    # Carica correzioni manuali separatamente
    corrections = load_manual_corrections()
    num_corrections = len(corrections)
    
    # Prepara features e target del dataset base
    X_base = df_base['testo']
    y_base = df_base[['tipologia', 'riferimento_temporale']].values
    
    # Crea label combinata per stratificazione
    df_base['combined_label'] = df_base['tipologia'].astype(str) + '_' + df_base['riferimento_temporale'].astype(str)
    
    # Split train/test SOLO sul dataset base (senza correzioni)
    X_train, X_test, y_train, y_test = train_test_split(
        X_base, y_base,
        test_size=0.2,
        random_state=42,
        stratify=df_base['combined_label']
    )
    
    # AGGIUNGI le correzioni manuali AL TRAINING SET (non al test set!)
    if num_corrections > 0:
        X_corrections = pd.Series([c['text'] for c in corrections])
        y_corrections = np.array([[c['tipologia'], c['riferimento_temporale']] for c in corrections])
        
        # Concatena con il training set
        X_train = pd.concat([X_train, X_corrections], ignore_index=True)
        y_train = np.vstack([y_train, y_corrections])
    
    # Vettorizzazione TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        min_df=2,  # Ridotto da 3 a 2 per dare più peso alle correzioni
        max_df=0.8,
        strip_accents='unicode',
        lowercase=True
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    # Training modello multi-output con parametri più flessibili per le correzioni
    lr_base = LogisticRegression(
        max_iter=1000,
        C=5.0,  # Aumentato da 1.0 a 5.0 per dare più peso alle correzioni
        random_state=42,
        solver='lbfgs',
        class_weight='balanced'  # Bilancia le classi per dare più peso agli esempi rari
    )
    model = MultiOutputClassifier(lr_base)
    model.fit(X_train_tfidf, y_train)
    
    # Ottieni nomi categorie
    category_names = get_category_names()
    
    total_dataset_size = len(df_base) + num_corrections
    
    return model, vectorizer, category_names, total_dataset_size, num_corrections


def check_context_relevance(text):
    """
    Verifica se il testo in input è pertinente al contesto di sinistri medical malpractice.
    Questo guardrail previene falsi positivi su domande/testi completamente fuori contesto.
    
    Args:
        text: Testo da verificare
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str)
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
            reason = f"Poche keyword rilevanti trovate ({keyword_count}/{min_keywords} richieste). Il testo non sembra pertinente al dominio medical malpractice."
        elif keyword_density < min_density:
            reason = f"Densità keyword troppo bassa ({keyword_density:.2%} vs {min_density:.2%} richiesto)"
        else:
            reason = "Testo non pertinente al contesto"
    else:
        reason = f"Testo pertinente al dominio ({keyword_count} keyword trovate, densità {keyword_density:.2%})"
    
    return is_relevant, confidence, reason


def get_prediction_probabilities(model, vectorizer, text):
    """
    Effettua la predizione e calcola le probabilità per entrambe le dimensioni.
    Include un guardrail per verificare la pertinenza del testo al contesto.
    
    Args:
        model: Modello multi-output trainato
        vectorizer: TF-IDF vectorizer
        text: Testo da classificare
    
    Returns:
        tuple: (predizione_tipologia, predizione_riferimento, prob_tipologia, prob_riferimento, 
                is_relevant, relevance_confidence, relevance_reason)
    """
    # GUARDRAIL: Verifica pertinenza del contesto
    is_relevant, relevance_confidence, relevance_reason = check_context_relevance(text)
    
    # Vettorizza il testo
    text_vector = vectorizer.transform([text])
    
    # Predizione
    prediction = model.predict(text_vector)[0]
    
    # Probabilità per entrambe le dimensioni
    prob_tipologia = model.estimators_[0].predict_proba(text_vector)[0]
    prob_riferimento = model.estimators_[1].predict_proba(text_vector)[0]
    
    return (prediction[0], prediction[1], prob_tipologia, prob_riferimento,
            is_relevant, relevance_confidence, relevance_reason)


def main():
    """Main function per l'applicazione Streamlit"""
    
    # Inizializza variabili di sessione
    if 'text_area' not in st.session_state:
        st.session_state.text_area = ''
    if 'classification_results' not in st.session_state:
        st.session_state.classification_results = None
    if 'current_text' not in st.session_state:
        st.session_state.current_text = ''
    
    # Header
    st.title("📧 Classificatore Multi-Dimensionale Email Sinistri")
    st.markdown("""
    Questo sistema classifica automaticamente le email su **due dimensioni indipendenti**:
    
    **Dimensione 1 - Tipologia:**
    - 🔴 **Sinistro Avvenuto**: Incidente medico già verificato con danni concreti
    - 🟡 **Circostanza Potenziale**: Situazione che potrebbe generare un sinistro futuro
    
    **Dimensione 2 - Riferimento Temporale:**
    - 🆕 **Fatto Iniziale**: Prima segnalazione del caso
    - 🔄 **Follow-up**: Aggiornamento, integrazione documentale, evoluzione del caso
    
    ---
    
    🛡️ **Guardrail Attivo**: Il sistema verifica automaticamente se il testo è pertinente al dominio 
    (sinistri medical malpractice) per **prevenire falsi positivi** su contenuti fuori contesto.
    """)
    
    st.divider()
    
    # Carica modello (cachato)
    with st.spinner("🔄 Caricamento modello..."):
        model, vectorizer, category_names, dataset_size, num_corrections = train_model()
    
    # Sidebar con informazioni
    with st.sidebar:
        st.header("ℹ️ Informazioni Modello")
        st.metric("Dataset Size", f"{dataset_size} email")
        st.metric("Correzioni Manuali", f"{num_corrections}")
        st.metric("Algoritmo", "Logistic Regression")
        st.metric("Architettura", "Multi-Output")
        
        st.divider()
        
        st.header("📋 Categorie")
        st.subheader("Tipologia")
        for cat_id, cat_name in category_names['tipologia'].items():
            icon = "🔴" if cat_id == 0 else "🟡"
            st.write(f"{icon} **{cat_id}**: {cat_name}")
        
        st.subheader("Riferimento Temporale")
        for cat_id, cat_name in category_names['riferimento_temporale'].items():
            icon = "🆕" if cat_id == 0 else "🔄"
            st.write(f"{icon} **{cat_id}**: {cat_name}")
    
    # Esempi pre-compilati
    st.header("🧪 Esempi di Test")
    
    esempi = {
        "Sinistro Avvenuto - Fatto Iniziale": "Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente. Il paziente è stato informato e richiede risarcimento. Allego documentazione clinica completa.",
        "Sinistro Avvenuto - Follow-up": "Rif. pratica SIN12345 - Dr.ssa Bianchi. Vi informo che il paziente ha presentato formale messa in mora. La famiglia ha già consultato CTP per valutazione danni. Invio documentazione integrativa richiesta dal vs perito. Chiedo aggiornamento sullo stato della pratica.",
        "Circostanza Potenziale - Fatto Iniziale": "Spett.le compagnia, Dr. Verdi, Risk Manager. Vi segnalo criticità rilevata durante audit: alcuni operatori non rispettano protocollo igiene mani. Temo possa generare infezioni nosocomiali e conseguenti richieste danni. Chiedo valutazione rischio potenziale.",
        "Circostanza Potenziale - Follow-up": "Con riferimento alla segnalazione 98765 del 10/02/2024 - Dr. Ferrari. Aggiorno che la situazione criticità igienico-sanitaria persiste nonostante le azioni correttive implementate. Gli infermieri continuano a non rispettare pienamente le procedure di lavaggio mani. Sollecito vs parere su ulteriori misure preventive da adottare."
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("📝 Esempio 1", use_container_width=True):
        st.session_state.text_area = esempi["Sinistro Avvenuto - Fatto Iniziale"]
    if col2.button("📝 Esempio 2", use_container_width=True):
        st.session_state.text_area = esempi["Sinistro Avvenuto - Follow-up"]
    if col3.button("📝 Esempio 3", use_container_width=True):
        st.session_state.text_area = esempi["Circostanza Potenziale - Fatto Iniziale"]
    if col4.button("📝 Esempio 4", use_container_width=True):
        st.session_state.text_area = esempi["Circostanza Potenziale - Follow-up"]
    
    st.divider()
    
    # Input testuale
    st.header("✍️ Inserisci il Testo da Classificare")
    
    testo_email = st.text_area(
        "Testo dell'email:",
        height=200,
        placeholder="Inserisci qui il testo dell'email da classificare...",
        key="text_area"
    )
    
    # Pulsante classificazione
    col_button1, col_button2, col_button3 = st.columns([1, 1, 3])
    
    with col_button1:
        classifica_button = st.button("🚀 Classifica", type="primary", use_container_width=True)
    
    with col_button2:
        if st.button("🗑️ Pulisci", use_container_width=True):
            st.session_state.text_area = ''
            st.session_state.classification_results = None
            st.session_state.current_text = ''
            st.rerun()
    
    # Classificazione
    if classifica_button and testo_email and testo_email.strip():
        with st.spinner("🔍 Classificazione in corso..."):
            # Ottieni predizioni con guardrail
            pred_tip, pred_rif, prob_tip, prob_rif, is_relevant, relevance_conf, relevance_reason = get_prediction_probabilities(
                model, vectorizer, testo_email
            )
            
            # Salva i risultati nello stato della sessione
            st.session_state.classification_results = {
                'pred_tip': pred_tip,
                'pred_rif': pred_rif,
                'prob_tip': prob_tip,
                'prob_rif': prob_rif,
                'dataset_size': dataset_size,
                'num_corrections': num_corrections,
                'is_relevant': is_relevant,
                'relevance_confidence': relevance_conf,
                'relevance_reason': relevance_reason
            }
            st.session_state.current_text = testo_email
    
    # Mostra i risultati se esistono (anche dopo re-run)
    if st.session_state.classification_results is not None:
        results = st.session_state.classification_results
        pred_tip = results['pred_tip']
        pred_rif = results['pred_rif']
        prob_tip = results['prob_tip']
        prob_rif = results['prob_rif']
        dataset_size = results['dataset_size']
        num_corrections = results['num_corrections']
        is_relevant = results.get('is_relevant', True)
        relevance_conf = results.get('relevance_confidence', 1.0)
        relevance_reason = results.get('relevance_reason', 'N/A')
        testo_email = st.session_state.current_text
        
        # GUARDRAIL: Mostra avviso se testo non pertinente
        if not is_relevant:
            st.error("🚫 **ATTENZIONE: Testo Fuori Contesto!**")
            st.warning(f"""
            **Il testo inserito non sembra pertinente al dominio di classificazione (sinistri medical malpractice).**
            
            **Motivo:** {relevance_reason}
            
            **Confidenza di pertinenza:** {relevance_conf:.1%}
            
            ⚠️ **La classificazione potrebbe essere un FALSO POSITIVO.** 
            Si raccomanda di inserire testi relativi a:
            - Sinistri medici
            - Segnalazioni di eventi avversi
            - Richieste di risarcimento
            - Follow-up di pratiche assicurative sanitarie
            """)
            st.divider()
        else:
            # Mostra badge di pertinenza
            st.success(f"✅ Testo pertinente al dominio (confidenza: {relevance_conf:.1%})")
            with st.expander("ℹ️ Dettaglio verifica pertinenza"):
                st.info(relevance_reason)
        
        # Risultati
        st.success("✅ Classificazione completata!")
        
        st.divider()
        
        # Layout a due colonne per i risultati
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 Dimensione 1: Tipologia")
            
            categoria_tip = category_names['tipologia'][pred_tip]
            icon_tip = "🔴" if pred_tip == 0 else "🟡"
            confidenza_tip = prob_tip[pred_tip] * 100
            
            st.markdown(f"### {icon_tip} {categoria_tip}")
            st.metric("Confidenza", f"{confidenza_tip:.2f}%")
            
            # Progress bar
            st.progress(prob_tip[pred_tip])
            
            # Dettaglio probabilità
            with st.expander("📈 Dettaglio Probabilità Tipologia"):
                df_prob_tip = pd.DataFrame({
                    'Categoria': [category_names['tipologia'][0], category_names['tipologia'][1]],
                    'Probabilità (%)': [prob_tip[0] * 100, prob_tip[1] * 100]
                })
                st.dataframe(df_prob_tip, use_container_width=True, hide_index=True)
                st.bar_chart(df_prob_tip.set_index('Categoria'))
        
        with col_right:
            st.subheader("⏰ Dimensione 2: Riferimento Temporale")
            
            categoria_rif = category_names['riferimento_temporale'][pred_rif]
            icon_rif = "🆕" if pred_rif == 0 else "🔄"
            confidenza_rif = prob_rif[pred_rif] * 100
            
            st.markdown(f"### {icon_rif} {categoria_rif}")
            st.metric("Confidenza", f"{confidenza_rif:.2f}%")
            
            # Progress bar
            st.progress(prob_rif[pred_rif])
            
            # Dettaglio probabilità
            with st.expander("📈 Dettaglio Probabilità Riferimento"):
                df_prob_rif = pd.DataFrame({
                    'Categoria': [category_names['riferimento_temporale'][0], 
                                 category_names['riferimento_temporale'][1]],
                    'Probabilità (%)': [prob_rif[0] * 100, prob_rif[1] * 100]
                })
                st.dataframe(df_prob_rif, use_container_width=True, hide_index=True)
                st.bar_chart(df_prob_rif.set_index('Categoria'))
        
        st.divider()
        
        # Riepilogo finale
        st.subheader("📋 Riepilogo Classificazione")
        
        # Confidenza media
        confidenza_media = (confidenza_tip + confidenza_rif) / 2
        
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        
        with col_summary1:
            st.metric("Tipologia", categoria_tip, f"{confidenza_tip:.1f}%")
        
        with col_summary2:
            st.metric("Riferimento", categoria_rif, f"{confidenza_rif:.1f}%")
        
        with col_summary3:
            st.metric("Confidenza Media", f"{confidenza_media:.1f}%")
        
        # Alert per bassa confidenza
        if not is_relevant:
            st.error("🚫 **TESTO FUORI CONTESTO**: La classificazione è probabilmente un falso positivo. Ignorare i risultati.")
        elif confidenza_media < 70:
            st.warning("⚠️ **Attenzione**: Confidenza media bassa. Si raccomanda revisione manuale.")
        elif confidenza_media >= 90:
            st.success("✅ **Eccellente**: Alta confidenza nella classificazione.")
        
        # Informazioni aggiuntive
        with st.expander("ℹ️ Informazioni Aggiuntive"):
            st.write("**Caratteristiche del testo analizzato:**")
            st.write(f"- Lunghezza: {len(testo_email or '')} caratteri")
            st.write(f"- Numero parole: {len((testo_email or '').split())} parole")
            st.write(f"- **Pertinenza al dominio: {'✅ SÌ' if is_relevant else '❌ NO'} ({relevance_conf:.1%})**")
            st.write(f"- Motivazione pertinenza: {relevance_reason}")
            st.write("- Modello: Logistic Regression Multi-Output")
            st.write("- Features utilizzate: TF-IDF (1000 features, n-gram 1-2)")
            st.write("- **Guardrail attivo**: Verifica pertinenza contesto")
        
        # Sezione correzione manuale
        st.divider()
        st.subheader("🔧 Correzione Manuale della Classificazione")
        
        with st.expander("✏️ Correggi la classificazione e ri-addestra il modello", expanded=True):
            st.info("""
            **💡 Come funziona:**
            1. Seleziona le classificazioni corrette qui sotto
            2. Clicca sul pulsante per salvare e ri-addestrare
            3. Visualizza il confronto prima/dopo con le nuove metriche
            """)
            
            col_correct1, col_correct2 = st.columns(2)
            
            with col_correct1:
                st.write("**Tipologia corretta:**")
                tipologia_corretta = st.radio(
                    "Seleziona la tipologia corretta:",
                    options=[0, 1],
                    format_func=lambda x: f"{category_names['tipologia'][x]} ({'🔴' if x == 0 else '🟡'})",
                    index=int(pred_tip),
                    key="tipologia_correction"
                )
            
            with col_correct2:
                st.write("**Riferimento temporale corretto:**")
                riferimento_corretto = st.radio(
                    "Seleziona il riferimento temporale corretto:",
                    options=[0, 1],
                    format_func=lambda x: f"{category_names['riferimento_temporale'][x]} ({'🆕' if x == 0 else '🔄'})",
                    index=int(pred_rif),
                    key="riferimento_correction"
                )
            
            st.divider()
            
            # Mostra se ci sono differenze
            has_changes = (tipologia_corretta != pred_tip) or (riferimento_corretto != pred_rif)
            
            if has_changes:
                st.success("✅ Hai modificato la classificazione originale - Pronto per il salvataggio!")
                
                # Mostra le differenze
                col_diff1, col_diff2 = st.columns(2)
                
                with col_diff1:
                    if tipologia_corretta != pred_tip:
                        st.write("**Tipologia:**")
                        st.write(f"❌ Prima: {category_names['tipologia'][pred_tip]}")
                        st.write(f"✅ Dopo: {category_names['tipologia'][tipologia_corretta]}")
                
                with col_diff2:
                    if riferimento_corretto != pred_rif:
                        st.write("**Riferimento Temporale:**")
                        st.write(f"❌ Prima: {category_names['riferimento_temporale'][pred_rif]}")
                        st.write(f"✅ Dopo: {category_names['riferimento_temporale'][riferimento_corretto]}")
            else:
                st.warning("⚠️ Nessuna modifica rilevata. Seleziona valori diversi per abilitare il salvataggio.")
            
            st.divider()
            
            # Pulsante più evidente
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
            with col_btn2:
                save_button = st.button(
                    "💾 SALVA E RI-ADDESTRA",
                    type="primary",
                    disabled=not has_changes,
                    use_container_width=True,
                    help="Salva la correzione, ri-addestra il modello e mostra il confronto"
                )
            
            if save_button and has_changes:
                        # Salva la predizione originale
                        original_prediction = {
                            "tipologia": int(pred_tip),
                            "riferimento_temporale": int(pred_rif),
                            "confidenza_tipologia": float(prob_tip[pred_tip]),
                            "confidenza_riferimento": float(prob_rif[pred_rif])
                        }
                        
                        # Salva la correzione
                        num_total_corrections = save_manual_correction(
                            testo_email,
                            int(tipologia_corretta),
                            int(riferimento_corretto),
                            original_prediction
                        )
                        
                        st.success(f"✅ Correzione salvata! Totale correzioni: {num_total_corrections}")
                        
                        # Clear cache e ri-addestra
                        st.cache_resource.clear()
                        
                        st.info("🔄 Re-training del modello in corso...")
                        
                        # Ri-carica il modello con le nuove correzioni
                        new_model, new_vectorizer, _, new_dataset_size, new_num_corrections = train_model()
                        
                        # Riesegui la predizione con il nuovo modello
                        new_pred_tip, new_pred_rif, new_prob_tip, new_prob_rif, new_is_rel, new_rel_conf, new_rel_reason = get_prediction_probabilities(
                            new_model, new_vectorizer, testo_email
                        )
                        
                        st.success("✅ Modello ri-addestrato con successo!")
                        
                        st.info("""
                        💡 **Nota sul Re-training:**
                        - La tua correzione è stata aggiunta DIRETTAMENTE al training set
                        - Il modello ha parametri ottimizzati per dare più peso alle correzioni manuali
                        - Con Logistic Regression, potrebbero servire più esempi simili per un cambiamento significativo
                        """)
                        
                        # Mostra le differenze
                        st.divider()
                        st.subheader("📊 Confronto Prima/Dopo il Re-training")
                        
                        col_before, col_after = st.columns(2)
                        
                        with col_before:
                            st.write("**🔴 PRIMA del Re-training**")
                            st.metric("Dataset Size", f"{dataset_size} email")
                            st.metric("Correzioni Manuali", f"{num_corrections}")
                            
                            st.write("**Predizione:**")
                            st.write(f"- Tipologia: {category_names['tipologia'][pred_tip]} ({prob_tip[pred_tip]*100:.2f}%)")
                            st.write(f"- Riferimento: {category_names['riferimento_temporale'][pred_rif]} ({prob_rif[pred_rif]*100:.2f}%)")
                        
                        with col_after:
                            st.write("**🟢 DOPO il Re-training**")
                            st.metric("Dataset Size", f"{new_dataset_size} email", delta=f"+{new_dataset_size - dataset_size}")
                            st.metric("Correzioni Manuali", f"{new_num_corrections}", delta=f"+{new_num_corrections - num_corrections}")
                            
                            st.write("**Predizione:**")
                            st.write(f"- Tipologia: {category_names['tipologia'][new_pred_tip]} ({new_prob_tip[new_pred_tip]*100:.2f}%)")
                            st.write(f"- Riferimento: {category_names['riferimento_temporale'][new_pred_rif]} ({new_prob_rif[new_pred_rif]*100:.2f}%)")
                        
                        # Analisi dei cambiamenti
                        st.divider()
                        st.write("**📈 Analisi dei Cambiamenti:**")
                        
                        # Cambiamento tipologia
                        if new_pred_tip != pred_tip:
                            st.write(f"✅ Tipologia cambiata: {category_names['tipologia'][pred_tip]} → {category_names['tipologia'][new_pred_tip]}")
                        else:
                            st.write(f"➡️ Tipologia invariata: {category_names['tipologia'][pred_tip]}")
                        
                        delta_conf_tip = (new_prob_tip[new_pred_tip] - prob_tip[pred_tip]) * 100
                        st.write(f"   Δ Confidenza Tipologia: {delta_conf_tip:+.2f}%")
                        
                        # Cambiamento riferimento
                        if new_pred_rif != pred_rif:
                            st.write(f"✅ Riferimento cambiato: {category_names['riferimento_temporale'][pred_rif]} → {category_names['riferimento_temporale'][new_pred_rif]}")
                        else:
                            st.write(f"➡️ Riferimento invariato: {category_names['riferimento_temporale'][pred_rif]}")
                        
                        delta_conf_rif = (new_prob_rif[new_pred_rif] - prob_rif[pred_rif]) * 100
                        st.write(f"   Δ Confidenza Riferimento: {delta_conf_rif:+.2f}%")
                        
                        # Suggerisci di ricaricare la pagina
                        st.info("💡 **Per continuare a usare il modello aggiornato, ricarica la pagina (F5).**")
    
    elif classifica_button and (not testo_email or not testo_email.strip()):
        st.error("❌ Per favore inserisci un testo da classificare.")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        📧 Classificatore Multi-Dimensionale Email Sinistri Medical Malpractice<br>
        Powered by Scikit-learn & Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
