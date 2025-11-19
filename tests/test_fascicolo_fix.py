#!/usr/bin/env python3
"""
Test specifico per fascicolo_analyzer con il nuovo parsing JSON migliorato
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

async def test_fascicolo_analyzer():
    """Test della funzione fascicolo_analyzer con il nuovo parsing JSON"""
    
    print("🧪 Test fascicolo_analyzer con parsing JSON migliorato")
    print("=" * 60)
    
    # Crea client Ollama
    ollama_client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
    tools = DeterminaTools(ollama_client)
    
    # Usa un contenuto di test simile a quello che potrebbe causare problemi
    test_content = """
    OGGETTO: Richiesta di autorizzazione allo scarico di acque reflue industriali
    
    DITTA: Industrie Alimentari Rossi S.r.l.
    CODICE FISCALE: 12345678901
    SEDE LEGALE: Via Giuseppe Verdi, 45 - 00185 Roma (RM)
    TELEFONO: 06-12345678
    EMAIL: info@industrierossi.it
    PEC: industrierossi@pec.it
    
    La società richiede l'autorizzazione per lo scarico di acque reflue derivanti 
    dal processo di lavorazione alimentare presso il proprio stabilimento.
    
    DOCUMENTI ALLEGATI:
    - Relazione tecnica
    - Planimetria impianto
    - Analisi chimiche acque
    """
    
    document_types = ["istanza", "relazione_tecnica", "planimetria"]
    
    print("📋 Parametri test:")
    print(f"   Lunghezza contenuto: {len(test_content)} caratteri")
    print(f"   Tipi documento: {document_types}")
    print()
    
    try:
        print("🔍 Test fascicolo_analyzer...")
        result = await tools.fascicolo_analyzer(test_content, document_types)
        
        print("✅ Risultato fascicolo_analyzer:")
        print(f"   Success: {result.get('success', False)}")
        
        if result.get('success'):
            analysis = result.get('analysis', {})
            print(f"   Tipo procedimento: {analysis.get('procedimento_type', 'N/A')}")
            print(f"   Richiedente: {analysis.get('richiedente', {}).get('nome', 'N/A')}")
            print(f"   Oggetto: {analysis.get('oggetto_richiesta', 'N/A')[:100]}...")
        else:
            print(f"   Error: {result.get('error', 'N/A')}")
            if result.get('raw_response'):
                print(f"   Raw response: {result['raw_response'][:200]}...")
        
        print()
        
    except Exception as e:
        print(f"❌ Errore in fascicolo_analyzer: {str(e)}")
        print()
    
    print("🎯 Test completato!")

if __name__ == "__main__":
    asyncio.run(test_fascicolo_analyzer())