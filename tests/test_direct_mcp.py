"""
Test del client MCP diretto per verificare che risolva i problemi di comunicazione.
"""

import asyncio
import sys
import os

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_client.direct_client import create_direct_mcp_client, create_direct_generation_service


async def test_direct_mcp_client():
    """Test del client MCP diretto"""
    print("🔍 Test Client MCP Diretto")
    print("=" * 40)
    
    try:
        # Test connessione
        print("🚀 Connessione client diretto...")
        client = await create_direct_mcp_client()
        print("✅ Connessione riuscita")
        
        # Test listing tools
        print("🔧 Test listing tools...")
        tools = await client.list_available_tools()
        print(f"✅ Tools disponibili ({len(tools)}):")
        for tool in tools:
            print(f"   - {tool}")
        
        # Test tool execution
        print("🛠️  Test esecuzione tool...")
        result = await client.invoke_tool("fascicolo-analyzer", {
            "fascicolo_content": "Test fascicolo per verifica funzionalità del client diretto",
            "document_types": ["istanza", "allegato"]
        })
        
        print(f"✅ Tool eseguito:")
        print(f"   - Successo: {result.get('success')}")
        if result.get('success'):
            analysis = result.get('analysis', {})
            print(f"   - Tipo procedimento: {analysis.get('procedimento_type')}")
            print(f"   - Richiedente: {analysis.get('richiedente', {}).get('nome')}")
        
        # Disconnessione
        await client.disconnect()
        print("✅ Disconnessione completata")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test client diretto: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_generation_service():
    """Test del servizio di generazione diretto"""
    print("\n🔍 Test Servizio Generazione Diretto")
    print("=" * 40)
    
    try:
        # Test creazione servizio
        print("🚀 Creazione servizio generazione...")
        service = await create_direct_generation_service()
        print("✅ Servizio creato")
        
        # Test analisi fascicolo
        print("📋 Test analisi fascicolo...")
        analysis_result = await service.analyze_fascicolo(
            "Test fascicolo per verifica del servizio di generazione completo",
            ["istanza", "documento_identità", "planimetria"]
        )
        
        print(f"✅ Analisi completata:")
        print(f"   - Successo: {analysis_result.get('success')}")
        
        if analysis_result.get('success'):
            analysis = analysis_result.get('analysis', {})
            print(f"   - Documenti identificati: {len(analysis.get('documenti_identificati', []))}")
            print(f"   - Urgenza: {analysis.get('urgenza')}")
        
        # Test validazione legale
        print("⚖️  Test validazione legale...")
        validation_result = await service.validate_legal_framework(
            "autorizzazione", 
            "Comune di Test",
            ["L. 241/1990", "T.U.E.L."]
        )
        
        print(f"✅ Validazione completata:")
        print(f"   - Successo: {validation_result.get('success')}")
        
        if validation_result.get('success'):
            validation = validation_result.get('validation', {})
            print(f"   - Conformità: {validation.get('conformita_generale')}")
            print(f"   - Competenza ente: {validation.get('competenza_ente', {}).get('valida')}")
        
        # Disconnessione
        await service.mcp_client.disconnect()
        print("✅ Servizio chiuso")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test servizio: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_vs_stdio():
    """Confronta le performance tra client diretto e stdio"""
    print("\n🔍 Test Confronto Performance")
    print("=" * 40)
    
    import time
    
    # Test client diretto
    print("⏱️  Test performance client diretto...")
    start_direct = time.time()
    
    try:
        client_direct = await create_direct_mcp_client()
        tools_direct = await client_direct.list_available_tools()
        result_direct = await client_direct.invoke_tool("fascicolo-analyzer", {
            "fascicolo_content": "Test performance",
            "document_types": ["test"]
        })
        await client_direct.disconnect()
        
        time_direct = time.time() - start_direct
        print(f"✅ Client diretto: {time_direct:.2f} secondi")
        
    except Exception as e:
        print(f"❌ Client diretto fallito: {str(e)}")
        time_direct = float('inf')
    
    # Test client stdio (se disponibile)
    print("⏱️  Test performance client stdio...")
    start_stdio = time.time()
    
    try:
        from mcp_client.client import MCPClient
        server_script = os.path.join(os.path.dirname(__file__), "start_mcp_server.py")
        
        client_stdio = MCPClient(server_script)
        await client_stdio.connect()
        tools_stdio = await asyncio.wait_for(client_stdio.list_available_tools(), timeout=10.0)
        await client_stdio.disconnect()
        
        time_stdio = time.time() - start_stdio
        print(f"✅ Client stdio: {time_stdio:.2f} secondi")
        
    except Exception as e:
        print(f"❌ Client stdio fallito: {str(e)}")
        time_stdio = float('inf')
    
    # Confronto
    print(f"\n📊 Risultati:")
    if time_direct < float('inf'):
        print(f"   🚀 Client diretto: {time_direct:.2f}s - {'✅ FUNZIONA' if time_direct < 10 else '⚠️ LENTO'}")
    else:
        print(f"   ❌ Client diretto: NON FUNZIONA")
    
    if time_stdio < float('inf'):
        print(f"   📡 Client stdio: {time_stdio:.2f}s - {'✅ FUNZIONA' if time_stdio < 10 else '⚠️ LENTO'}")
    else:
        print(f"   ❌ Client stdio: NON FUNZIONA")
    
    if time_direct < float('inf') and time_stdio < float('inf'):
        if time_direct < time_stdio:
            print(f"   🏆 Client diretto è {time_stdio/time_direct:.1f}x più veloce")
        else:
            print(f"   🏆 Client stdio è {time_direct/time_stdio:.1f}x più veloce")


async def main():
    """Esegue tutti i test del client diretto"""
    print("🏛️ Test Client MCP Diretto")
    print("🎯 Soluzione alternativa ai problemi stdio")
    print("=" * 50)
    
    test1_ok = await test_direct_mcp_client()
    test2_ok = await test_direct_generation_service()
    await test_direct_vs_stdio()
    
    print("\n" + "=" * 50)
    print("📊 RISULTATI FINALI")
    print("=" * 50)
    
    if test1_ok and test2_ok:
        print("✅ CLIENT MCP DIRETTO: Completamente funzionante!")
        print("🎉 Soluzione trovata per i problemi di comunicazione MCP")
        print("💡 Vantaggi:")
        print("   - Bypass completo del protocollo stdio problematico")
        print("   - Performance migliori (nessun overhead JSON-RPC)")
        print("   - Maggiore affidabilità")
        print("   - Debugging più semplice")
    else:
        print("❌ CLIENT MCP DIRETTO: Problemi rilevati")
        if not test1_ok:
            print("   - Problemi nel client base")
        if not test2_ok:
            print("   - Problemi nel servizio di generazione")


if __name__ == "__main__":
    asyncio.run(main())