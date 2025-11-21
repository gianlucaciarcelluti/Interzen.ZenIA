#!/usr/bin/env python3

"""
Script per verificare la presenza di System Card per Microservices con ML (AI Act)

LOGICA:
- Solo 4 MS richiedono System Card per conformità AI Act 2024/1689:
  • MS01-CLASSIFIER (HIGH-RISK ML)
  • MS02-ANALYZER (MEDIUM-RISK ML)
  • MS04-VALIDATOR (MEDIUM-RISK ML)
  • MS05-TRANSFORMER (LOW-RISK deterministic)

- I rimanenti 12 MS sono utility/infrastruttura senza decisioni automatizzate

Verifica per i 4 MS obbligatori:
1. Presenza di SYSTEM-CARD.md (versione inglese)
2. Presenza di SYSTEM-CARD-ITA.md (versione italiana)
3. Completezza della documentazione (sezioni richieste)
4. Status di approvazione

Output: JSON report in scripts/reports/system_cards_validation.json
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
MICROSERVICES_DIR = REPO_ROOT / "docs" / "microservices"
REPORTS_DIR = SCRIPT_DIR / "reports"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Microservices che RICHIEDONO System Card per AI Act compliance
# Sono solo quelli con Machine Learning o decisioni automatizzate
REQUIRES_SYSTEM_CARD = {
    'MS01-CLASSIFIER': 'HIGH-RISK (Document Classification)',
    'MS02-ANALYZER': 'MEDIUM-RISK (Entity Extraction & NLP)',
    'MS04-VALIDATOR': 'MEDIUM-RISK (ML Validation)',
    'MS05-TRANSFORMER': 'LOW-RISK (Deterministic Transformation)',
}

# Microservices che NON richiedono System Card (utility/infrastruttura)
NON_ML_MICROSERVICES = {
    'MS03-ORCHESTRATOR': 'Workflow Orchestration',
    'MS06-AGGREGATOR': 'Data Aggregation',
    'MS07-DISTRIBUTOR': 'Document Distribution',
    'MS08-MONITOR': 'Infrastructure Monitoring',
    'MS09-MANAGER': 'Service Management',
    'MS10-LOGGER': 'Logging Service',
    'MS11-GATEWAY': 'API Gateway',
    'MS12-CACHE': 'Caching Layer',
    'MS13-SECURITY': 'Security Module',
    'MS14-AUDIT': 'Audit Trail',
    'MS15-CONFIG': 'Configuration Service',
    'MS16-REGISTRY': 'Service Registry',
}

# Required sections in System Card (minimum)
REQUIRED_SECTIONS = {
    'Model Identity': ['Model Identity', 'Identità del Modello', 'Identità e Versionamento', 'Identificazione Modello'],
    'Intended Use': ['Intended Use', 'Uso Previsto'],
    'Training Data': ['Training Data', 'Dati di Training', 'Dati di training', 'Transformation Algorithm', 'Algoritmi di Trasformazione'],
    'Performance': ['Performance', 'Performance Metrics', 'Metriche di Performance', 'Metriche', 'Conversion Success'],
    'Risk Assessment': ['Risk Assessment', 'Valutazione Rischi', 'Risk'],
    'Approvals': ['Approvals', 'Approvazioni', 'Approval']
}

def check_system_card_file(ms_dir, language='en'):
    """Verifica la presenza e qualità della System Card"""
    if language == 'en':
        filename = 'SYSTEM-CARD.md'
    else:
        filename = 'SYSTEM-CARD-ITA.md'

    filepath = ms_dir / filename

    result = {
        'file': filename,
        'present': filepath.exists(),
        'path': str(filepath.relative_to(REPO_ROOT)) if filepath.exists() else None,
        'size_bytes': filepath.stat().st_size if filepath.exists() else 0,
        'sections_found': [],
        'missing_sections': [],
        'approval_status': None,
        'risk_level': None
    }

    if not filepath.exists():
        return result

    # Leggi il contenuto
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verifica sezioni (ricerca semplice case-insensitive)
        # Supporta sia nomi inglesi che italiani
        for section_name, variants in REQUIRED_SECTIONS.items():
            found = False
            for variant in variants:
                if variant.lower() in content.lower():
                    found = True
                    break

            if found:
                result['sections_found'].append(section_name)
            else:
                result['missing_sections'].append(section_name)

        # Estrai status approvazioni
        if '✅ Executive Approval' in content or '✅ Executive Review' in content:
            result['approval_status'] = 'APPROVED'
        elif 'Executive Approval: PENDING' in content or 'Executive Review: PENDING' in content or '⏳ Executive' in content:
            result['approval_status'] = 'PENDING'
        else:
            result['approval_status'] = 'UNKNOWN'

    except Exception as e:
        result['error'] = str(e)

    return result

def validate_system_cards():
    """Valida System Card solo per i 4 MS che richiedono AI Act compliance"""
    microservices_dir = MICROSERVICES_DIR

    report = {
        'timestamp': datetime.now().isoformat(),
        'scope': 'AI Act 2024/1689 Compliance (ML Systems Only)',
        'required_count': len(REQUIRES_SYSTEM_CARD),
        'non_ml_count': len(NON_ML_MICROSERVICES),
        'total_microservices': len(REQUIRES_SYSTEM_CARD) + len(NON_ML_MICROSERVICES),
        'required_microservices': {},
        'non_ml_microservices': NON_ML_MICROSERVICES,
        'summary': {
            'english_cards_present': 0,
            'italian_cards_present': 0,
            'both_languages_complete': 0,
            'missing_english': 0,
            'missing_italian': 0,
            'compliance_score': 0  # percentage
        },
        'issues': []
    }

    # Valida solo i 4 MS che richiedono System Card
    for ms_name, risk_level in REQUIRES_SYSTEM_CARD.items():
        ms_dir = microservices_dir / ms_name

        if not ms_dir.exists():
            continue

        # Verifica entrambe le versioni
        en_card = check_system_card_file(ms_dir, 'en')
        it_card = check_system_card_file(ms_dir, 'it')

        report['required_microservices'][ms_name] = {
            'risk_level': risk_level,
            'english': en_card,
            'italian': it_card
        }

        # Aggiorna summary
        if en_card['present']:
            report['summary']['english_cards_present'] += 1
        else:
            report['summary']['missing_english'] += 1
            report['issues'].append({
                'type': 'MISSING_REQUIRED_CARD',
                'severity': 'CRITICAL',
                'microservice': ms_name,
                'language': 'english',
                'message': f'{ms_name} ({risk_level}): manca SYSTEM-CARD.md',
                'required': True
            })

        if it_card['present']:
            report['summary']['italian_cards_present'] += 1
        else:
            report['summary']['missing_italian'] += 1
            report['issues'].append({
                'type': 'MISSING_REQUIRED_CARD',
                'severity': 'CRITICAL',
                'microservice': ms_name,
                'language': 'italian',
                'message': f'{ms_name} ({risk_level}): manca SYSTEM-CARD-ITA.md',
                'required': True
            })

        if en_card['present'] and it_card['present']:
            report['summary']['both_languages_complete'] += 1

        # Verifica sezioni mancanti
        if en_card['present'] and en_card['missing_sections']:
            for section in en_card['missing_sections']:
                report['issues'].append({
                    'type': 'MISSING_SECTION',
                    'severity': 'WARNING',
                    'microservice': ms_name,
                    'language': 'english',
                    'section': section,
                    'message': f'{ms_name} SYSTEM-CARD.md: manca sezione "{section}"',
                    'required': True
                })

        if it_card['present'] and it_card['missing_sections']:
            for section in it_card['missing_sections']:
                report['issues'].append({
                    'type': 'MISSING_SECTION',
                    'severity': 'WARNING',
                    'microservice': ms_name,
                    'language': 'italian',
                    'section': section,
                    'message': f'{ms_name} SYSTEM-CARD-ITA.md: manca sezione "{section}"',
                    'required': True
                })

    # Calcola compliance score
    both_langs_required = report['summary']['both_languages_complete']
    required_total = len(REQUIRES_SYSTEM_CARD)
    compliance_score = int((both_langs_required / required_total * 100)) if required_total > 0 else 0
    report['summary']['compliance_score'] = compliance_score

    return report

def print_results(report):
    """Stampa risultati in console"""
    required_ms = report['required_count']
    english_cards = report['summary']['english_cards_present']
    italian_cards = report['summary']['italian_cards_present']
    both_langs = report['summary']['both_languages_complete']
    compliance = report['summary']['compliance_score']
    issues_count = len(report['issues'])
    critical_issues = len([i for i in report['issues'] if i['severity'] == 'CRITICAL'])

    print(f"\n📋 AI Act System Card Validation")
    print(f"{'='*60}")
    print(f"Required (AI Act ML Systems): {required_ms}")
    print(f"English Cards: {english_cards}/{required_ms}")
    print(f"Italian Cards: {italian_cards}/{required_ms}")
    print(f"Complete (Both Languages): {both_langs}/{required_ms}")
    print(f"AI Act Compliance Score: {compliance}%")
    print()

    if compliance == 100:
        print("✅ AI ACT COMPLIANCE COMPLETE - PASS")
        print("   All required System Cards present (EN + IT)")
        return 0
    elif critical_issues > 0:
        print(f"⚠️ INCOMPLETE COVERAGE: {critical_issues} missing required System Cards\n")

        # Raggruppa per tipo di problema
        missing_cards = [i for i in report['issues'] if i['type'] == 'MISSING_REQUIRED_CARD']
        missing_english = [i for i in missing_cards if i['language'] == 'english']
        missing_italian = [i for i in missing_cards if i['language'] == 'italian']
        missing_sections = [i for i in report['issues'] if i['type'] == 'MISSING_SECTION']

        if missing_english:
            print(f"Missing English System Cards ({len(missing_english)}):")
            for issue in missing_english:
                print(f"  • {issue['microservice']}")

        if missing_italian:
            print(f"\nMissing Italian System Cards ({len(missing_italian)}):")
            for issue in missing_italian:
                print(f"  • {issue['microservice']}")

        if missing_sections:
            print(f"\nIncomplete Sections ({len(missing_sections)}):")
            for issue in missing_sections:
                print(f"  • {issue['microservice']} ({issue['language']}): {issue['section']}")

        return 1
    else:
        print(f"✅ AI ACT COMPLIANCE - Minor issues ({len([i for i in report['issues'] if i['severity'] == 'WARNING'])} warnings)")
        return 0

def main():
    report = validate_system_cards()

    # Salva JSON report
    report_file = REPORTS_DIR / 'system_cards_validation.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Stampa risultati
    exit_code = print_results(report)

    print(f"\n📁 Report: scripts/reports/system_cards_validation.json")

    return exit_code

if __name__ == '__main__':
    exit(main())
