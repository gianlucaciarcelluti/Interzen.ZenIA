"""
Test per verificare il funzionamento del guardrail di pertinenza del contesto
nel classificatore Groq LLM per sinistri medical malpractice.
"""

import sys
from pathlib import Path

# Aggiungi il percorso del modulo al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "SP04" / "llm_classifier"))

from streamlit_groq_classifier import check_context_relevance


def test_testi_pertinenti():
    """Testa che testi pertinenti vengano riconosciuti correttamente"""
    
    testi_pertinenti = [
        # Sinistro medico chiaro
        """Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso 
        verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico 
        al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente.""",
        
        # Follow-up assicurativo
        """Rif. pratica SIN234567 - Dr. Bianchi. Invio documentazione medica integrativa 
        richiesta dal vs perito. Allego referto specialistico che conferma nesso causale.""",
        
        # Near miss
        """Dr.ssa Verdi, responsabile Qualità. Segnalo near miss verificatosi: infermiere 
        ha preparato farmaco per paziente sbagliato ma errore intercettato prima della somministrazione.""",
        
        # Richiesta risarcimento
        """Egregio Direttore, familiare del paziente ricoverato in clinica. A seguito di 
        grave negligenza medica durante la degenza, richiediamo risarcimento danni."""
    ]
    
    print("=" * 80)
    print("TEST TESTI PERTINENTI AL DOMINIO - CLASSIFICATORE GROQ")
    print("=" * 80)
    
    for i, testo in enumerate(testi_pertinenti, 1):
        is_relevant, confidence, reason = check_context_relevance(testo)
        
        print(f"\n[Test {i}]")
        print(f"Testo (prime 100 char): {testo[:100]}...")
        print(f"✅ Pertinente: {is_relevant}")
        print(f"📊 Confidenza: {confidence:.2%}")
        print(f"💡 Motivo: {reason}")
        
        # Asserzione: deve essere pertinente
        assert is_relevant, f"Test {i} FALLITO: testo pertinente non riconosciuto!"
        print(f"✅ Test {i} SUPERATO")


def test_testi_fuori_contesto():
    """Testa che testi fuori contesto vengano identificati correttamente"""
    
    testi_fuori_contesto = [
        # Domande generiche
        "Come posso migliorare la mia produttività?",
        "Qual è la capitale della Francia?",
        
        # Conversazioni
        "Buongiorno, tutto bene? Ci vediamo domani?",
        
        # Altri argomenti
        "Il Milan ha vinto lo scudetto nel 2022. Grande partita!",
        "La ricetta della carbonara: guanciale, uova, pecorino, pepe nero.",
        "Il nuovo iPhone 15 ha caratteristiche innovative.",
        
        # Codice
        "function hello() { console.log('Hello World'); }",
        
        # Testi brevi
        "Ok",
        "Grazie",
        "Ciao"
    ]
    
    print("\n\n" + "=" * 80)
    print("TEST TESTI FUORI CONTESTO - CLASSIFICATORE GROQ")
    print("=" * 80)
    
    for i, testo in enumerate(testi_fuori_contesto, 1):
        is_relevant, confidence, reason = check_context_relevance(testo)
        
        print(f"\n[Test {i}]")
        print(f"Testo: {testo[:100]}")
        print(f"❌ Pertinente: {is_relevant}")
        print(f"📊 Confidenza: {confidence:.2%}")
        print(f"💡 Motivo: {reason}")
        
        # Asserzione: NON deve essere pertinente
        assert not is_relevant, f"Test {i} FALLITO: testo fuori contesto riconosciuto come pertinente!"
        print(f"✅ Test {i} SUPERATO")


def test_casi_borderline():
    """Testa casi borderline che potrebbero essere ambigui"""
    
    print("\n\n" + "=" * 80)
    print("TEST CASI BORDERLINE - CLASSIFICATORE GROQ")
    print("=" * 80)
    
    # Caso 1: Keyword mediche ma contesto non assicurativo
    testo1 = """Il paziente è stato dimesso dall'ospedale dopo l'intervento chirurgico. 
    Il medico ha confermato che la terapia farmacologica è stata efficace."""
    
    is_rel, conf, reason = check_context_relevance(testo1)
    print(f"\n[Caso Borderline 1 - Testo medico generico senza riferimento sinistri]")
    print(f"Testo: {testo1}")
    print(f"Pertinente: {is_rel}")
    print(f"Confidenza: {conf:.2%}")
    print(f"Motivo: {reason}")
    print("Note: Potrebbe essere accettato (keyword mediche presenti)")
    
    # Caso 2: Email generica con minimo contesto medico
    testo2 = """Caro dottore, grazie per l'appuntamento di ieri. 
    L'ospedale è molto carino. A presto!"""
    
    is_rel, conf, reason = check_context_relevance(testo2)
    print(f"\n[Caso Borderline 2 - Email informale con poche keyword]")
    print(f"Testo: {testo2}")
    print(f"Pertinente: {is_rel}")
    print(f"Confidenza: {conf:.2%}")
    print(f"Motivo: {reason}")
    print("Note: Densità keyword probabilmente troppo bassa")


def test_esempi_applicazione():
    """Testa gli esempi usati nell'applicazione Streamlit"""
    
    print("\n\n" + "=" * 80)
    print("TEST ESEMPI APPLICAZIONE - CLASSIFICATORE GROQ")
    print("=" * 80)
    
    examples = {
        "Sinistro Iniziale (0,0)": """Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente. Il paziente è stato informato e richiede risarcimento. Allego documentazione clinica completa.""",
        
        "Sinistro Follow-up (0,1)": """Rif. pratica SIN234567 - Dr. Bianchi. Invio documentazione medica integrativa richiesta dal vs perito. Allego referto specialistico che conferma nesso causale tra procedura e danno lamentato dal paziente. La famiglia ha aggiornato la richiesta risarcitoria.""",
        
        "Circostanza Iniziale (1,0)": """Spett.le compagnia, Dr.ssa Verdi, responsabile Qualità. Segnalo near miss verificatosi il 20/03/2024: infermiere ha preparato farmaco per paziente sbagliato ma errore intercettato prima della somministrazione. Nessun danno al paziente. Implementate procedure correttive.""",
        
        "Circostanza Follow-up (1,1)": """Rif. segnalazione CIRC789012 del 20/03/2024. Come richiesto invio relazione finale incident reporting. Il near miss è stato analizzato, implementato nuovo protocollo doppio controllo. Nessun danno occorso, situazione risolta."""
    }
    
    for nome, testo in examples.items():
        is_rel, conf, reason = check_context_relevance(testo)
        
        print(f"\n[{nome}]")
        print(f"Testo (prime 100 char): {testo[:100]}...")
        print(f"Pertinente: {is_rel}")
        print(f"Confidenza: {conf:.2%}")
        print(f"Motivo: {reason}")
        
        # Tutti gli esempi dell'app devono essere pertinenti
        assert is_rel, f"FALLITO: Esempio '{nome}' non riconosciuto come pertinente!"
        print(f"✅ Esempio validato")


def test_performance():
    """Test performance del guardrail"""
    import time
    
    print("\n\n" + "=" * 80)
    print("TEST PERFORMANCE GUARDRAIL - CLASSIFICATORE GROQ")
    print("=" * 80)
    
    testo_test = """Spett.le Compagnia, segnalo evento avverso durante intervento chirurgico. 
    Paziente richiede risarcimento danni. Allego documentazione medica completa."""
    
    num_iterations = 1000
    
    start_time = time.time()
    for _ in range(num_iterations):
        check_context_relevance(testo_test)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = (total_time / num_iterations) * 1000  # in millisecondi
    
    print(f"\nIterazioni: {num_iterations}")
    print(f"Tempo totale: {total_time:.4f} secondi")
    print(f"Tempo medio per verifica: {avg_time:.4f} ms")
    print(f"Verifiche al secondo: {num_iterations / total_time:.2f}")
    
    # Asserzione: deve essere veloce (< 5ms per verifica)
    assert avg_time < 5, f"Performance insufficiente: {avg_time:.4f}ms > 5ms"
    print("✅ Performance accettabile (overhead trascurabile rispetto a chiamata LLM)")


if __name__ == "__main__":
    print("\n🚀 AVVIO TEST GUARDRAIL CLASSIFICATORE GROQ\n")
    
    try:
        test_testi_pertinenti()
        test_testi_fuori_contesto()
        test_casi_borderline()
        test_esempi_applicazione()
        test_performance()
        
        print("\n\n" + "=" * 80)
        print("✅ TUTTI I TEST SUPERATI CON SUCCESSO!")
        print("=" * 80)
        print("\n💡 Il guardrail è pronto per l'uso nel classificatore Groq LLM")
        print("   Esegui l'app con: streamlit run streamlit_groq_classifier.py")
        
    except AssertionError as e:
        print(f"\n\n❌ TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRORE DURANTE I TEST: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
