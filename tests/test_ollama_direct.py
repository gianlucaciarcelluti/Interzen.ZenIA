"""
Test semplificato per debuggare il problema JSON del document-composer
Questo test bypassa le dipendenze e testa direttamente il problema
"""
import asyncio
import json
import aiohttp

async def test_ollama_directly():
    """Test diretto del server Ollama per capire cosa sta succedendo"""
    
    print("🔍 Test diretto del server Ollama...")
    
    # Test di connessione base
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Ollama è attivo, modelli disponibili: {[m['name'] for m in data.get('models', [])]}")
                    return True
                else:
                    print(f"❌ Ollama non risponde correttamente: status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Errore di connessione a Ollama: {str(e)}")
        return False

async def test_ollama_generation():
    """Test di generazione semplice con Ollama"""
    
    print("\n🔍 Test di generazione con Ollama...")
    
    # Prompt molto semplice per un JSON
    simple_prompt = """
    Genera un documento JSON molto semplice per un test.
    Rispondi SOLO con JSON valido, senza altri commenti:
    
    {
        "test": "successo",
        "documento": "test document",
        "timestamp": "2024-01-01T12:00:00"
    }
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "gemma2:2b",
                "prompt": simple_prompt,
                "format": "json",
                "stream": False
            }
            
            print("📤 Invio richiesta a Ollama...")
            async with session.post("http://localhost:11434/api/generate", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ollama_response = data.get("response", "")
                    
                    print(f"📥 Risposta Ollama (lunghezza: {len(ollama_response)}):")
                    print(f"   - Raw response: {repr(ollama_response[:200])}")
                    
                    # Tenta di parsare come JSON
                    try:
                        # Pulisce la risposta
                        cleaned = ollama_response.strip()
                        if cleaned.startswith('```json'):
                            cleaned = cleaned[7:]
                        if cleaned.endswith('```'):
                            cleaned = cleaned[:-3]
                        cleaned = cleaned.strip()
                        
                        parsed = json.loads(cleaned)
                        print(f"✅ JSON parseato correttamente: {parsed}")
                        return True
                        
                    except json.JSONDecodeError as je:
                        print(f"❌ Errore parsing JSON: {str(je)}")
                        print(f"   - Contenuto da parsare: {repr(cleaned)}")
                        return False
                        
                else:
                    print(f"❌ Errore HTTP: {response.status}")
                    text = await response.text()
                    print(f"   - Dettagli: {text[:200]}")
                    return False
                    
    except Exception as e:
        print(f"❌ Errore durante la generazione: {str(e)}")
        return False

async def test_complex_prompt():
    """Test con un prompt più complesso simile a quello del document-composer"""
    
    print("\n🔍 Test con prompt complesso...")
    
    complex_prompt = """
    Componi una determina amministrativa in formato JSON.
    
    Sezioni disponibili:
    - premesse: Test delle premesse
    - dispositivo: Test del dispositivo
    
    Template: determina_standard
    Ente: Comune di Test
    
    Rispondi SOLO con JSON valido in questo formato:
    {
        "premesse": "contenuto premesse",
        "dispositivo": "contenuto dispositivo",
        "numero": "DETERMINA_001",
        "data": "2024-01-01",
        "firma": {
            "ruolo": "Dirigente",
            "nome": "Da completare"
        }
    }
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "gemma2:2b",
                "prompt": complex_prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            print("📤 Invio prompt complesso a Ollama...")
            async with session.post("http://localhost:11434/api/generate", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ollama_response = data.get("response", "")
                    
                    print(f"📥 Risposta complessa (lunghezza: {len(ollama_response)}):")
                    
                    if len(ollama_response) == 0:
                        print("❌ Risposta vuota! Questo è il problema.")
                        return False
                    
                    print(f"   - Primi 300 caratteri: {repr(ollama_response[:300])}")
                    
                    # Tenta di parsare
                    try:
                        cleaned = ollama_response.strip()
                        if cleaned.startswith('```json'):
                            cleaned = cleaned[7:]
                        if cleaned.endswith('```'):
                            cleaned = cleaned[:-3]
                        cleaned = cleaned.strip()
                        
                        if cleaned:
                            parsed = json.loads(cleaned)
                            print(f"✅ JSON complesso parseato: {list(parsed.keys())}")
                            return True
                        else:
                            print("❌ Contenuto vuoto dopo pulizia")
                            return False
                            
                    except json.JSONDecodeError as je:
                        print(f"❌ Errore parsing JSON complesso: {str(je)}")
                        print(f"   - Posizione errore: carattere {je.pos}")
                        return False
                        
                else:
                    print(f"❌ Errore HTTP nel test complesso: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Errore nel test complesso: {str(e)}")
        return False

async def main():
    print("🚀 Debug diretto del problema JSON\n")
    
    # Test 1: Connessione Ollama
    connected = await test_ollama_directly()
    if not connected:
        print("⚠️ Ollama non è disponibile, impossibile continuare")
        return
    
    # Test 2: Generazione semplice
    simple_success = await test_ollama_generation()
    
    # Test 3: Generazione complessa
    complex_success = await test_complex_prompt()
    
    print(f"\n📊 Risultati:")
    print(f"   - Connessione Ollama: {'✅' if connected else '❌'}")
    print(f"   - Generazione semplice: {'✅' if simple_success else '❌'}")
    print(f"   - Generazione complessa: {'✅' if complex_success else '❌'}")
    
    if not simple_success:
        print("\n❗ Il problema è nella generazione base di Ollama")
    elif not complex_success:
        print("\n❗ Il problema è con prompt complessi - potrebbe essere timeout o memoria")
    else:
        print("\n🎉 Ollama funziona correttamente - il problema è altrove")

if __name__ == "__main__":
    asyncio.run(main())