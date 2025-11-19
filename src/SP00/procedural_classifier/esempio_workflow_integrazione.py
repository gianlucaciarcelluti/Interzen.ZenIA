"""
Esempio di integrazione SP00 in workflow completo
Dimostra come usare il classificatore in un contesto più ampio
"""

from groq_procedural_classifier import ProceduralClassifier
from procedimenti_dataset import get_procedimento_info
import json
from typing import Optional


def workflow_classificazione_completo(istanza_text: str, api_key: Optional[str] = None):
    """
    Workflow completo di classificazione istanza
    Simula integrazione con altri servizi (SP01, SP03, ecc.)
    
    Args:
        istanza_text: Testo dell'istanza da classificare
        api_key: API key Groq
    
    Returns:
        Dict con risultati completi del workflow
    """
    
    print("=" * 80)
    print("🏛️  WORKFLOW CLASSIFICAZIONE PROCEDIMENTO COMPLETO")
    print("=" * 80)
    
    workflow_result = {
        "fase_0_classificazione": None,
        "fase_1_kb_retrieval": None,
        "fase_2_template_selection": None,
        "fase_3_validation": None,
        "stato": "IN_CORSO"
    }
    
    # ========================================================================
    # FASE 0: Classificazione Procedimento (SP00)
    # ========================================================================
    print("\n📋 FASE 0: Classificazione Procedimento (SP00)")
    print("-" * 80)
    
    classifier = ProceduralClassifier(api_key=api_key)
    result = classifier.classify_single(istanza_text)
    
    if not result.get('success'):
        print(f"❌ Errore classificazione: {result.get('error')}")
        workflow_result['stato'] = "ERRORE_CLASSIFICAZIONE"
        return workflow_result
    
    workflow_result['fase_0_classificazione'] = result
    
    print(f"✅ Procedimento identificato: {result['procedimento']}")
    print(f"   Tipo provvedimento: {result['tipo_provvedimento']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    
    # Verifica confidence
    if result['confidence'] < 0.7:
        print("\n⚠️  ATTENZIONE: Confidence bassa - Richiesta revisione manuale")
        workflow_result['stato'] = "REVISIONE_MANUALE_RICHIESTA"
        return workflow_result
    
    # ========================================================================
    # FASE 1: KB Retrieval - Normativa e Regole (SP03)
    # ========================================================================
    print("\n📚 FASE 1: Knowledge Base Retrieval (SP03)")
    print("-" * 80)
    
    # SIMULAZIONE: In produzione, questo chiamerebbe SP03
    procedimento = result['procedimento']
    procedimento_info = get_procedimento_info(procedimento)
    
    kb_data = {
        "normativa_dettagliata": procedimento_info.get('normativa', []),
        "termini_procedimentali": procedimento_info.get('termini_giorni'),
        "autorita_competente": procedimento_info.get('autorita_competente'),
        "metadata_required": ["dati_richiedente", "allegati_tecnici"],
        "regole_validazione": [
            "Verifica completezza documentazione",
            "Controllo requisiti soggettivi richiedente",
            "Validazione conformità normativa"
        ]
    }
    
    workflow_result['fase_1_kb_retrieval'] = kb_data
    
    print(f"✅ Normativa recuperata: {', '.join(kb_data['normativa_dettagliata'])}")
    print(f"   Termini: {kb_data['termini_procedimentali']} giorni")
    print(f"   Autorità: {kb_data['autorita_competente']}")
    
    # ========================================================================
    # FASE 2: Template Selection (SP01)
    # ========================================================================
    print("\n📝 FASE 2: Selezione Template Provvedimento (SP01)")
    print("-" * 80)
    
    # SIMULAZIONE: In produzione, questo chiamerebbe SP01
    tipo_provv = result['tipo_provvedimento']
    
    template_info = {
        "template_id": f"TPL_{tipo_provv}_001",
        "nome_template": f"Template {tipo_provv}",
        "versione": "2.1",
        "sezioni": [
            "Intestazione Ente",
            "Premessa",
            "Motivazioni",
            "Parte Dispositiva",
            "Firma Digitale"
        ],
        "campi_da_compilare": [
            "oggetto_provvedimento",
            "richiedente",
            "normativa_riferimento",
            "motivazione_tecnica",
            "dispositivo",
            "responsabile_procedimento"
        ]
    }
    
    workflow_result['fase_2_template_selection'] = template_info
    
    print(f"✅ Template selezionato: {template_info['nome_template']}")
    print(f"   Versione: {template_info['versione']}")
    print(f"   Sezioni: {len(template_info['sezioni'])}")
    
    # ========================================================================
    # FASE 3: Validation Preliminare (SP02)
    # ========================================================================
    print("\n✓ FASE 3: Validazione Preliminare (SP02)")
    print("-" * 80)
    
    # SIMULAZIONE: In produzione, questo chiamerebbe SP02
    validation_checks = {
        "completezza_istanza": True,
        "conformita_normativa": True,
        "requisiti_formali": True,
        "allegati_presenti": True,  # Mock
        "firme_valide": True,       # Mock
        "warnings": []
    }
    
    # Aggiungi eventuali warning
    if result['confidence'] < 0.85:
        validation_checks['warnings'].append(
            "Confidence classificazione < 85%: raccomandato doppio controllo"
        )
    
    workflow_result['fase_3_validation'] = validation_checks
    
    all_valid = all([
        validation_checks['completezza_istanza'],
        validation_checks['conformita_normativa'],
        validation_checks['requisiti_formali']
    ])
    
    if all_valid:
        print("✅ Validazione superata")
        workflow_result['stato'] = "PRONTO_PER_GENERAZIONE"
    else:
        print("❌ Validazione fallita")
        workflow_result['stato'] = "VALIDAZIONE_FALLITA"
    
    if validation_checks['warnings']:
        print("\n⚠️  Warning:")
        for warning in validation_checks['warnings']:
            print(f"   - {warning}")
    
    # ========================================================================
    # RIEPILOGO WORKFLOW
    # ========================================================================
    print("\n" + "=" * 80)
    print("📊 RIEPILOGO WORKFLOW")
    print("=" * 80)
    
    print(f"\n✅ Stato Finale: {workflow_result['stato']}")
    print(f"\n📋 Procedimento: {procedimento}")
    print(f"📄 Provvedimento: {tipo_provv}")
    print(f"📚 Normativa: {', '.join(kb_data['normativa_dettagliata'])}")
    print(f"⏱️  Termini: {kb_data['termini_procedimentali']} giorni")
    print(f"👤 Responsabile: {kb_data['autorita_competente']}")
    
    if workflow_result['stato'] == "PRONTO_PER_GENERAZIONE":
        print("\n🚀 PROSSIMO STEP: Generazione provvedimento con SP01")
        print(f"   Template: {template_info['template_id']}")
        print(f"   Campi da compilare: {len(template_info['campi_da_compilare'])}")
    
    print("\n" + "=" * 80)
    
    return workflow_result


def esempio_batch_workflow():
    """
    Esempio di processing batch con workflow completo
    """
    
    print("=" * 80)
    print("🔄 ESEMPIO BATCH PROCESSING")
    print("=" * 80)
    
    # Istanze di esempio
    istanze = [
        {
            "id": "IST-001",
            "testo": """Spettabile Comune, la scrivente ABC S.p.A. richiede 
            autorizzazione allo scarico di acque reflue industriali."""
        },
        {
            "id": "IST-002",
            "testo": """Il sottoscritto Mario Rossi chiede il rilascio del 
            permesso di costruire per villetta unifamiliare."""
        },
        {
            "id": "IST-003",
            "testo": """Si richiede licenza commerciale per apertura negozio 
            di abbigliamento."""
        }
    ]
    
    results = []
    
    for istanza in istanze:
        print(f"\n{'='*80}")
        print(f"Elaborazione istanza: {istanza['id']}")
        print(f"{'='*80}")
        
        result = workflow_classificazione_completo(istanza['testo'])
        
        results.append({
            "istanza_id": istanza['id'],
            "stato": result['stato'],
            "procedimento": result['fase_0_classificazione'].get('procedimento') if result['fase_0_classificazione'] else None,
            "confidence": result['fase_0_classificazione'].get('confidence') if result['fase_0_classificazione'] else 0.0
        })
    
    # Riepilogo batch
    print("\n" + "=" * 80)
    print("📊 RIEPILOGO BATCH")
    print("=" * 80)
    
    for r in results:
        status_icon = "✅" if r['stato'] == "PRONTO_PER_GENERAZIONE" else "⚠️"
        print(f"{status_icon} {r['istanza_id']}: {r['procedimento']} (conf: {r['confidence']:.2f})")
    
    print(f"\nTotale istanze: {len(results)}")
    ready = sum(1 for r in results if r['stato'] == "PRONTO_PER_GENERAZIONE")
    print(f"Pronte per generazione: {ready}/{len(results)}")


# ============================================================================
# MAIN - Esempi di utilizzo
# ============================================================================

if __name__ == "__main__":
    
    print("\n🏛️  SP00 - ESEMPI DI INTEGRAZIONE WORKFLOW")
    print("=" * 80)
    print("\nOpzioni:")
    print("1. Workflow completo singola istanza")
    print("2. Batch processing (3 istanze)")
    
    choice = input("\nScelta (1/2): ").strip()
    
    if choice == "1":
        # Esempio singola istanza
        test_istanza = """
        Spettabile Comune, la scrivente ABC S.p.A. richiede autorizzazione 
        allo scarico di acque reflue industriali provenienti dal ciclo 
        produttivo tessile. Portata media: 500 m³/giorno. Si allega 
        relazione tecnica e planimetria degli impianti.
        """
        
        workflow_classificazione_completo(test_istanza)
    
    elif choice == "2":
        # Esempio batch
        esempio_batch_workflow()
    
    else:
        print("❌ Scelta non valida")
    
    print("\n✅ Esempio completato!")
    print("\n💡 Questo dimostra come SP00 si integra nel workflow completo:")
    print("   SP00 → SP03 → SP01 → SP02 → SP05 → SP06")
