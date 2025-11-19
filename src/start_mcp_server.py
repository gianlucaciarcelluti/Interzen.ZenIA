"""
Script di avvio per il MCP Server.
Può essere utilizzato per avviare il server in modalità standalone.
"""

import asyncio
import logging
import sys
import os

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.server import main
from core.config import config

if __name__ == "__main__":
    print("🚀 Avvio MCP Server per Generazione Determine...")
    print(f"📡 Ollama URL: {config.OLLAMA_BASE_URL}")
    print(f"🤖 Modello: {config.OLLAMA_MODEL}")
    print("📝 Tools disponibili:")
    print("   - fascicolo-analyzer")
    print("   - legal-framework-validator")
    print("   - content-generator")
    print("   - document-composer")
    print("   - compliance-checker")
    print("\n⏳ Avvio del server...")
    
    try:
        print("🟢 Server MCP avviato e in ascolto...")
        print("📥 In attesa di connessioni dai client MCP...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server fermato dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante l'avvio: {str(e)}")
        sys.exit(1)
