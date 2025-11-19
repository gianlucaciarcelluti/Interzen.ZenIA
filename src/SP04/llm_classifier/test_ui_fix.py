"""
Test rapido per verificare la classificazione con i nuovi fix UI
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carica .env dalla root
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
env_file = root_dir / '.env'

if env_file.exists():
    load_dotenv(env_file)

from groq_integration import GroqClassifier

# Test email
test_email = """
Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare 
un evento avverso verificatosi il 15/03/2024 presso il nostro reparto. 
Durante intervento chirurgico al ginocchio sx, per errore procedurale 
è stato operato il ginocchio dx del paziente. Il paziente è stato informato 
e richiede risarcimento. Allego documentazione clinica completa.
"""

api_key = os.environ.get("GROQ_API_KEY", "")
if not api_key:
    print("❌ API key non trovata")
    exit(1)

print("=" * 80)
print("TEST CLASSIFICAZIONE CON INDICATORI CHIAVE")
print("=" * 80)

classifier = GroqClassifier(api_key=api_key, model="llama-3.1-8b-instant")

print("\n📧 Email di test:")
print("-" * 80)
print(test_email.strip())
print("-" * 80)

print("\n🔄 Classificazione in corso...")
results = classifier.classify_batch([test_email], show_progress=False)

if results.empty or not results.iloc[0]['success']:
    print("❌ Errore durante la classificazione")
    exit(1)

result = results.iloc[0]

print("\n✅ Classificazione completata!\n")
print("=" * 80)
print("RISULTATI")
print("=" * 80)

print(f"\n📊 Tipologia: {result['tipologia']}")
print(f"   Confidence: {result['confidence_tipologia']:.2%}")

print(f"\n📅 Riferimento Temporale: {result['riferimento_temporale']}")
print(f"   Confidence: {result['confidence_riferimento']:.2%}")

print(f"\n💡 Spiegazione:")
print(f"   {result.get('spiegazione', 'N/A')}")

print(f"\n🔑 Indicatori Chiave:")
if 'indicatori_chiave' in result and isinstance(result['indicatori_chiave'], list):
    for idx, indicator in enumerate(result['indicatori_chiave'], 1):
        print(f"   {idx}. {indicator}")
else:
    print("   N/A")

print("\n" + "=" * 80)
print("✅ TEST COMPLETATO")
print("=" * 80)
