"""
Test specifico per simulare il comportamento del frontend nella verifica dello stato MCP.
Questo test simula esattamente quello che fa il frontend quando clicchi su "Verifica stato MCP".
"""

import asyncio
import sys
import os
import time

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_client.client import create_mcp_client


async def test_frontend_mcp_behavior():
    """
    Simula esattamente il comportamento del frontend quando verifica lo stato MCP
    """
    print("🔍 Test comportamento frontend MCP...")
    print("=" * 50)
    
    # Script del server (stesso path usato dal frontend)
    server_script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "start_mcp_server.py"
    )
    
    print(f"📂 Script server MCP: {server_script_path}")
    print(f"📁 Esistenza file: {'✅ OK' if os.path.exists(server_script_path) else '❌ NON TROVATO'}")
    
    client = None
    start_time = time.time()
    
    try:
        print("\n🚀 Avvio connessione MCP...")
        print("⏱️  Timeout configurato: 15 secondi")
        
        # Test con timeout aumentato (come nel frontend aggiornato)
        client = await asyncio.wait_for(
            create_mcp_client(server_script_path), 
            timeout=15.0
        )
        
        connection_time = time.time() - start_time
        print(f"✅ Connessione riuscita in {connection_time:.2f} secondi")
        
        print("\n🔧 Test listing tools...")
        print("⏱️  Timeout configurato: 10 secondi")
        
        tools_start = time.time()
        tools = await asyncio.wait_for(
            client.list_available_tools(), 
            timeout=10.0
        )
        
        tools_time = time.time() - tools_start
        print(f"✅ Listing tools riuscito in {tools_time:.2f} secondi")
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 Test completato con successo!")
        print(f"⏱️  Tempo totale: {total_time:.2f} secondi")
        print(f"🔧 Tools trovati: {len(tools)}")
        
        if tools:
            print("📋 Lista tools:")
            for i, tool in enumerate(tools[:5], 1):  # Primi 5 per non appesantire
                print(f"   {i}. {tool}")
            if len(tools) > 5:
                print(f"   ... e altri {len(tools) - 5} tools")
        
        return {
            'success': True,
            'connection_time': connection_time,
            'tools_time': tools_time,
            'total_time': total_time,
            'tools_count': len(tools),
            'error': None
        }
        
    except asyncio.TimeoutError as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Timeout dopo {elapsed:.2f} secondi")
        
        if elapsed < 5:
            print("💡 Il timeout è avvenuto molto rapidamente.")
            print("   Possibili cause:")
            print("   - Server MCP non si avvia correttamente")
            print("   - Problemi con lo script di avvio")
            print("   - Ollama non è in esecuzione")
        elif elapsed < 15:
            print("💡 Timeout durante la connessione al server.")
            print("   Possibili cause:")
            print("   - Server MCP impiega troppo tempo ad avviarsi")
            print("   - Problemi di caricamento del modello Ollama")
        else:
            print("💡 Timeout durante il listing dei tools.")
            print("   Possibili cause:")
            print("   - Comunicazione MCP lenta")
            print("   - Server sovraccarico")
        
        return {
            'success': False,
            'connection_time': elapsed,
            'tools_time': None,
            'total_time': elapsed,
            'tools_count': 0,
            'error': f'Timeout dopo {elapsed:.2f} secondi'
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = str(e)
        
        print(f"\n❌ Errore dopo {elapsed:.2f} secondi: {error_msg}")
        
        # Analisi dell'errore
        if "WouldBlock" in error_msg or "CancelledError" in error_msg:
            print("💡 Server MCP in modalità stdio (normale per MCP)")
            print("   Questo è il comportamento atteso, non un errore")
        elif "Connection" in error_msg:
            print("💡 Problema di connessione")
            print("   - Verifica che Ollama sia in esecuzione")
            print("   - Controlla la configurazione di rete")
        elif "Permission" in error_msg:
            print("💡 Problema di permessi")
            print("   - Verifica i permessi del file script")
            print("   - Controlla l'ambiente virtuale")
        else:
            print("💡 Errore generico, controlla i log")
        
        return {
            'success': False,
            'connection_time': elapsed,
            'tools_time': None,
            'total_time': elapsed,
            'tools_count': 0,
            'error': error_msg
        }
        
    finally:
        if client:
            try:
                print("\n🔌 Disconnessione...")
                await client.disconnect()
                print("✅ Disconnessione completata")
            except Exception as e:
                print(f"⚠️  Errore durante disconnessione: {str(e)}")


async def test_multiple_attempts():
    """
    Testa connessioni multiple per simulare click ripetuti nel frontend
    """
    print("\n" + "=" * 60)
    print("🔄 Test connessioni multiple (simula click ripetuti)")
    print("=" * 60)
    
    results = []
    
    for attempt in range(3):
        print(f"\n🔄 Tentativo {attempt + 1}/3...")
        
        result = await test_frontend_mcp_behavior()
        results.append(result)
        
        if result['success']:
            print(f"✅ Tentativo {attempt + 1}: SUCCESSO")
        else:
            print(f"❌ Tentativo {attempt + 1}: FALLITO - {result['error']}")
        
        # Pausa tra i tentativi
        if attempt < 2:
            print("⏳ Pausa di 2 secondi...")
            await asyncio.sleep(2)
    
    # Statistiche finali
    print("\n" + "=" * 40)
    print("📊 STATISTICHE FINALI")
    print("=" * 40)
    
    successful = sum(1 for r in results if r['success'])
    
    print(f"✅ Tentativi riusciti: {successful}/3")
    print(f"❌ Tentativi falliti: {3 - successful}/3")
    
    if successful > 0:
        avg_time = sum(r['total_time'] for r in results if r['success']) / successful
        print(f"⏱️  Tempo medio (successi): {avg_time:.2f} secondi")
    
    return results


def main():
    """Esegue tutti i test"""
    print("🏛️ Test Frontend MCP - Diagnostica Problemi")
    print("🎯 Simula esattamente il comportamento del frontend")
    print("=" * 60)
    
    try:
        # Test singolo
        result = asyncio.run(test_frontend_mcp_behavior())
        
        # Test multipli
        results = asyncio.run(test_multiple_attempts())
        
        print("\n" + "=" * 60)
        print("🎉 DIAGNOSI COMPLETA")
        print("=" * 60)
        
        if result['success']:
            print("✅ Il sistema MCP funziona correttamente!")
            print("💡 Se vedi ancora problemi nel frontend:")
            print("   1. Ricarica la pagina del browser")
            print("   2. Aspetta qualche secondo prima di cliccare")
            print("   3. I timeout sono stati aumentati")
        else:
            print("❌ Problema identificato nel sistema MCP")
            print("🔧 Azioni consigliate:")
            print("   1. Verifica che Ollama sia in esecuzione:")
            print("      ollama serve")
            print("   2. Controlla i log dell'applicazione")
            print("   3. Riavvia l'applicazione")
        
    except Exception as e:
        print(f"\n❌ Errore durante i test: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)