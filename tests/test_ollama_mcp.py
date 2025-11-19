"""
Test rapido per verificare il funzionamento di Ollama con il server MCP
"""
import asyncio
import sys
import os

# Aggiungi il path per gli import
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from core.config import config
from mcp_server.server import OllamaClient

async def test_ollama_basic():
    """Test base di Ollama"""
    print("🔍 Test funzionamento Ollama...")
    
    client = OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
    
    try:
        # Test molto semplice
        print("📤 Test generazione semplice...")
        response = await client.generate(
            "Rispondi con un JSON semplice: {'test': 'ok', 'status': 'funzionante'}",
            "Sei un assistente che risponde sempre in JSON valido."
        )
        
        print(f"📥 Risposta ricevuta: {response}")
        
        # Test con analisi fascicolo simulata
        print("\n📤 Test analisi fascicolo simulata...")
        fascicolo_content = """
        RICHIESTA DI AUTORIZZAZIONE
        
        Il sottoscritto Mario Rossi, nato a Roma il 01/01/1980, 
        codice fiscale RSSMRA80A01H501X, residente in Via Roma 123,
        chiede l'autorizzazione per l'apertura di un'attività commerciale.
        
        Documenti allegati:
        - Documento di identità
        - Certificato di agibilità
        - Planimetria locale
        """
        
        system_prompt = """
        Sei un esperto di procedure amministrative italiane. 
        Analizza il fascicolo ed estrai le informazioni in formato JSON.
        """
        
        prompt = f"""
        Analizza questo fascicolo:
        
        {fascicolo_content}
        
        Rispondi in formato JSON con questa struttura:
        {{
            "procedimento_type": "tipo_procedimento",
            "richiedente": {{
                "nome": "nome",
                "cognome": "cognome"
            }},
            "oggetto_richiesta": "descrizione"
        }}
        """
        
        response = await client.generate(prompt, system_prompt)
        print(f"📥 Risposta analisi: {response[:300]}...")
        
        print("✅ Test Ollama completato con successo!")
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test Ollama: {str(e)}")
        return False
    finally:
        await client.client.aclose()

async def main():
    print("🚀 Test Diagnostico Ollama MCP\n")
    success = await test_ollama_basic()
    
    if success:
        print("\n🎉 Ollama funziona correttamente!")
        print("💡 Il problema potrebbe essere:")
        print("   - Timeout troppo brevi")
        print("   - Prompt troppo complessi")
        print("   - Carico del sistema")
    else:
        print("\n⚠️ Problema con Ollama identificato!")
        print("💡 Possibili soluzioni:")
        print("   - Verifica che Ollama sia in esecuzione")
        print("   - Controlla il modello configurato")
        print("   - Verifica la connessione di rete")

if __name__ == "__main__":
    asyncio.run(main())