#!/usr/bin/env python3
"""
Test per verificare che le correzioni al parsing JSON funzionino correttamente
"""

import sys
import os
import asyncio
import json
import logging

# Aggiungi il path per importare i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from mcp_server.server import OllamaClient, DeterminaTools
from core.config import config

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_json_parsing():
    """Test delle funzioni che parsano JSON per verificare la gestione degli errori"""
    
    print("🧪 Test del parsing JSON migliorato")
    print("=" * 50)
    
    # Crea client Ollama (anche se non è disponibile)
    ollama_client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
    tools = DeterminaTools(ollama_client)
    
    # Test con dati di input validi
    test_procedimento = "autorizzazione_scarico_acque"
    test_ente = "Comune di Test"
    test_normativa = ["D.Lgs. 152/2006", "Regolamento comunale"]
    
    print("📋 Parametri test:")
    print(f"   Procedimento: {test_procedimento}")
    print(f"   Ente: {test_ente}")
    print(f"   Normativa: {test_normativa}")
    print()
    
    try:
        print("🔍 Test legal_framework_validator...")
        result = await tools.legal_framework_validator(
            test_procedimento,
            test_ente, 
            test_normativa
        )
        
        print("✅ Risultato legal_framework_validator:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Error: {result.get('error', 'N/A')}")
        if result.get('raw_response'):
            print(f"   Raw response: {result['raw_response'][:100]}...")
        print()
        
    except Exception as e:
        print(f"❌ Errore in legal_framework_validator: {str(e)}")
        print()
    
    # Test content_generator
    try:
        print("🔍 Test content_generator...")
        result = await tools.content_generator(
            "premesse",
            {"procedimento": test_procedimento, "ente": test_ente},
            "formale"
        )
        
        print("✅ Risultato content_generator:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Error: {result.get('error', 'N/A')}")
        if result.get('raw_response'):
            print(f"   Raw response: {result['raw_response'][:100]}...")
        print()
        
    except Exception as e:
        print(f"❌ Errore in content_generator: {str(e)}")
        print()
    
    print("🎯 Test completato!")
    print("ℹ️  Nota: È normale che i test falliscano se Ollama non è disponibile.")
    print("   L'importante è che l'errore sia gestito correttamente con logging dettagliato.")

if __name__ == "__main__":
    asyncio.run(test_json_parsing())