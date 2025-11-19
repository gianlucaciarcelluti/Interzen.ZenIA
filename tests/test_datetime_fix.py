"""
Test specifico per verificare la correzione del problema di serializzazione JSON.
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Aggiungi il path del progetto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_client.direct_client import create_direct_generation_service, make_json_serializable
from core.models import *


async def test_json_serialization():
    """Test della funzione di serializzazione JSON"""
    print("🧪 Test Serializzazione JSON")
    print("=" * 40)
    
    # Test oggetti con datetime
    test_data = {
        "data_semplice": datetime.now(),
        "lista_date": [datetime.now(), datetime(2025, 1, 1)],
        "dict_nested": {
            "data_creazione": datetime.now(),
            "meta": {"ultima_modifica": datetime.now()}
        },
        "stringa": "test",
        "numero": 42,
        "booleano": True
    }
    
    print(f"📦 Dati originali: {len(str(test_data))} caratteri")
    
    # Test serializzazione
    try:
        serialized = make_json_serializable(test_data)
        print("✅ Serializzazione riuscita")
        
        # Test che sia effettivamente JSON-serializzabile
        json_str = json.dumps(serialized, indent=2)
        print(f"✅ JSON valido generato: {len(json_str)} caratteri")
        
        # Verifica che le date siano diventate stringhe ISO
        if isinstance(serialized["data_semplice"], str):
            print("✅ Date convertite in stringhe ISO")
        else:
            print("❌ Date non convertite correttamente")
            
        return True
        
    except Exception as e:
        print(f"❌ Errore nella serializzazione: {str(e)}")
        return False


async def test_fascicolo_data_serialization():
    """Test specifico per FascicoloData con datetime"""
    print("\n🧪 Test FascicoloData Serializzazione")
    print("=" * 40)
    
    try:
        # Crea un FascicoloData con datetime
        richiedente = AnagraficaRichiedente(
            nome="Mario",
            cognome="Rossi",
            codice_fiscale="RSSMRA80C15H501X",
            email="mario.rossi@test.com"
        )
        
        documento = DocumentReference(
            id="doc_1",
            nome="test.pdf",
            tipo=DocumentType.ISTANZA,
            percorso="/test/path",
            dimensione=1024,
            data_caricamento=datetime.now(),  # Questo causa il problema
            contenuto_estratto="Contenuto test"
        )
        
        fascicolo = FascicoloData(
            id="fasc_001",
            data_apertura=datetime.now(),  # E anche questo
            procedimento_type=ProcedimentoType.AUTORIZZAZIONE,
            richiedente=richiedente,
            documenti=[documento],
            urgente=False
        )
        
        print("✅ FascicoloData creato")
        
        # Test dict() normale (dovrebbe fallire JSON)
        try:
            fascicolo_dict = fascicolo.dict()
            json.dumps(fascicolo_dict)  # Questo dovrebbe fallire
            print("❌ dict() normale è JSON serializzabile (inaspettato)")
        except TypeError as e:
            print(f"✅ dict() normale fallisce JSON: {str(e)[:50]}...")
        
        # Test con make_json_serializable
        serialized_fascicolo = make_json_serializable(fascicolo)
        json_str = json.dumps(serialized_fascicolo, indent=2)
        print("✅ make_json_serializable risolve il problema")
        print(f"   JSON generato: {len(json_str)} caratteri")
        
        # Verifica campi specifici
        if isinstance(serialized_fascicolo["data_apertura"], str):
            print("✅ data_apertura convertita in stringa")
        
        if isinstance(serialized_fascicolo["documenti"][0]["data_caricamento"], str):
            print("✅ data_caricamento documento convertita in stringa")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore nel test FascicoloData: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_generation_with_datetime():
    """Test completo di generazione con datetime nel fascicolo"""
    print("\n🧪 Test Generazione con DateTime")
    print("=" * 40)
    
    try:
        # Crea servizio di generazione
        service = await create_direct_generation_service()
        print("✅ Servizio creato")
        
        # Crea fascicolo con datetime
        richiedente = AnagraficaRichiedente(
            nome="Mario",
            cognome="Rossi",
            codice_fiscale="RSSMRA80C15H501X",
            email="mario.rossi@test.com"
        )
        
        documento = DocumentReference(
            id="doc_test",
            nome="istanza_test.pdf",
            tipo=DocumentType.ISTANZA,
            percorso="/test/istanza.pdf",
            dimensione=2048,
            data_caricamento=datetime.now(),
            contenuto_estratto="Istanza di autorizzazione per apertura attività commerciale"
        )
        
        fascicolo = FascicoloData(
            id="fasc_test_datetime",
            data_apertura=datetime.now(),
            procedimento_type=ProcedimentoType.AUTORIZZAZIONE,
            richiedente=richiedente,
            documenti=[documento],
            urgente=False
        )
        
        ente_metadata = {
            "nome": "Comune di Test",
            "settore": "SUAP",
            "responsabile": "Dott. Test"
        }
        
        print("🚀 Avvio generazione completa...")
        
        # Test generazione completa (questo dovrebbe ora funzionare)
        response = await service.generate_complete_determina(
            fascicolo, 
            ente_metadata,
            "standard"
        )
        
        print(f"✅ Generazione completata:")
        print(f"   - Status: {response.status}")
        print(f"   - ID: {response.determina_id}")
        
        if response.status == GenerationStatus.GENERATED:
            print(f"   - Premesse: {len(response.content.premesse) if response.content else 0} caratteri")
            print(f"   - Motivazione: {len(response.content.motivazione) if response.content else 0} caratteri")
            print(f"   - Dispositivo: {len(response.content.dispositivo) if response.content else 0} caratteri")
            print("✅ Determina generata con successo!")
        elif response.error_message:
            print(f"⚠️  Errore: {response.error_message}")
        
        await service.mcp_client.disconnect()
        return response.status == GenerationStatus.GENERATED
        
    except Exception as e:
        print(f"❌ Errore nella generazione: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Esegue tutti i test di serializzazione"""
    print("🏛️ Test Correzione Serializzazione JSON")
    print("🎯 Verifica che il problema datetime sia risolto")
    print("=" * 50)
    
    test1_ok = await test_json_serialization()
    test2_ok = await test_fascicolo_data_serialization()
    test3_ok = await test_generation_with_datetime()
    
    print("\n" + "=" * 50)
    print("📊 RISULTATI FINALI")
    print("=" * 50)
    
    if test1_ok and test2_ok and test3_ok:
        print("✅ CORREZIONE SERIALIZZAZIONE: Successo completo!")
        print("🎉 Il problema datetime è stato risolto")
        print("💡 Ora la generazione delle determine dovrebbe funzionare senza errori")
    else:
        print("❌ CORREZIONE SERIALIZZAZIONE: Problemi rilevati")
        if not test1_ok:
            print("   - Problemi nella funzione base di serializzazione")
        if not test2_ok:
            print("   - Problemi con FascicoloData")
        if not test3_ok:
            print("   - Problemi nella generazione completa")


if __name__ == "__main__":
    asyncio.run(main())