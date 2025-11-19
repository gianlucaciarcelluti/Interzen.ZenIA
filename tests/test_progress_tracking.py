"""
Test del sistema di progress tracking
"""
import asyncio
import sys
import os

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from mcp_client.direct_client import create_direct_generation_service
from core.models import *
from datetime import datetime

class MockProgressTracker:
    """Mock del progress tracker per test"""
    
    def __init__(self):
        self.progress_history = []
    
    def update_progress(self, tool_name, status, details=""):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.progress_history.append({
            "timestamp": timestamp,
            "tool": tool_name,
            "status": status,
            "details": details
        })
        print(f"[{timestamp}] {tool_name}: {status}")
        if details:
            print(f"    └─ {details}")

async def test_progress_tracking():
    """Test del sistema di tracking con un fascicolo semplice"""
    
    print("🔍 Test Progress Tracking Sistema\n")
    
    # Setup mock data
    richiedente = AnagraficaRichiedente(
        nome="Mario",
        cognome="Rossi", 
        codice_fiscale="RSSMRA80A01H501X",
        email="mario.rossi@test.com"
    )
    
    documento = DocumentReference(
        id="doc001",
        nome="richiesta.pdf",
        tipo=DocumentType.ISTANZA,
        percorso="/test/richiesta.pdf",
        dimensione=1024,
        data_caricamento=datetime.now(),
        contenuto_estratto="Richiesta di autorizzazione commerciale per apertura negozio abbigliamento"
    )
    
    fascicolo_data = FascicoloData(
        id="FASC_PROGRESS_TEST",
        numero_protocollo="PROT/TEST/001",
        data_apertura=datetime.now(),
        procedimento_type=ProcedimentoType.AUTORIZZAZIONE,
        richiedente=richiedente,
        documenti=[documento],
        note="Test progress tracking"
    )
    
    ente_metadata = {
        "nome": "Comune di Test",
        "codice": "TEST001",
        "regione": "Test Region"
    }
    
    # Mock progress tracker
    tracker = MockProgressTracker()
    
    try:
        print("📤 Creazione servizio di generazione...")
        service = await create_direct_generation_service()
        
        print("🔧 Setup progress tracking...")
        
        # Wrapper per il tracking
        original_invoke = service.mcp_client.invoke_tool
        
        async def tracked_invoke_tool(tool_name, parameters):
            tool_display_names = {
                "fascicolo-analyzer": "📁 Analisi Fascicolo",
                "legal-framework-validator": "⚖️ Validazione Normativa", 
                "content-generator": "📝 Generazione Contenuti",
                "document-composer": "📄 Composizione Documento",
                "compliance-checker": "✅ Verifica Conformità"
            }
            
            display_name = tool_display_names.get(tool_name, f"🔧 {tool_name}")
            
            # Avvia tool
            tracker.update_progress(display_name, "🚀 Iniziato", f"Parametri: {len(str(parameters))} caratteri")
            
            try:
                # Esegui il tool originale
                result = await original_invoke(tool_name, parameters)
                
                # Analizza il risultato
                details = ""
                if isinstance(result, dict):
                    if result.get("success"):
                        details = "Eseguito con successo"
                    else:
                        details = f"Errore: {result.get('error', 'Sconosciuto')}"
                
                tracker.update_progress(display_name, "✅ Completato", details)
                return result
                
            except Exception as e:
                tracker.update_progress(display_name, "❌ Errore", str(e))
                raise
        
        # Sostituisci il metodo
        service.mcp_client.invoke_tool = tracked_invoke_tool
        
        print("\n🚀 Avvio generazione con tracking...")
        tracker.update_progress("Sistema", "🚀 Iniziato", "Avvio processo generazione")
        
        # Esegui generazione
        result = await service.generate_complete_determina(fascicolo_data, ente_metadata)
        
        tracker.update_progress("Sistema", "✅ Completato", "Generazione terminata")
        
        print(f"\n📊 Risultato:")
        print(f"   - Status: {result.status if hasattr(result, 'status') else 'N/A'}")
        print(f"   - Success: {result.get('success', 'N/A') if isinstance(result, dict) else 'N/A'}")
        
        print(f"\n📈 Progress History ({len(tracker.progress_history)} passi):")
        for i, step in enumerate(tracker.progress_history, 1):
            print(f"   {i}. [{step['timestamp']}] {step['tool']}: {step['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test: {str(e)}")
        tracker.update_progress("Sistema", "❌ Errore", str(e))
        return False

async def main():
    print("🚀 Test Sistema Progress Tracking\n")
    
    success = await test_progress_tracking()
    
    if success:
        print("\n🎉 Progress tracking funziona correttamente!")
        print("💡 Il frontend ora mostrerà tutti i passi della generazione in tempo reale")
    else:
        print("\n⚠️ Problemi nel progress tracking - verifica i log")

if __name__ == "__main__":
    asyncio.run(main())