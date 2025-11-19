"""
Test per recuperare i modelli disponibili da Groq
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Carica .env dalla root
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent.parent
env_file = root_dir / '.env'

if env_file.exists():
    load_dotenv(env_file)
    print(f"✅ File .env caricato da: {env_file}")

# Recupera API key
api_key = os.environ.get("GROQ_API_KEY", "")

if not api_key:
    print("❌ API key non trovata")
    exit(1)

print(f"\n🔑 API Key trovata (lunghezza: {len(api_key)})\n")

# Chiama API Groq
print("📡 Recupero modelli disponibili da Groq...\n")

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
        print(f"✅ Recuperati {len(data.get('data', []))} modelli\n")
        print("=" * 80)
        print(f"{'MODEL ID':<40} | {'OWNED BY':<20} | {'CREATED':<15}")
        print("=" * 80)
        
        for model in data.get('data', []):
            model_id = model.get('id', 'N/A')
            owned_by = model.get('owned_by', 'N/A')
            created = model.get('created', 'N/A')
            print(f"{model_id:<40} | {owned_by:<20} | {created:<15}")
        
        print("=" * 80)
        
        # Filtra modelli consigliati
        print("\n🎯 Modelli consigliati per classificazione:")
        print("-" * 80)
        
        for model in data.get('data', []):
            model_id = model.get('id', '')
            if 'llama' in model_id.lower() or 'mixtral' in model_id.lower() or 'gemma' in model_id.lower():
                print(f"  • {model_id}")
        
        print("-" * 80)
    else:
        print(f"❌ Errore HTTP {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Errore: {e}")
    import traceback
    traceback.print_exc()
