"""
Test per verificare il funzionamento del guardrail di pertinenza del contesto
nel classificatore multi-dimensionale di email per sinistri medical malpractice.
"""

import sys
from pathlib import Path

# Aggiungi il percorso del modulo al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "SP04" / "classifier"))

from streamlit_multidimensional_classifier import check_context_relevance


def test_testi_pertinenti():
    """Testa che testi pertinenti vengano riconosciuti correttamente"""
    
    testi_pertinenti = [
        # Sinistro medico chiaro
        """Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso 
        verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico 
        al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente.""",
        
        # Follow-up assicurativo
        """Rif. pratica SIN12345 - Dr.ssa Bianchi. Vi informo che il paziente ha presentato 
        formale messa in mora. Invio documentazione integrativa richiesta dal vs perito.""",
        
        # Segnalazione risk management
        """Spett.le compagnia, Dr. Verdi, Risk Manager. Vi segnalo criticità rilevata durante 
        audit: alcuni operatori sanitari non rispettano protocollo igiene mani in ospedale.""",
        
        # Richiesta risarcimento
        """Egregio Sig. Direttore, sono il familiare del paziente ricoverato in clinica. 
        A seguito di grave negligenza medica durante la degenza, richiediamo risarcimento danni."""
    ]
    
    print("=" * 80)
    print("TEST TESTI PERTINENTI AL DOMINIO")
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
        # Domanda generica
        "Che tempo fa oggi?",
        
        # Conversazione casuale
        "Ciao, come stai? Tutto bene?",
        
        # Testo completamente diverso
        "La ricetta della pizza margherita prevede farina, pomodoro, mozzarella e basilico.",
        
        # Domanda su altro argomento
        "Quali sono le migliori destinazioni turistiche in Italia?",
        
        # Codice di programmazione
        "def hello_world(): print('Hello, World!')",
        
        # Domanda filosofica
        "Qual è il senso della vita?",
        
        # Sport
        "Il calcio è lo sport più popolare in Italia. La Juventus ha vinto molti scudetti.",
        
        # Economia generica
        "I tassi di interesse della BCE influenzano l'economia europea.",
        
        # Testo troppo breve
        "Ciao",
        
        # Elenco casuale
        "Mela, pera, banana, arancia"
    ]
    
    print("\n\n" + "=" * 80)
    print("TEST TESTI FUORI CONTESTO")
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


def test_casi_limite():
    """Testa casi limite e borderline"""
    
    print("\n\n" + "=" * 80)
    print("TEST CASI LIMITE")
    print("=" * 80)
    
    # Testo con poche keyword mediche ma in contesto diverso
    testo_limite_1 = """Il dottore mi ha detto che devo andare in vacanza. 
    L'ospedale più vicino alla spiaggia è molto carino."""
    
    is_rel, conf, reason = check_context_relevance(testo_limite_1)
    print(f"\n[Caso Limite 1 - Keyword mediche ma contesto turistico]")
    print(f"Testo: {testo_limite_1}")
    print(f"Pertinente: {is_rel}")
    print(f"Confidenza: {conf:.2%}")
    print(f"Motivo: {reason}")
    
    # Testo medico ma senza riferimento a sinistri
    testo_limite_2 = """Il paziente è stato visitato in ambulatorio. 
    La diagnosi è stata confermata con esami di laboratorio. La terapia prescritta prevede farmaci."""
    
    is_rel, conf, reason = check_context_relevance(testo_limite_2)
    print(f"\n[Caso Limite 2 - Testo medico generico]")
    print(f"Testo: {testo_limite_2}")
    print(f"Pertinente: {is_rel}")
    print(f"Confidenza: {conf:.2%}")
    print(f"Motivo: {reason}")
    
    # Testo con keyword ma in lingua straniera mescolata
    testo_limite_3 = """The patient was admitted to hospital with complications. 
    Il medico ha commesso un errore durante l'intervento chirurgico. Chiediamo risarcimento."""
    
    is_rel, conf, reason = check_context_relevance(testo_limite_3)
    print(f"\n[Caso Limite 3 - Testo misto italiano/inglese]")
    print(f"Testo: {testo_limite_3}")
    print(f"Pertinente: {is_rel}")
    print(f"Confidenza: {conf:.2%}")
    print(f"Motivo: {reason}")


def test_performance_guardrail():
    """Testa le performance del guardrail"""
    import time
    
    print("\n\n" + "=" * 80)
    print("TEST PERFORMANCE GUARDRAIL")
    print("=" * 80)
    
    testo_test = """Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento avverso 
    verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento chirurgico 
    al ginocchio sx, per errore procedurale è stato operato il ginocchio dx del paziente. 
    Il paziente è stato informato e richiede risarcimento. Allego documentazione clinica completa."""
    
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
    print("✅ Performance accettabile")


if __name__ == "__main__":
    print("\n🚀 AVVIO TEST GUARDRAIL PERTINENZA CONTESTO\n")
    
    try:
        test_testi_pertinenti()
        test_testi_fuori_contesto()
        test_casi_limite()
        test_performance_guardrail()
        
        print("\n\n" + "=" * 80)
        print("✅ TUTTI I TEST SUPERATI CON SUCCESSO!")
        print("=" * 80)
        
    except AssertionError as e:
        print(f"\n\n❌ TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRORE DURANTE I TEST: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
