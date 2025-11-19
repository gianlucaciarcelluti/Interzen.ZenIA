"""
Test delle funzionalità di correzione manuale del classificatore

Nota: Il file manual_corrections.json è salvato in src/classifier/
"""

import sys
from pathlib import Path

# Aggiungi il path corretto
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "classifier"))

from streamlit_multidimensional_classifier import (
    load_manual_corrections,
    save_manual_correction,
    integrate_manual_corrections,
    MANUAL_CORRECTIONS_FILE
)
from mock_email_multidimensional_dataset import create_mock_dataset


def test_load_corrections():
    """Test del caricamento delle correzioni"""
    print("🧪 Test: load_manual_corrections()")
    corrections = load_manual_corrections()
    print(f"✅ Correzioni caricate: {len(corrections)}")
    
    if corrections:
        print("\n📋 Prima correzione:")
        first = corrections[0]
        print(f"   - Timestamp: {first['timestamp']}")
        print(f"   - Testo: {first['text'][:100]}...")
        print(f"   - Tipologia: {first['tipologia']}")
        print(f"   - Riferimento: {first['riferimento_temporale']}")
    
    return corrections


def test_integrate_corrections():
    """Test dell'integrazione delle correzioni nel dataset"""
    print("\n🧪 Test: integrate_manual_corrections()")
    
    # Carica dataset originale
    df_original = create_mock_dataset()
    print(f"📊 Dataset originale: {len(df_original)} righe")
    
    # Integra correzioni
    df_integrated = integrate_manual_corrections(df_original)
    print(f"📊 Dataset integrato: {len(df_integrated)} righe")
    print(f"✅ Righe aggiunte: {len(df_integrated) - len(df_original)}")
    
    # Verifica struttura
    print("\n📋 Colonne del dataset:")
    print(df_integrated.columns.tolist())
    
    # Verifica ultimi elementi (le correzioni)
    num_corrections = len(df_integrated) - len(df_original)
    if num_corrections > 0:
        print(f"\n📋 Ultime {min(3, num_corrections)} correzioni aggiunte al dataset:")
        print(df_integrated.tail(min(3, num_corrections))[['testo', 'tipologia', 'riferimento_temporale']])
    
    return df_integrated


def test_save_correction():
    """Test del salvataggio di una nuova correzione"""
    print("\n🧪 Test: save_manual_correction()")
    
    # Conta correzioni attuali
    corrections_before = load_manual_corrections()
    num_before = len(corrections_before)
    print(f"📊 Correzioni prima: {num_before}")
    
    # Prepara dati di test
    test_text = "Questo è un testo di test per verificare il salvataggio delle correzioni manuali."
    test_tipologia = 0
    test_riferimento = 1
    test_original = {
        "tipologia": 1,
        "riferimento_temporale": 0,
        "confidenza_tipologia": 0.75,
        "confidenza_riferimento": 0.82
    }
    
    print("\n📝 Dati correzione di test:")
    print(f"   - Testo: {test_text[:50]}...")
    print(f"   - Tipologia corretta: {test_tipologia}")
    print(f"   - Riferimento corretto: {test_riferimento}")
    print(f"   - Predizione originale: {test_original}")
    
    # Chiedi conferma
    response = input("\n⚠️  Vuoi procedere con il salvataggio della correzione di test? (s/n): ")
    
    if response.lower() == 's':
        # Salva correzione
        num_total = save_manual_correction(
            test_text,
            test_tipologia,
            test_riferimento,
            test_original
        )
        
        print(f"✅ Correzione salvata! Totale correzioni: {num_total}")
        
        # Verifica salvataggio
        corrections_after = load_manual_corrections()
        num_after = len(corrections_after)
        print(f"📊 Correzioni dopo: {num_after}")
        print(f"✅ Incremento: +{num_after - num_before}")
        
        # Mostra ultima correzione
        if corrections_after:
            last = corrections_after[-1]
            print("\n📋 Ultima correzione salvata:")
            print(f"   - Timestamp: {last['timestamp']}")
            print(f"   - Testo: {last['text'][:50]}...")
            print(f"   - Tipologia: {last['tipologia']}")
            print(f"   - Riferimento: {last['riferimento_temporale']}")
        
        return True
    else:
        print("❌ Test di salvataggio annullato")
        return False


def test_file_structure():
    """Test della struttura del file JSON"""
    print("\n🧪 Test: Struttura file JSON")
    
    print(f"📁 Path file: {MANUAL_CORRECTIONS_FILE}")
    print(f"📁 File esiste: {MANUAL_CORRECTIONS_FILE.exists()}")
    
    if MANUAL_CORRECTIONS_FILE.exists():
        import json
        with open(MANUAL_CORRECTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ File JSON valido")
        print(f"📊 Numero di correzioni: {len(data)}")
        
        if data:
            print("\n📋 Struttura prima correzione:")
            first = data[0]
            for key, value in first.items():
                if key == 'text':
                    print(f"   - {key}: {str(value)[:50]}...")
                else:
                    print(f"   - {key}: {value}")


def main():
    """Esegue tutti i test"""
    print("=" * 80)
    print("🧪 TEST FUNZIONALITÀ CORREZIONE MANUALE CLASSIFICATORE")
    print("=" * 80)
    
    try:
        # Test 1: Struttura file
        test_file_structure()
        
        print("\n" + "-" * 80 + "\n")
        
        # Test 2: Caricamento
        corrections = test_load_corrections()
        
        print("\n" + "-" * 80 + "\n")
        
        # Test 3: Integrazione
        df = test_integrate_corrections()
        
        print("\n" + "-" * 80 + "\n")
        
        # Test 4: Salvataggio (opzionale)
        test_save_correction()
        
        print("\n" + "=" * 80)
        print("✅ TUTTI I TEST COMPLETATI")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERRORE durante i test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
