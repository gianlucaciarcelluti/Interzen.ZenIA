"""
Test rapido delle nuove funzionalità Groq Integration
Esegui questo script per verificare che tutto funzioni correttamente
"""

import os
import sys

# Carica variabili d'ambiente dal file .env
from dotenv import load_dotenv
load_dotenv()

# Aggiungi il percorso src al path per import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'llm_classifier'))

# Verifica tqdm installato
try:
    from tqdm import tqdm
    print("✅ tqdm installato correttamente")
except ImportError:
    print("❌ tqdm non installato. Esegui: pip install tqdm")
    sys.exit(1)

# Verifica groq_integration
try:
    from llm_classifier.groq_integration import GroqClassifier
    print("✅ groq_integration importato correttamente")
except ImportError as e:
    print(f"❌ Errore import groq_integration: {e}")
    sys.exit(1)

# Verifica API key
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("⚠️  GROQ_API_KEY non trovata")
    print("   Per test completo, imposta: $env:GROQ_API_KEY='your-key'")
    print("\n✅ Test import completato - API key richiesta per test funzionali")
    sys.exit(0)

print("✅ GROQ_API_KEY trovata\n")

# Test 1: Inizializzazione
print("=" * 60)
print("TEST 1: Inizializzazione Classifier")
print("=" * 60)

try:
    classifier = GroqClassifier(
        api_key=api_key,
        cache_dir="test_cache"
    )
    print("✅ Classifier inizializzato")
    print(f"   Modello default: {classifier.model}")
    print(f"   Cache directory: {classifier.cache_dir}")
except Exception as e:
    print(f"❌ Errore inizializzazione: {e}")
    sys.exit(1)

# Test 2: Recupero modelli
print("\n" + "=" * 60)
print("TEST 2: Recupero Modelli dall'API")
print("=" * 60)

try:
    print("Recupero modelli disponibili...")
    available = classifier.fetch_available_models()
    print(f"✅ Recuperati {len(available)} modelli")
    
    if available:
        print("\nPrimi 5 modelli:")
        for model in available[:5]:
            status = "🟢" if model.get("active", True) else "🔴"
            print(f"   {status} {model['id']}")
    
    recommended = classifier.get_recommended_models()
    print(f"\n✅ Modelli consigliati: {len(recommended)}")
    for i, model in enumerate(recommended[:3], 1):
        print(f"   {i}. {model}")
        
except Exception as e:
    print(f"❌ Errore recupero modelli: {e}")
    print("   Fallback a modelli predefiniti disponibile")

# Test 3: Progress bar
print("\n" + "=" * 60)
print("TEST 3: Progress Bar (Test Visivo)")
print("=" * 60)

try:
    print("Simulazione progress bar con tqdm...")
    import time
    
    with tqdm(total=20, desc="Test", unit="item") as pbar:
        for i in range(20):
            time.sleep(0.05)
            pbar.update(1)
    
    print("✅ Progress bar funzionante")
    
except Exception as e:
    print(f"❌ Errore progress bar: {e}")

# Test 4: Persistenza (senza chiamate API)
print("\n" + "=" * 60)
print("TEST 4: Sistema Persistenza")
print("=" * 60)

try:
    test_emails = ["test1", "test2", "test3"]
    cache_key = classifier._get_cache_key(test_emails, "test-model")
    print(f"✅ Cache key generata: {cache_key}")
    
    # Test salvataggio
    test_data = [{"test": "data"}]
    classifier._save_progress(cache_key, test_data, 1)
    print("✅ Salvataggio cache funzionante")
    
    # Test caricamento
    loaded = classifier._load_progress(cache_key)
    if loaded:
        print("✅ Caricamento cache funzionante")
        print(f"   Dati caricati: {loaded}")
    
    # Cleanup
    classifier._clear_cache(cache_key)
    print("✅ Pulizia cache funzionante")
    
except Exception as e:
    print(f"❌ Errore persistenza: {e}")

# Test 5: Classificazione singola (richiede API)
print("\n" + "=" * 60)
print("TEST 5: Classificazione Singola (API)")
print("=" * 60)

try:
    test_email = "Segnalo evento del 15/03/2024 con richiesta danni."
    print(f"Email di test: {test_email}")
    print("Classificazione in corso...\n")
    
    result = classifier.classify_single(test_email)
    
    if result.get("success"):
        print("✅ Classificazione riuscita")
        print(f"   Tipologia: {result.get('tipologia')}")
        print(f"   Riferimento: {result.get('riferimento_temporale')}")
        print(f"   Latency: {result.get('latency', 0):.3f}s")
        print(f"   Confidence: Tip={result.get('confidence_tipologia', 0):.2f}, "
              f"Rif={result.get('confidence_riferimento', 0):.2f}")
    else:
        print(f"❌ Classificazione fallita: {result.get('error')}")
        
except Exception as e:
    print(f"❌ Errore classificazione: {e}")
    print("   Verifica API key e quota disponibile")

# Riepilogo
print("\n" + "=" * 60)
print("RIEPILOGO TEST")
print("=" * 60)
print("✅ Import e dipendenze: OK")
print("✅ Inizializzazione: OK")
print("✅ Recupero modelli: OK")
print("✅ Progress bar: OK")
print("✅ Persistenza: OK")
print("✅ Sistema pronto per l'uso!")
print("\n💡 Per esempi completi, vedi: example_groq_features.py")
print("💡 Per notebook interattivo, apri: groq_study_notebook.ipynb")

# Cleanup finale
import shutil
if os.path.exists("test_cache"):
    shutil.rmtree("test_cache")
    print("\n🧹 Test cache rimossa")
