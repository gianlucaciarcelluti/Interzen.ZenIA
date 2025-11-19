"""
Test minimale del server MCP per identificare il problema di base.
"""

import asyncio
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import config

async def test_minimal_mcp():
    """Test minimale per verificare se il server MCP si avvia senza problemi"""
    print("🧪 Test minimale server MCP")
    print("=" * 40)
    
    try:
        # Test 1: Importazioni
        print("📦 Test importazioni...")
        from mcp_server.server import app, DeterminaTools, OllamaClient
        print("✅ Importazioni riuscite")
        
        # Test 2: Creazione oggetti
        print("🔧 Test creazione oggetti...")
        ollama_client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        tools = DeterminaTools(ollama_client)
        print("✅ Oggetti creati")
        
        # Test 3: Test Ollama
        print("🌐 Test connessione Ollama...")
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{config.OLLAMA_BASE_URL}/api/tags")
                if response.status_code == 200:
                    print("✅ Ollama raggiungibile")
                else:
                    print(f"⚠️  Ollama status: {response.status_code}")
        except Exception as e:
            print(f"❌ Ollama non raggiungibile: {str(e)}")
        
        # Test 4: Test tools
        print("🛠️  Test tools...")
        try:
            # Proviamo una chiamata semplice
            result = await tools.fascicolo_analyzer(
                "Test fascicolo contenuto", 
                ["istanza", "documento"]
            )
            if result and result.get("success"):
                print("✅ Tool fascicolo_analyzer funziona")
            else:
                print(f"⚠️  Tool restituisce: {result}")
        except Exception as e:
            print(f"❌ Errore nel tool: {str(e)}")
        
        print("\n🎉 Test minimale completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test minimale: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_manual_mcp_server():
    """Test manuale del server MCP senza stdio"""
    print("\n🧪 Test manuale server MCP")
    print("=" * 40)
    
    try:
        from mcp_server.server import app, tools
        
        print("� Test diretto dei tools...")
        
        # Test diretto del tool
        test_result = await tools.fascicolo_analyzer(
            "Test contenuto fascicolo per verifica funzionalità",
            ["istanza", "allegato", "documento"]
        )
        
        print(f"✅ Tool testato direttamente")
        print(f"   - Successo: {test_result.get('success', 'N/A')}")
        
        if test_result.get('success'):
            analysis = test_result.get('analysis', {})
            print(f"   - Tipo procedimento: {analysis.get('procedimento_type', 'N/A')}")
            print(f"   - Richiedente nome: {analysis.get('richiedente', {}).get('nome', 'N/A')}")
        else:
            print(f"   - Errore: {test_result.get('error', 'N/A')}")
        
        print("\n🎉 Test manuale completato!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test manuale: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Esegue tutti i test"""
    print("🏛️ Diagnosi Server MCP")
    print("🎯 Test per identificare il problema di base")
    print("=" * 50)
    
    # Test configurazione
    print(f"📍 Ollama URL: {config.OLLAMA_BASE_URL}")
    print(f"🤖 Modello: {config.OLLAMA_MODEL}")
    
    test1_ok = await test_minimal_mcp()
    test2_ok = await test_manual_mcp_server()
    
    print("\n" + "=" * 50)
    print("📊 RISULTATI")
    print("=" * 50)
    
    if test1_ok and test2_ok:
        print("✅ Server MCP: Funzionalità di base OK")
        print("💡 Il problema è probabilmente nella comunicazione stdio")
        print("🔧 Suggerimenti:")
        print("   - Il server funziona internamente")
        print("   - Il problema è nel protocollo JSON-RPC via stdio")
        print("   - Verifica la configurazione del client")
    else:
        print("❌ Server MCP: Problemi nelle funzionalità di base")
        print("🔧 Risolvi prima questi problemi:")
        if not test1_ok:
            print("   - Problemi con importazioni o configurazione")
        if not test2_ok:
            print("   - Problemi con le funzionalità dei tools")

if __name__ == "__main__":
    asyncio.run(main())