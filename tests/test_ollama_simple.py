"""
Test molto semplice usando solo librerie standard
"""
import json
import urllib.request
import urllib.error
import urllib.parse

def test_ollama_connection():
    """Test connessione Ollama usando urllib"""
    print("🔍 Test connessione Ollama...")
    
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                models = [m['name'] for m in data.get('models', [])]
                print(f"✅ Ollama attivo, modelli: {models}")
                return True
            else:
                print(f"❌ Status code: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Errore connessione: {str(e)}")
        return False

def test_ollama_generation():
    """Test generazione semplice"""
    print("\n🔍 Test generazione semplice...")
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": "Genera un JSON semplice: {'test': 'ok'}",
        "format": "json",
        "stream": False
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
                ollama_response = result.get("response", "")
                
                print(f"📥 Risposta Ollama:")
                print(f"   - Lunghezza: {len(ollama_response)}")
                print(f"   - Contenuto: {repr(ollama_response[:200])}")
                
                if ollama_response:
                    try:
                        # Prova a parsare come JSON
                        cleaned = ollama_response.strip()
                        if cleaned.startswith('```json'):
                            cleaned = cleaned[7:]
                        if cleaned.endswith('```'):
                            cleaned = cleaned[:-3]
                        cleaned = cleaned.strip()
                        
                        parsed = json.loads(cleaned)
                        print(f"✅ JSON valido: {parsed}")
                        return True
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON non valido: {str(e)}")
                        print(f"   - Tentativo parse: {repr(cleaned)}")
                        return False
                else:
                    print("❌ Risposta vuota")
                    return False
            else:
                print(f"❌ Status: {response.status}")
                return False
    
    except urllib.error.URLError as e:
        print(f"❌ Errore URL: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Errore: {str(e)}")
        return False

def main():
    print("🚀 Test Ollama con librerie standard\n")
    
    # Test connessione
    if not test_ollama_connection():
        print("⚠️ Ollama non disponibile")
        return
    
    # Test generazione
    generation_ok = test_ollama_generation()
    
    print(f"\n📊 Risultato generazione: {'✅' if generation_ok else '❌'}")
    
    if not generation_ok:
        print("\n💡 Possibili cause:")
        print("   - Modello non disponibile")
        print("   - Timeout nella generazione")
        print("   - Problema con formato JSON")
        print("   - Memoria insufficiente")

if __name__ == "__main__":
    main()