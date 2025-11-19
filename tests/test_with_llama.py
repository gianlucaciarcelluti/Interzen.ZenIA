"""
Script per testare con llama3.2:1b
"""
import os

# Imposta il modello
os.environ["OLLAMA_MODEL"] = "llama3.2:1b"

import asyncio
import sys

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from core.document_processor import DocumentProcessor
from mcp_client.direct_client import create_direct_generation_service
from core.models import *
from datetime import datetime

async def test_with_llama():
    print("🚀 Test con llama3.2:1b")
    print(f"📋 Modello configurato: {os.getenv('OLLAMA_MODEL', 'default')}")
    
    # Test veloce
    pdf_path = "tests/Istanza per Autorizzazione Scarico Acque.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF non trovato: {pdf_path}")
        return
    
    try:
        processor = DocumentProcessor()
        pdf_content = processor.extract_text_from_pdf(pdf_path)
        print(f"✅ PDF elaborato: {len(pdf_content)} caratteri")
        
        # Crea fascicolo semplificato
        richiedente = AnagraficaRichiedente(
            nome="Mario", cognome="Rossi", codice_fiscale="RSSMRA80A01H501X"
        )
        
        documento = DocumentReference(
            id="doc_test", nome="test.pdf", tipo=DocumentType.ISTANZA,
            percorso=pdf_path, dimensione=1000, data_caricamento=datetime.now(),
            contenuto_estratto=pdf_content[:2000]  # Limito a 2K caratteri
        )
        
        fascicolo_data = FascicoloData(
            id="TEST", numero_protocollo="TEST/001", data_apertura=datetime.now(),
            procedimento_type=ProcedimentoType.AUTORIZZAZIONE, richiedente=richiedente,
            documenti=[documento], note="Test llama3.2:1b"
        )
        
        ente_metadata = {"nome": "Comune Test", "codice": "TEST", "regione": "Lazio"}
        
        print("\n🔄 Avvio generazione...")
        service = await create_direct_generation_service()
        result = await service.generate_complete_determina(fascicolo_data, ente_metadata)
        
        print(f"\n📊 Risultato: {result.status}")
        if result.status == GenerationStatus.ERROR:
            print(f"❌ Errore: {result.error_message}")
        elif result.status == GenerationStatus.GENERATED:
            print("✅ Generazione completata!")
            print(f"📝 Determina generata con {len(result.validation_results)} validazioni")
        
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    asyncio.run(test_with_llama())