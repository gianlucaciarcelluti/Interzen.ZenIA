"""
Guardrail Ibrido per SP00 - Procedural Classifier
Sistema a 2 livelli per verificare pertinenza delle istanze al dominio PA
"""

from typing import Tuple, Optional
import json
import time


def check_context_relevance_basic(text: str) -> Tuple[bool, float, str, int]:
    """
    Verifica VELOCE basata su keyword per filtrare casi ovvi.
    Livello 1 del guardrail (gratuito e istantaneo).
    
    Args:
        text: Testo da verificare
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str, keyword_count: int)
    """
    text_lower = text.lower()
    
    # Termini chiave che indicano pertinenza al dominio PA
    domain_keywords = {
        # Termini amministrativi generali
        'comune', 'provincia', 'regione', 'ente', 'pubblica amministrazione', 'pa',
        'amministrazione', 'ufficio', 'settore', 'dirigente', 'assessore', 'sindaco',
        'giunta', 'consiglio', 'delibera', 'determinazione', 'ordinanza', 'decreto',
        
        # Termini procedurali
        'istanza', 'richiesta', 'domanda', 'procedimento', 'provvedimento', 'autorizzazione',
        'concessione', 'permesso', 'licenza', 'nulla osta', 'parere', 'certificato',
        'scia', 'dia', 'cila', 'comunicazione', 'segnalazione',
        
        # Normativa e diritto
        'legge', 'decreto legislativo', 'd.lgs', 'dpr', 'legge regionale', 'l.r.',
        'regolamento', 'normativa', 'disposizione', 'articolo', 'comma',
        
        # Ambiente
        'ambiente', 'ambientale', 'via', 'vas', 'aia', 'scarico', 'emissioni',
        'rifiuti', 'bonifiche', 'inquinamento', 'ecologia', 'tutela acque',
        
        # Urbanistica
        'urbanistica', 'edilizia', 'costruire', 'edificare', 'fabbricato', 'immobile',
        'piano regolatore', 'prg', 'variante', 'zonizzazione', 'destinazione urbanistica',
        'vincolo paesaggistico', 'vincolo', 'lottizzazione',
        
        # Commercio
        'commercio', 'commerciale', 'esercizio', 'attività economica', 'impresa',
        'partita iva', 'iscrizione', 'camera di commercio', 'suap',
        'occupazione suolo', 'plateatico', 'dehors',
        
        # Sociale
        'sociale', 'assistenza', 'servizi sociali', 'contributo', 'sussidio',
        'alloggio', 'erp', 'edilizia residenziale', 'casa popolare',
        
        # Mobilità
        'mobilità', 'traffico', 'viabilità', 'circolazione', 'sosta', 'parcheggio',
        'ztl', 'zona traffico limitato', 'trasporto', 'strada',
        
        # Cultura/Eventi
        'cultura', 'culturale', 'patrocinio', 'evento', 'manifestazione', 'spettacolo',
        'museo', 'biblioteca', 'teatro'
    }
    
    # Conta keyword presenti
    keyword_count = sum(1 for keyword in domain_keywords if keyword in text_lower)
    
    # Calcola densità keyword
    word_count = len(text.split())
    keyword_density = keyword_count / max(word_count, 1)
    
    # Criteri di pertinenza
    min_keywords = 2  # Almeno 2 keyword nel dominio PA
    min_density = 0.03  # Almeno 3% delle parole devono essere keyword
    min_length = 20  # Almeno 20 caratteri
    
    # Verifica pertinenza
    is_relevant = (
        keyword_count >= min_keywords and
        keyword_density >= min_density and
        len(text.strip()) >= min_length
    )
    
    # Calcola confidenza (0-1)
    confidence = min(1.0, (keyword_count / 5) * (keyword_density / 0.05))
    
    # Genera ragione
    if not is_relevant:
        if len(text.strip()) < min_length:
            reason = f"Testo troppo breve ({len(text.strip())} caratteri, minimo {min_length})"
        elif keyword_count < min_keywords:
            reason = f"Poche keyword PA trovate ({keyword_count}/{min_keywords} richieste)"
        elif keyword_density < min_density:
            reason = f"Densità keyword troppo bassa ({keyword_density:.2%} vs {min_density:.2%} richiesto)"
        else:
            reason = "Testo non pertinente al contesto PA"
    else:
        reason = f"Keyword check: {keyword_count} keyword PA trovate, densità {keyword_density:.2%}"
    
    return is_relevant, confidence, reason, keyword_count


def check_context_relevance_llm(
    text: str, 
    api_key: str, 
    model: str = "llama-3.3-70b-versatile"
) -> Tuple[Optional[bool], float, str, str]:
    """
    Verifica AVANZATA usando LLM per casi borderline.
    Livello 2 del guardrail (a pagamento ma molto accurato).
    
    Args:
        text: Testo da verificare
        api_key: API key di Groq
        model: Modello LLM da usare
    
    Returns:
        tuple: (is_relevant: bool, confidence: float, reason: str, llm_analysis: str)
    """
    from groq import Groq
    
    try:
        client = Groq(api_key=api_key)
        
        # Prompt ottimizzato per verifica pertinenza PA
        system_prompt = """Sei un esperto analizzatore di testi per il dominio della Pubblica Amministrazione italiana.

Il tuo compito è determinare se un testo è PERTINENTE al dominio dei procedimenti amministrativi.

Un testo è PERTINENTE se riguarda:
- Istanze/richieste di cittadini o aziende verso la PA
- Procedimenti amministrativi (autorizzazioni, permessi, licenze, ecc.)
- Provvedimenti amministrativi (delibere, determinazioni, ordinanze, ecc.)
- Richieste di certificati o documenti amministrativi
- Comunicazioni verso enti pubblici (Comune, Provincia, Regione, ecc.)
- Materie amministrative (ambiente, urbanistica, commercio, sociale, mobilità, cultura)

Un testo è NON PERTINENTE se:
- È una domanda generica non collegata alla PA
- Riguarda argomenti completamente diversi (sport, cucina, tecnologia, ecc.)
- È una conversazione casuale
- Non ha nessun collegamento con procedimenti amministrativi

Rispondi in formato JSON con questa struttura:
{
    "is_relevant": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "spiegazione dettagliata del perché",
    "domain_match": "quale aspetto del dominio PA corrisponde (se pertinente)",
    "suggested_category": "categoria PA suggerita se pertinente (AMBIENTE, URBANISTICA, COMMERCIO, ecc.)"
}

Sii RIGOROSO: solo testi chiaramente legati a procedimenti amministrativi sono pertinenti."""

        user_prompt = f"""Analizza questo testo e determina se è pertinente al dominio procedimenti amministrativi PA:

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
            temperature=0.1,
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
        suggested_category = result.get('suggested_category', 'N/A')
        
        # Costruisci analisi dettagliata
        token_count = response.usage.total_tokens if response.usage else 0
        llm_analysis = f"""**Analisi LLM ({model}):**
- Pertinente: {'✅ SÌ' if is_relevant else '❌ NO'}
- Confidenza: {confidence:.1%}
- Ragionamento: {reasoning}
- Match dominio: {domain_match}
- Categoria suggerita: {suggested_category}
- Latenza: {latency:.2f}s
- Token usati: {token_count}"""
        
        reason = f"LLM Analysis: {reasoning[:100]}..." if len(reasoning) > 100 else f"LLM Analysis: {reasoning}"
        
        return is_relevant, confidence, reason, llm_analysis
        
    except Exception as e:
        # Fallback in caso di errore LLM
        return None, 0.5, f"Errore LLM: {str(e)}", f"⚠️ Errore durante verifica LLM: {str(e)}"


def check_context_relevance(
    text: str, 
    api_key: str = "", 
    model: str = "llama-3.3-70b-versatile", 
    use_llm_for_borderline: bool = False
) -> Tuple[bool, float, str, str, Optional[str]]:
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
        reason_final = f"{reason_kw} [Keyword PA: {keyword_count}]"
        
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


# ============================================================================
# FUNZIONI DI UTILITÀ
# ============================================================================

def get_guardrail_recommendation(is_relevant: bool, confidence: float) -> str:
    """
    Genera raccomandazione basata su risultato guardrail
    
    Args:
        is_relevant: Se il testo è pertinente
        confidence: Confidenza della verifica
    
    Returns:
        Raccomandazione testuale
    """
    if not is_relevant:
        return "🚫 TESTO FUORI CONTESTO - Non procedere con classificazione"
    elif confidence >= 0.8:
        return "✅ Testo pertinente al dominio PA - Procedere con classificazione"
    elif confidence >= 0.6:
        return "⚠️ Pertinenza probabile ma da verificare - Classificazione con cautela"
    else:
        return "❌ Bassa confidenza di pertinenza - Revisione manuale raccomandata"


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 80)
    print("🛡️ TEST GUARDRAIL PERTINENZA SP00")
    print("=" * 80)
    
    # Test cases
    test_cases = [
        {
            "name": "Istanza PA Valida - Ambiente",
            "text": "Spettabile Comune, richiedo autorizzazione scarico acque reflue industriali",
            "expected": True
        },
        {
            "name": "Istanza PA Valida - Urbanistica",
            "text": "Il sottoscritto chiede permesso di costruire per villetta unifamiliare",
            "expected": True
        },
        {
            "name": "Testo Fuori Contesto",
            "text": "Che tempo fa oggi? Mi consigli una ricetta per la pasta?",
            "expected": False
        },
        {
            "name": "Borderline - Contiene keyword ma non PA",
            "text": "L'autorizzazione dei genitori è necessaria per la gita scolastica",
            "expected": False
        },
        {
            "name": "Testo Troppo Breve",
            "text": "Ciao",
            "expected": False
        }
    ]
    
    print("\n🧪 TEST LIVELLO 1 (Keyword-based):")
    print("-" * 80)
    
    for i, test in enumerate(test_cases, 1):
        is_rel, conf, reason, kw_count = check_context_relevance_basic(test["text"])
        
        status = "✅" if is_rel == test["expected"] else "❌"
        print(f"\n{i}. {status} {test['name']}")
        print(f"   Pertinente: {is_rel} (atteso: {test['expected']})")
        print(f"   Confidence: {conf:.2f}")
        print(f"   Keyword: {kw_count}")
        print(f"   Motivo: {reason}")
    
    print("\n" + "=" * 80)
    print("✅ Test completati!")
    print("\n💡 Per testare con LLM, usa:")
    print("   check_context_relevance(text, api_key='your-key', use_llm_for_borderline=True)")
