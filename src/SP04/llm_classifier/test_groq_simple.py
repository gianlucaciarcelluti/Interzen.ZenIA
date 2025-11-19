"""
Test rapido per verificare che groq_integration funzioni
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("TEST GROQ INTEGRATION")
print("=" * 60)

# 0. Carica .env dalla root del progetto
print("\n0️⃣ Carica file .env...")
try:
    from dotenv import load_dotenv
    
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    env_file = root_dir / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ File .env caricato da: {env_file}")
    else:
        print(f"⚠️ File .env non trovato in: {env_file}")
        load_dotenv()  # Prova nella directory corrente
except ImportError:
    print("⚠️ python-dotenv non installato")

# 1. Verifica import
print("\n1️⃣ Verifica import groq_integration...")
try:
    from groq_integration import GroqClassifier
    print("✅ Import groq_integration riuscito")
except ImportError as e:
    print(f"❌ Errore import: {e}")
    sys.exit(1)

# 2. Verifica API key
print("\n2️⃣ Verifica API key...")
api_key = os.environ.get("GROQ_API_KEY", "")

if api_key:
    print(f"✅ API key trovata (lunghezza: {len(api_key)})")
    print(f"   Inizia con: {api_key[:10]}...")
else:
    print("❌ API key NON trovata")
    print("   Impostala con: export GROQ_API_KEY='your-key-here'")
    print("   Oppure crea un file .env con: GROQ_API_KEY=your-key-here")
    sys.exit(1)

# 3. Inizializza classifier
print("\n3️⃣ Inizializzazione classifier...")
try:
    classifier = GroqClassifier(api_key=api_key, model="llama-3.1-8b-instant")
    print("✅ Classifier inizializzato correttamente")
except Exception as e:
    print(f"❌ Errore inizializzazione: {e}")
    sys.exit(1)

# 4. Test classificazione
print("\n4️⃣ Test classificazione...")
test_email = """
Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare 
un evento avverso verificatosi il 15/03/2024 presso il nostro reparto. 
Durante intervento chirurgico al ginocchio sx, per errore procedurale 
è stato operato il ginocchio dx del paziente.
"""

try:
    print("   Invio richiesta a Groq...")
    results = classifier.classify_batch([test_email], show_progress=False)
    
    if results.empty:
        print("❌ Nessun risultato ricevuto")
        sys.exit(1)
    
    result = results.iloc[0]
    
    if result['success']:
        print("✅ Classificazione riuscita!")
        print(f"   Tipologia: {result['tipologia']}")
        print(f"   Riferimento: {result['riferimento_temporale']}")
        print(f"   Confidence Tipologia: {result['confidence_tipologia']:.2%}")
        print(f"   Confidence Riferimento: {result['confidence_riferimento']:.2%}")
        print(f"   Latenza: {result['latency']:.3f}s")
    else:
        print(f"❌ Classificazione fallita: {result.get('error', 'Errore sconosciuto')}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Errore durante classificazione: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TUTTI I TEST COMPLETATI CON SUCCESSO!")
print("=" * 60)
