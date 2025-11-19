"""
Test con prompt semplificati per gemma3:270m
"""
import asyncio
import sys
import os

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from mcp_server.server import OllamaClient

async def test_simple_prompts():
    """Test con prompt molto semplici per gemma3:270m"""
    
    print("🔍 Test Prompt Semplificati per gemma3:270m\n")
    
    ollama = OllamaClient("http://localhost:11434", "gemma3:270m")
    
    # Test 1: Prompt base
    print("1️⃣ Test prompt base...")
    try:
        response = await ollama.generate(
            "Scrivi una frase di esempio.",
            "Sei un assistente utile."
        )
        print(f"✅ Risposta: {response[:100]}...")
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    # Test 2: Prompt JSON semplice
    print("\n2️⃣ Test JSON semplice...")
    try:
        response = await ollama.generate(
            'Rispondi con JSON: {"test": "ok", "numero": 1}',
            "Rispondi solo in JSON."
        )
        print(f"✅ Risposta: {response}")
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    # Test 3: Analisi documento molto semplice
    print("\n3️⃣ Test analisi documento semplice...")
    try:
        doc_text = "Mario Rossi richiede autorizzazione per scarico acque."
        response = await ollama.generate(
            f'Analizza: {doc_text}\n\nRispondi: {{"nome": "...", "tipo": "..."}}',
            "Estrai nome e tipo richiesta."
        )
        print(f"✅ Risposta: {response}")
    except Exception as e:
        print(f"❌ Errore: {e}")

async def main():
    print("🚀 Test Compatibilità gemma3:270m\n")
    await test_simple_prompts()
    print("\n💡 Se i test falliscono, cambia modello a llama3.2:1b")

if __name__ == "__main__":
    asyncio.run(main())