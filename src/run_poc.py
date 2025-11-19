#!/usr/bin/env python3
"""
Script principale di avvio del POC Determina Generator.
Questo script configura l'ambiente e avvia l'applicazione Streamlit.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_ollama_connection():
    """Verifica che Ollama sia in esecuzione"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama connesso - {len(models)} modelli disponibili")

            # Verifica se llama3.2:1b è disponibile
            llama_available = any("llama3.2:1b" in model.get("name", "") for model in models)
            if llama_available:
                print("✅ Modello llama3.2:1b disponibile")
            else:
                print("⚠️  Modello llama3.2:1b non trovato. Installazione in corso...")
                subprocess.run(["ollama", "pull", "llama3.2:1b"])
            
            return True
        else:
            print("❌ Ollama non risponde correttamente")
            return False
    except Exception as e:
        print(f"❌ Impossibile connettersi a Ollama: {str(e)}")
        print("💡 Assicurati che Ollama sia in esecuzione su http://localhost:11434")
        return False

def install_dependencies():
    """Installa le dipendenze Python"""
    print("📦 Installazione dipendenze...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dipendenze installate con successo")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nell'installazione delle dipendenze: {str(e)}")
        return False

def create_env_file():
    """Crea il file .env se non esiste"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creazione file .env...")
        env_file.write_text(env_example.read_text())
        print("✅ File .env creato da .env.example")

def main():
    parser = argparse.ArgumentParser(description="POC Generatore Determine Amministrative")
    parser.add_argument("--skip-deps", action="store_true", help="Salta l'installazione delle dipendenze")
    parser.add_argument("--skip-ollama-check", action="store_true", help="Salta il controllo Ollama")
    parser.add_argument("--port", type=int, default=8501, help="Porta per Streamlit (default: 8501)")
    
    args = parser.parse_args()
    
    print("🏛️ POC Generatore Determine Amministrative")
    print("=" * 50)
    
    # Verifica directory corrente
    if not Path("requirements.txt").exists():
        print("❌ Eseguire lo script dalla directory src del progetto")
        sys.exit(1)
    
    # Crea file .env
    create_env_file()
    
    # Installa dipendenze
    if not args.skip_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Verifica Ollama
    if not args.skip_ollama_check:
        if not check_ollama_connection():
            print("\n💡 Per avviare Ollama:")
            print("   docker run -d -p 11434:11434 ollama/ollama")
            print("   # oppure se installato localmente:")
            print("   ollama serve")
            sys.exit(1)
    
    # Avvia Streamlit
    print(f"\n🚀 Avvio applicazione Streamlit sulla porta {args.port}...")
    print(f"🌐 L'applicazione sarà disponibile su: http://localhost:{args.port}")
    print("\n⏳ Avvio in corso...")
    
    try:
        subprocess.run([
            "streamlit", "run", "frontend/app.py",
            "--server.port", str(args.port),
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Applicazione fermata dall'utente")
    except FileNotFoundError:
        print("❌ Streamlit non trovato. Installare con: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante l'avvio: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
