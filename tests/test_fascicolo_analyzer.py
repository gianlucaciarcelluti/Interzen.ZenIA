"""
Test del fascicolo analyzer migliorato
"""
import asyncio
import sys
import os

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from core.config import config
from mcp_server.server import OllamaClient, DeterminaTools

async def test_fascicolo_analyzer():
    """Test dell'analyzer con contenuto realistico"""
    print("🔍 Test Fascicolo Analyzer migliorato...")
    
    # Contenuto di test simile a quello reale
    fascicolo_content = """
    RICHIESTA DI AUTORIZZAZIONE COMMERCIALE
    
    Il sottoscritto MARIO ROSSI, nato a Roma il 15/03/1980, 
    codice fiscale RSSMRA80C15H501X, residente in Via Roma 123, 00100 Roma,
    telefono 06-12345678, email mario.rossi@email.com
    
    CHIEDE
    
    L'autorizzazione per l'apertura di un'attività di vendita al dettaglio di abbigliamento
    presso il locale sito in Via del Corso 456, Roma.
    
    DICHIARA
    
    - Di essere in possesso dei requisiti previsti dalla normativa vigente
    - Di voler aprire un negozio di abbigliamento di 150 mq
    - Di aver ottenuto l'agibilità del locale in data 10/01/2025
    
    DOCUMENTI ALLEGATI:
    1. Documento di identità
    2. Codice fiscale
    3. Certificato di agibilità del locale
    4. Planimetria del negozio
    5. Dichiarazione conformità impianti
    
    RIFERIMENTI NORMATIVI:
    - D.Lgs. 114/1998 (Riforma della disciplina relativa al settore del commercio)
    - Regolamento comunale per il commercio
    
    Data: 12/09/2025
    Firma: Mario Rossi
    """
    
    client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
    tools = DeterminaTools(client)
    
    try:
        print("📤 Avvio analisi fascicolo...")
        
        result = await tools.fascicolo_analyzer(
            fascicolo_content=fascicolo_content,
            document_types=["istanza", "documento_identita", "certificazione", "allegato_tecnico"]
        )
        
        print("📥 Risultato analisi:")
        print(f"   - Success: {result.get('success')}")
        
        if result.get('success'):
            analysis = result.get('analysis', {})
            print(f"   - Tipo procedimento: {analysis.get('procedimento_type', 'N/A')}")
            print(f"   - Richiedente: {analysis.get('richiedente', {})}")
            print(f"   - Oggetto: {analysis.get('oggetto_richiesta', 'N/A')}")
            print("✅ Analisi completata con successo!")
        else:
            error = result.get('error', 'Errore sconosciuto')
            print(f"❌ Errore nell'analisi: {error}")
            
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Eccezione durante il test: {str(e)}")
        return False
    finally:
        await client.client.aclose()

async def main():
    print("🚀 Test Analyzer Migliorato\n")
    
    success = await test_fascicolo_analyzer()
    
    if success:
        print("\n🎉 Il fascicolo analyzer funziona correttamente!")
        print("💡 Le modifiche applicate dovrebbero risolvere il problema timeout")
    else:
        print("\n⚠️ Il problema persiste. Potrebbero servire ulteriori modifiche.")

if __name__ == "__main__":
    asyncio.run(main())