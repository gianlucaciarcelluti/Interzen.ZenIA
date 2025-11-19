"""
Test per il guardrail IBRIDO (Keyword + LLM) nel classificatore Groq.

Questo test verifica il sistema a due livelli:
- Livello 1: Keyword-based (veloce, gratuito)
- Livello 2: LLM-based (accurato, a pagamento, solo casi borderline)
"""

import sys
import os
from pathlib import Path

# Aggiungi il percorso del modulo al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "SP04" / "llm_classifier"))

from SP04.llm_classifier.streamlit_groq_classifier import check_context_relevance_basic, check_context_relevance


def test_livello1_keyword():
    """Test del livello 1 (keyword-based)"""
    
    print("=" * 80)
    print("TEST LIVELLO 1 - GUARDRAIL KEYWORD (Veloce, Gratuito)")
    print("=" * 80)
    
    # Casi ovviamente pertinenti (alta confidenza)
    testi_pertinenti = [
        """Spett.le Compagnia, segnalo evento avverso durante intervento chirurgico. 
        Paziente richiede risarcimento danni. Allego documentazione medica.""",
        
        """Rif. pratica SIN12345. Il perito ha confermato nesso causale tra errore medico 
        e lesione del paziente. Follow-up richiesta risarcitoria."""
    ]
    
    # Casi ovviamente NON pertinenti (confidenza zero)
    testi_fuori_contesto = [
        "Che tempo fa oggi?",
        "La ricetta della pizza margherita è semplice.",
        "Ciao"
    ]
    
    print("\n✅ TEST TESTI PERTINENTI (alta confidenza keyword):")
    for i, testo in enumerate(testi_pertinenti, 1):
        is_rel, conf, reason, kw_count = check_context_relevance_basic(testo)
        print(f"\n[Test {i}]")
        print(f"Testo (50 char): {testo[:50]}...")
        print(f"Pertinente: {is_rel}")
        print(f"Confidenza: {conf:.1%}")
        print(f"Keyword: {kw_count}")
        print(f"Reason: {reason}")
        
        assert is_rel, f"Test {i} FALLITO: dovrebbe essere pertinente"
        assert conf >= 0.7, f"Test {i} FALLITO: confidenza troppo bassa"
        print(f"✅ Test {i} SUPERATO")
    
    print("\n\n❌ TEST TESTI FUORI CONTESTO (confidenza zero):")
    for i, testo in enumerate(testi_fuori_contesto, 1):
        is_rel, conf, reason, kw_count = check_context_relevance_basic(testo)
        print(f"\n[Test {i}]")
        print(f"Testo: {testo}")
        print(f"Pertinente: {is_rel}")
        print(f"Confidenza: {conf:.1%}")
        print(f"Keyword: {kw_count}")
        print(f"Reason: {reason}")
        
        assert not is_rel, f"Test {i} FALLITO: NON dovrebbe essere pertinente"
        print(f"✅ Test {i} SUPERATO")


def test_livello2_llm():
    """Test del livello 2 (LLM-based) su casi borderline"""
    
    print("\n\n" + "=" * 80)
    print("TEST LIVELLO 2 - GUARDRAIL LLM (Accurato, Opzionale)")
    print("=" * 80)
    
    # Verifica API key
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    if not api_key:
        print("\n⚠️ GROQ_API_KEY non trovata nelle variabili d'ambiente")
        print("⚠️ Test LLM SALTATO (richiede API key)")
        return
    
    # Casi borderline (confidenza media con keyword)
    testi_borderline = [
        # Caso 1: Keyword mediche ma contesto turistico
        """Il dottore mi ha consigliato di andare in vacanza al mare. 
        L'ospedale più vicino alla spiaggia è molto carino e moderno.""",
        
        # Caso 2: Keyword mediche ma contesto generico (non malpractice)
        """Il paziente è stato visitato in ambulatorio. La diagnosi è stata confermata 
        con esami di laboratorio. La terapia prescritta include farmaci.""",
    ]
    
    print(f"\n🧠 Usando API Groq con chiave: {api_key[:10]}...")
    
    for i, testo in enumerate(testi_borderline, 1):
        print(f"\n\n{'='*60}")
        print(f"[Caso Borderline {i}]")
        print(f"Testo: {testo[:80]}...")
        print(f"{'='*60}")
        
        # Prima: verifica keyword
        is_rel_kw, conf_kw, _reason_kw, kw_count = check_context_relevance_basic(testo)
        print("\n📊 LIVELLO 1 (Keyword):")
        print(f"  Pertinente: {is_rel_kw}")
        print(f"  Confidenza: {conf_kw:.1%}")
        print(f"  Keyword trovate: {kw_count}")
        
        # Poi: verifica completa (keyword + LLM se borderline)
        is_rel, conf, reason, method, llm_analysis = check_context_relevance(
            testo,
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            use_llm_for_borderline=True
        )
        
        print("\n🛡️ GUARDRAIL COMPLETO (Keyword + LLM):")
        print(f"  Pertinente: {is_rel}")
        print(f"  Confidenza: {conf:.1%}")
        print(f"  Metodo: {method}")
        print(f"  Reason: {reason[:100]}...")
        
        if llm_analysis:
            print("\n🧠 ANALISI LLM:")
            print(llm_analysis)
            print("✅ LLM è stato utilizzato per caso borderline")
        else:
            print("⚠️ LLM NON utilizzato (confidenza keyword era già chiara)")
        
        print(f"\n✅ Caso {i} completato")


def test_efficienza_ibrida():
    """Test che il sistema ibrido sia efficiente (usa LLM solo quando serve)"""
    
    print("\n\n" + "=" * 80)
    print("TEST EFFICIENZA - Verifica Uso Ottimale LLM")
    print("=" * 80)
    
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    if not api_key:
        print("\n⚠️ Test saltato (richiede API key)")
        return
    
    test_cases = [
        ("Ovviamente pertinente", "Sinistro medico con risarcimento richiesto dal paziente", True),
        ("Ovviamente NON pertinente", "Che tempo fa?", False),
        ("Borderline medico", "Il dottore mi ha visitato ieri. Tutto bene.", None),  # None = potrebbe andare in entrambi i modi
    ]
    
    for nome, testo, expected_llm_used in test_cases:
        print(f"\n[{nome}]")
        print(f"Testo: {testo}")
        
        _is_rel, conf, _reason, method, llm_analysis = check_context_relevance(
            testo,
            api_key=api_key,
            use_llm_for_borderline=True
        )
        
        llm_used = llm_analysis is not None
        
        print(f"Metodo: {method}")
        print(f"LLM usato: {'✅ Sì' if llm_used else '❌ No'}")
        
        # Verifica efficienza
        if expected_llm_used == True:
            # Dovrebbe usare LLM (borderline)
            if "livello 1+2" not in method:
                print("⚠️ NOTA: Caso borderline ma LLM non usato (probabilmente confidenza keyword era chiara)")
        elif expected_llm_used == False:
            # NON dovrebbe usare LLM (caso ovvio)
            assert "livello 1" in method and "livello 1+2" not in method, \
                "INEFFICIENTE: LLM usato per caso ovvio!"
            print("✅ Efficiente: LLM non usato per caso ovvio")
        
        print(f"Confidenza: {conf:.1%}")


def test_performance():
    """Test performance del guardrail ibrido"""
    import time
    
    print("\n\n" + "=" * 80)
    print("TEST PERFORMANCE")
    print("=" * 80)
    
    # Test solo livello 1 (keyword)
    testo_test = """Spett.le Compagnia, segnalo evento avverso. Paziente richiede risarcimento."""
    
    num_iterations = 1000
    
    print(f"\n📊 Test Livello 1 (Keyword) - {num_iterations} iterazioni:")
    start_time = time.time()
    for _ in range(num_iterations):
        check_context_relevance_basic(testo_test)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = (total_time / num_iterations) * 1000
    
    print(f"  Tempo totale: {total_time:.4f}s")
    print(f"  Tempo medio: {avg_time:.4f}ms")
    print(f"  Throughput: {num_iterations / total_time:.2f} verifiche/sec")
    
    assert avg_time < 1, f"Performance insufficiente: {avg_time:.4f}ms > 1ms"
    print("  ✅ Performance eccellente")


if __name__ == "__main__":
    print("\n🚀 AVVIO TEST GUARDRAIL IBRIDO (Keyword + LLM)\n")
    
    try:
        test_livello1_keyword()
        test_livello2_llm()
        test_efficienza_ibrida()
        test_performance()
        
        print("\n\n" + "=" * 80)
        print("✅ TUTTI I TEST COMPLETATI!")
        print("=" * 80)
        print("\n💡 Il guardrail ibrido è operativo:")
        print("   - Livello 1: Keyword (veloce, gratuito, sempre attivo)")
        print("   - Livello 2: LLM (accurato, opzionale, solo casi borderline)")
        print("\n🚀 Avvia l'app con: streamlit run streamlit_groq_classifier.py")
        
    except AssertionError as e:
        print(f"\n\n❌ TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
