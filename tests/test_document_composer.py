"""
Test specifico per debuggare il problema del document-composer
"""
import asyncio
import json
import sys
import os

# Aggiungi i path necessari
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, current_dir)

from mcp_client.direct_client import DirectMCPClient
from core.models import FascicoloData
from datetime import datetime

def make_json_serializable(obj):
    """Converte oggetti non JSON serializzabili"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, 'dict'):
        return {k: make_json_serializable(v) for k, v in obj.dict().items()}
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    return obj

async def test_document_composer():
    """Test isolato del document-composer"""
    
    print("🔍 Test del document-composer...")
    
    # Crea il client diretto
    client = DirectMCPClient()
    
    # Test con sezioni semplici
    test_sections = {
        "premesse": "Test delle premesse",
        "considerato": "Test dei considerato",
        "visto": "Test dei visto",
        "dispositivo": "Test del dispositivo"
    }
    
    test_template_id = "determina_standard"
    test_ente_metadata = {
        "nome": "Comune di Test",
        "codice": "TEST001",
        "regione": "Test Region"
    }
    
    try:
        print("📤 Chiamata al document-composer...")
        print(f"   - Sezioni: {list(test_sections.keys())}")
        print(f"   - Template: {test_template_id}")
        
        result = await client.invoke_tool(
            "document-composer",
            {
                "sections": test_sections,
                "template_id": test_template_id,
                "ente_metadata": test_ente_metadata
            }
        )
        
        print("📥 Risposta ricevuta:")
        print(f"   - Tipo: {type(result)}")
        print(f"   - Contenuto: {result}")
        
        if isinstance(result, dict) and result.get("success"):
            print("✅ Document-composer funziona correttamente")
            return True
        else:
            print("❌ Document-composer ha restituito un errore")
            print(f"   - Dettagli errore: {result.get('error', 'Errore sconosciuto')}")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante il test del document-composer: {str(e)}")
        print(f"   - Tipo errore: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_simple_generation():
    """Test di una generazione più semplice"""
    
    print("\n🔍 Test di generazione semplificata...")
    
    # Crea dati di test più semplici
    from core.models import AnagraficaRichiedente, ProcedimentoType, DocumentReference, DocumentType
    
    richiedente = AnagraficaRichiedente(
        nome="Mario",
        cognome="Rossi",
        codice_fiscale="RSSMRA80A01H501X",
        email="mario.rossi@example.com"
    )
    
    documento = DocumentReference(
        id="doc001",
        nome="istanza.pdf",
        tipo=DocumentType.ISTANZA,
        percorso="/uploads/istanza.pdf",
        dimensione=1024,
        data_caricamento=datetime.now(),
        contenuto_estratto="Richiesta di autorizzazione"
    )
    
    fascicolo_data = FascicoloData(
        id="FASC001",
        numero_protocollo="PROT/001",
        data_apertura=datetime.now(),
        procedimento_type=ProcedimentoType.AUTORIZZAZIONE,
        richiedente=richiedente,
        documenti=[documento],
        note="Test di generazione semplice"
    )
    
    ente_metadata = {
        "nome": "Comune di Test",
        "codice": "TEST001",
        "regione": "Test Region"
    }
    
    client = DirectMCPClient()
    
    try:
        # 1. Test content-generator con dati semplici
        print("📤 Test content-generator...")
        
        # Converte i dati in formato JSON serializzabile
        fascicolo_serializable = make_json_serializable(fascicolo_data)
        
        content_result = await client.invoke_tool(
            "content-generator",
            {
                "section_type": "premesse",
                "context_data": {
                    "fascicolo": fascicolo_serializable,
                    "ente": ente_metadata
                },
                "template_style": "standard"
            }
        )
        
        print(f"📥 Content-generator result: {content_result}")
        
        if not content_result.get("success"):
            print("❌ Content-generator fallito")
            return False
            
        # 2. Test document-composer con risultato del content-generator
        print("📤 Test document-composer con contenuto generato...")
        
        simple_sections = {
            "premesse": content_result.get("content", "Contenuto di test")
        }
        
        compose_result = await client.invoke_tool(
            "document-composer",
            {
                "sections": simple_sections,
                "template_id": "determina_standard",
                "ente_metadata": ente_metadata
            }
        )
        
        print(f"📥 Document-composer result: {compose_result}")
        
        if compose_result.get("success"):
            print("✅ Generazione semplificata completata con successo")
            return True
        else:
            print("❌ Generazione semplificata fallita")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante la generazione semplificata: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Debug del Document-Composer\n")
    
    # Test 1: Document-composer isolato
    success1 = await test_document_composer()
    
    # Test 2: Generazione semplificata
    success2 = await test_simple_generation()
    
    print(f"\n📊 Risultati:")
    print(f"   - Document-composer isolato: {'✅' if success1 else '❌'}")
    print(f"   - Generazione semplificata: {'✅' if success2 else '❌'}")
    
    if success1 and success2:
        print("\n🎉 Tutti i test sono passati!")
    else:
        print("\n⚠️  Alcuni test sono falliti - serve debug aggiuntivo")

if __name__ == "__main__":
    asyncio.run(main())