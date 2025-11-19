"""
Test specifico per llama3.2:1b
"""
import os
import asyncio
import sys

# Imposta il modello
os.environ["OLLAMA_MODEL"] = "llama3.2:1b"

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from mcp_server.server import OllamaClient
import json

async def test_llama_1b_capabilities():
    """Test delle capacità di llama3.2:1b per il nostro progetto"""
    
    print("🧠 Test Capacità llama3.2:1b")
    print(f"📋 Modello: {os.getenv('OLLAMA_MODEL')}\n")
    
    ollama = OllamaClient("http://localhost:11434", "llama3.2:1b")
    
    tests = [
        {
            "name": "Test JSON Base",
            "system": "Rispondi solo in JSON valido.",
            "prompt": 'Crea un JSON con: {"nome": "Mario", "tipo": "autorizzazione"}',
            "expected_json": True
        },
        {
            "name": "Analisi Documento Semplice", 
            "system": "Sei un esperto di procedure amministrative. Estrai informazioni in JSON.",
            "prompt": """Analizza: "Mario Rossi (CF: RSSMRA80A01H501X) richiede autorizzazione per scarico acque reflue via Roma 123, Milano."
            
            JSON richiesto:
            {
                "richiedente": {"nome": "...", "cognome": "...", "cf": "..."},
                "tipo_procedimento": "...",
                "oggetto": "...",
                "indirizzo": "..."
            }""",
            "expected_json": True
        },
        {
            "name": "Generazione Testo Strutturato",
            "system": "Sei un esperto legale. Scrivi in italiano formale.",
            "prompt": """Scrivi le premesse per una determina amministrativa per autorizzazione scarico acque reflue.
            
            Formato richiesto:
            PREMESSE:
            - VISTO il D.Lgs...
            - CONSIDERATO che...
            - ACCERTATO che...""",
            "expected_json": False
        }
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"{i}️⃣ {test['name']}...")
        
        try:
            response = await ollama.generate(test['prompt'], test['system'])
            
            if not response or response.strip() == "":
                results.append({"test": test['name'], "status": "❌ FAILED", "error": "Risposta vuota"})
                print(f"   ❌ FAILED: Risposta vuota")
                continue
            
            # Verifica JSON se richiesto
            if test['expected_json']:
                try:
                    # Pulisci risposta
                    clean_response = response.strip()
                    if clean_response.startswith('```json'):
                        clean_response = clean_response[7:]
                    if clean_response.endswith('```'):
                        clean_response = clean_response[:-3]
                    clean_response = clean_response.strip()
                    
                    json.loads(clean_response)
                    results.append({"test": test['name'], "status": "✅ PASSED", "length": len(response)})
                    print(f"   ✅ PASSED: JSON valido ({len(response)} chars)")
                    print(f"   📝 Preview: {response[:100]}...")
                except json.JSONDecodeError:
                    results.append({"test": test['name'], "status": "🟡 PARTIAL", "error": "JSON non valido"})
                    print(f"   🟡 PARTIAL: Risposta ricevuta ma JSON non valido")
                    print(f"   📝 Preview: {response[:100]}...")
            else:
                results.append({"test": test['name'], "status": "✅ PASSED", "length": len(response)})
                print(f"   ✅ PASSED: Testo generato ({len(response)} chars)")
                print(f"   📝 Preview: {response[:100]}...")
                
        except Exception as e:
            results.append({"test": test['name'], "status": "❌ ERROR", "error": str(e)})
            print(f"   ❌ ERROR: {str(e)}")
        
        print()
    
    # Riepilogo
    print("📊 RIEPILOGO TEST:")
    passed = sum(1 for r in results if r['status'].startswith('✅'))
    partial = sum(1 for r in results if r['status'].startswith('🟡'))
    failed = sum(1 for r in results if r['status'].startswith('❌'))
    
    print(f"   ✅ Successi: {passed}/{len(tests)}")
    print(f"   🟡 Parziali: {partial}/{len(tests)}")
    print(f"   ❌ Falliti: {failed}/{len(tests)}")
    
    if passed >= 2:
        print(f"\n🎉 llama3.2:1b dovrebbe funzionare bene per il progetto!")
    elif passed >= 1:
        print(f"\n🟡 llama3.2:1b potrebbe funzionare per il progetto!")
    else:
        print(f"\n❌ llama3.2:1b potrebbe essere insufficiente")
    
    return results

async def main():
    print("🚀 Test Compatibilità llama3.2:1b per ZenIA\n")
    await test_llama_1b_capabilities()

if __name__ == "__main__":
    asyncio.run(main())