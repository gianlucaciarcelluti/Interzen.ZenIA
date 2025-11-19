"""
Test del PDF di esempio per verificare le correzioni
"""
import asyncio
import sys
import os

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from core.document_processor import DocumentProcessor
from mcp_client.direct_client import create_direct_generation_service
from core.models import *
from datetime import datetime

async def test_pdf_example():
    """Test del PDF di esempio con le correzioni applicate"""
    
    print("🔍 Test PDF di Esempio - Istanza Autorizzazione Scarico Acque\n")
    
    # Path al PDF di test
    pdf_path = "tests/Istanza per Autorizzazione Scarico Acque.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF non trovato: {pdf_path}")
        return False
    
    try:
        # 1. Elabora il PDF
        print("📄 Elaborazione PDF...")
        processor = DocumentProcessor()
        pdf_content = processor.extract_text_from_pdf(pdf_path)
        print(f"✅ Testo estratto: {len(pdf_content)} caratteri")
        print(f"📝 Prime 200 caratteri: {pdf_content[:200]}...")
        
        # 2. Crea fascicolo
        print("\n📁 Creazione fascicolo...")
        
        richiedente = AnagraficaRichiedente(
            nome="Test",
            cognome="User", 
            codice_fiscale="TSTUSER80A01H501X"
        )
        
        documento = DocumentReference(
            id="doc_pdf_test",
            nome="Istanza per Autorizzazione Scarico Acque.pdf",
            tipo=DocumentType.ISTANZA,
            percorso=pdf_path,
            dimensione=os.path.getsize(pdf_path),
            data_caricamento=datetime.now(),
            contenuto_estratto=pdf_content
        )
        
        fascicolo_data = FascicoloData(
            id="FASC_PDF_TEST",
            numero_protocollo="PROT/PDF/001",
            data_apertura=datetime.now(),
            procedimento_type=ProcedimentoType.AUTORIZZAZIONE,
            richiedente=richiedente,
            documenti=[documento],
            note="Test PDF di esempio"
        )
        
        ente_metadata = {
            "nome": "Comune di Test",
            "codice": "TEST001", 
            "regione": "Test Region"
        }
        
        # 3. Test generazione con correzioni
        print("\n🚀 Test generazione con correzioni applicate...")
        
        service = await create_direct_generation_service()
        
        result = await service.generate_complete_determina(fascicolo_data, ente_metadata)
        
        print(f"\n📊 Risultato:")
        print(f"   - Tipo: {type(result)}")
        
        if isinstance(result, dict):
            print(f"   - Success: {result.get('success', 'N/A')}")
            if not result.get('success'):
                print(f"   - Error: {result.get('error', 'N/A')}")
        else:
            print(f"   - Status: {result.status}")
            if result.status == GenerationStatus.ERROR:
                print(f"   - Error: {result.error_message}")
            elif result.status == GenerationStatus.GENERATED:
                print("   - ✅ Generazione completata con successo!")
                if hasattr(result, 'validation_results'):
                    print(f"   - Validazioni: {len(result.validation_results)}")
                    for val in result.validation_results[:3]:  # Prime 3
                        print(f"     • {val.section}: {val.severity} - {val.passed}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Test Correzioni PDF di Esempio\n")
    
    success = await test_pdf_example()
    
    if success:
        print("\n🎉 Test completato!")
        print("💡 Controlla che:")
        print("   1. Non ci siano errori di validazione severity")
        print("   2. Il progresso tracking funzioni correttamente")
    else:
        print("\n⚠️ Test fallito - controlla i dettagli sopra")

if __name__ == "__main__":
    asyncio.run(main())