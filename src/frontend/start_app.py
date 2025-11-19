"""
Script di avvio per l'applicazione Streamlit.
"""

import os
import sys
import subprocess

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config

def main():
    """Avvia l'applicazione Streamlit"""
    print("🚀 Avvio dell'applicazione Streamlit...")
    print(f"🌐 Porta: {config.STREAMLIT_PORT}")
    print(f"📡 Ollama URL: {config.OLLAMA_BASE_URL}")
    print(f"🤖 Modello: {config.OLLAMA_MODEL}")
    
    # Path al file dell'app
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    # Comandi Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port", str(config.STREAMLIT_PORT),
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "light"
    ]
    
    try:
        print("\n📱 Aprendo l'applicazione nel browser...")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Applicazione fermata dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'avvio: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
