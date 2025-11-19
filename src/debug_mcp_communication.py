"""
Test di debugging per vedere esattamente cosa succede nella comunicazione MCP.
Questo test mostra la comunicazione raw tra client e server.
"""

import asyncio
import json
import sys
import os
import logging

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging per vedere i dettagli
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def debug_mcp_communication():
    """Debug della comunicazione MCP a basso livello"""
    print("🔍 DEBUG: Comunicazione MCP Raw")
    print("=" * 50)
    
    # Script del server
    server_script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "start_mcp_server.py"
    )
    
    # Avvia il processo del server
    import sys
    python_path = sys.executable
    
    src_dir = os.path.dirname(server_script_path)
    env = os.environ.copy()
    env['PYTHONPATH'] = src_dir
    
    print(f"🚀 Avvio server MCP: {server_script_path}")
    
    process = await asyncio.create_subprocess_exec(
        python_path, server_script_path,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env
    )
    
    print(f"📡 Processo avviato con PID: {process.pid}")
    
    try:
        # Aspetta che il server sia stabile e leggi stderr per errori
        print("⏳ Aspetto che il server si stabilizzi...")
        
        # Leggi stderr del server per 3 secondi per vedere eventuali errori di avvio
        start_time = asyncio.get_event_loop().time()
        server_ready = False
        
        while asyncio.get_event_loop().time() - start_time < 3.0:
            if process.stderr:
                try:
                    line = await asyncio.wait_for(process.stderr.readline(), timeout=0.5)
                    if line:
                        error_line = line.decode().strip()
                        if error_line:
                            print(f"Server stderr: {error_line}")
                            if "error" in error_line.lower() or "traceback" in error_line.lower():
                                print(f"❌ Errore critico del server: {error_line}")
                                return False
                except asyncio.TimeoutError:
                    pass
            
            # Controlla se il processo è crashato
            if process.returncode is not None:
                print(f"❌ Server crashato con codice: {process.returncode}")
                return False
            
            await asyncio.sleep(0.1)
        
        if process.returncode is None:
            server_ready = True
            print("✅ Server sembra essere stabile")
        
        print("\n📤 FASE 1: Test ping/handshake")
        
        # Test 1: Prova un messaggio di ping semplice
        ping_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
            "params": {}
        }
        
        ping_json = json.dumps(ping_msg) + '\n'
        print(f"Invio: {ping_json.strip()}")
        
        if process.stdin:
            process.stdin.write(ping_json.encode())
            await process.stdin.drain()
        
        # Leggi risposta con timeout
        try:
            if process.stdout:
                response_line = await asyncio.wait_for(process.stdout.readline(), timeout=3.0)
                if response_line:
                    response_text = response_line.decode().strip()
                    print(f"Risposta: {response_text}")
                    try:
                        response_json = json.loads(response_text)
                        print(f"JSON valido: {response_json}")
                    except json.JSONDecodeError:
                        print(f"❌ Risposta non è JSON valido")
                else:
                    print("❌ Nessuna risposta ricevuta")
        except asyncio.TimeoutError:
            print("❌ Timeout nella risposta")
        
        print("\n📤 FASE 2: Test initialize")
        
        # Test 2: Prova il protocollo MCP standard
        init_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "debug-client",
                    "version": "1.0.0"
                }
            }
        }
        
        init_json = json.dumps(init_msg) + '\n'
        print(f"Invio: {init_json.strip()}")
        
        if process.stdin:
            process.stdin.write(init_json.encode())
            await process.stdin.drain()
        
        try:
            if process.stdout:
                response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
                if response_line:
                    response_text = response_line.decode().strip()
                    print(f"Risposta: {response_text}")
                    try:
                        response_json = json.loads(response_text)
                        print(f"JSON valido: {response_json}")
                        
                        # Se l'inizializzazione funziona, prova tools/list
                        if "result" in response_json:
                            print("\n📤 FASE 3: Test tools/list")
                            
                            tools_msg = {
                                "jsonrpc": "2.0",
                                "id": 3,
                                "method": "tools/list",
                                "params": {}
                            }
                            
                            tools_json = json.dumps(tools_msg) + '\n'
                            print(f"Invio: {tools_json.strip()}")
                            
                            if process.stdin:
                                process.stdin.write(tools_json.encode())
                                await process.stdin.drain()
                            
                            response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
                            if response_line:
                                response_text = response_line.decode().strip()
                                print(f"Risposta: {response_text}")
                                try:
                                    response_json = json.loads(response_text)
                                    print(f"JSON valido: {response_json}")
                                    
                                    if "result" in response_json and "tools" in response_json["result"]:
                                        tools = response_json["result"]["tools"]
                                        print(f"✅ SUCCESSO! Trovati {len(tools)} tools:")
                                        for tool in tools:
                                            print(f"   - {tool.get('name', 'senza nome')}")
                                        return True
                                except json.JSONDecodeError:
                                    print(f"❌ Risposta tools/list non è JSON valido")
                    except json.JSONDecodeError:
                        print(f"❌ Risposta initialize non è JSON valido")
                else:
                    print("❌ Nessuna risposta a initialize")
        except asyncio.TimeoutError:
            print("❌ Timeout nella risposta a initialize")
        
        print("\n📤 FASE 4: Controllo stderr del server")
        
        # Leggi eventuali errori dal server
        if process.stderr:
            try:
                while True:
                    line = await asyncio.wait_for(process.stderr.readline(), timeout=1.0)
                    if line:
                        error_line = line.decode().strip()
                        if error_line:
                            print(f"Server stderr: {error_line}")
                    else:
                        break
            except asyncio.TimeoutError:
                print("Nessun errore da stderr")
    
    except Exception as e:
        print(f"❌ Errore durante il debug: {str(e)}")
        return False
    
    finally:
        print(f"\n🛑 Chiusura processo server...")
        if process:
            process.terminate()
            await process.wait()
            print(f"Processo terminato con codice: {process.returncode}")
    
    return False


async def main():
    """Esegue il debug della comunicazione MCP"""
    print("🏛️ DEBUG MCP Communication")
    print("🎯 Analisi dettagliata della comunicazione con il server")
    print("=" * 60)
    
    success = await debug_mcp_communication()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ COMUNICAZIONE MCP: Funzionante!")
        print("💡 Il problema potrebbe essere nei timeout o nella logica del client")
    else:
        print("❌ COMUNICAZIONE MCP: Problemi identificati")
        print("💡 Il server MCP non risponde come previsto al protocollo")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)