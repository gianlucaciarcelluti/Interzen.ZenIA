#!/usr/bin/env python3

"""
Script per verificare la presenza di System Card per ogni Microservice (MS)

Verifica:
1. Presenza di SYSTEM-CARD.md (versione inglese)
2. Presenza di SYSTEM-CARD-ITA.md (versione italiana)
3. Completezza della documentazione (sezioni richieste)
4. Status di approvazione

Output: JSON report in scripts/reports/system_cards_validation.json
"""

import os
import json
import re
import time
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
MICROSERVICES_DIR = REPO_ROOT / "docs" / "microservices"
REPORTS_DIR = SCRIPT_DIR / "reports"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Expected MS pattern: MS##-NAME
MS_PATTERN = re.compile(r'^MS\d{2}-')

# Required sections in System Card (minimum)
# Sono presenti varianti inglesi e italiane
REQUIRED_SECTIONS = {
    'Model Identity': ['Model Identity', 'Identità del Modello', 'Identità e Versionamento', 'Identificazione Modello'],
    'Intended Use': ['Intended Use', 'Uso Previsto'],
    'Training Data': ['Training Data', 'Dati di Training', 'Dati di training', 'Transformation Algorithm', 'Algoritmi di Trasformazione'],
    'Performance': ['Performance', 'Performance Metrics', 'Metriche di Performance', 'Metriche', 'Conversion Success'],
    'Risk Assessment': ['Risk Assessment', 'Valutazione Rischi', 'Risk'],
    'Approvals': ['Approvals', 'Approvazioni', 'Approval']
}

def find_microservices():
    """Trova tutti i microservices nella struttura"""
    if not MICROSERVICES_DIR.exists():
        return []

    ms_dirs = []
    for item in MICROSERVICES_DIR.iterdir():
        if item.is_dir() and MS_PATTERN.match(item.name):
            ms_dirs.append(item)

    return sorted(ms_dirs)

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

        # Estrai livello rischio
        risk_match = re.search(r'Risk Level["\s:]*[=:]*\s*([🔴🟠🟢]?\s*(?:HIGH|MEDIUM|LOW|ALTO|MEDIO|BASSO))', content, re.IGNORECASE)
        if risk_match:
            result['risk_level'] = risk_match.group(1).strip()

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
    """Valida tutte le System Card presenti"""
    ms_dirs = find_microservices()

    report = {
        'timestamp': datetime.now().isoformat(),
        'total_microservices': len(ms_dirs),
        'microservices': {},
        'summary': {
            'english_cards': 0,
            'italian_cards': 0,
            'both_languages': 0,
            'missing_english': 0,
            'missing_italian': 0,
            'complete_coverage': 0
        },
        'issues': []
    }

    for ms_dir in ms_dirs:
        ms_name = ms_dir.name

        # Verifica entrambe le versioni
        en_card = check_system_card_file(ms_dir, 'en')
        it_card = check_system_card_file(ms_dir, 'it')

        report['microservices'][ms_name] = {
            'english': en_card,
            'italian': it_card
        }

        # Aggiorna summary
        if en_card['present']:
            report['summary']['english_cards'] += 1
        else:
            report['summary']['missing_english'] += 1
            report['issues'].append({
                'type': 'MISSING_ENGLISH_CARD',
                'microservice': ms_name,
                'message': f'{ms_name} manca SYSTEM-CARD.md (versione inglese)'
            })

        if it_card['present']:
            report['summary']['italian_cards'] += 1
        else:
            report['summary']['missing_italian'] += 1
            report['issues'].append({
                'type': 'MISSING_ITALIAN_CARD',
                'microservice': ms_name,
                'message': f'{ms_name} manca SYSTEM-CARD-ITA.md (versione italiana)'
            })

        if en_card['present'] and it_card['present']:
            report['summary']['both_languages'] += 1
            report['summary']['complete_coverage'] += 1

        # Verifica sezioni mancanti
        if en_card['present'] and en_card['missing_sections']:
            for section in en_card['missing_sections']:
                report['issues'].append({
                    'type': 'MISSING_SECTION',
                    'microservice': ms_name,
                    'language': 'english',
                    'section': section,
                    'message': f'{ms_name} SYSTEM-CARD.md: manca sezione "{section}"'
                })

        if it_card['present'] and it_card['missing_sections']:
            for section in it_card['missing_sections']:
                report['issues'].append({
                    'type': 'MISSING_SECTION',
                    'microservice': ms_name,
                    'language': 'italian',
                    'section': section,
                    'message': f'{ms_name} SYSTEM-CARD-ITA.md: manca sezione "{section}"'
                })

    return report

def print_results(report):
    """Stampa risultati in console"""
    total_ms = report['total_microservices']
    english_cards = report['summary']['english_cards']
    italian_cards = report['summary']['italian_cards']
    both_langs = report['summary']['both_languages']
    issues_count = len(report['issues'])

    print(f"\n📋 System Cards Validation Report")
    print(f"{'='*60}")
    print(f"Total Microservices: {total_ms}")
    print(f"English Cards (SYSTEM-CARD.md): {english_cards}/{total_ms}")
    print(f"Italian Cards (SYSTEM-CARD-ITA.md): {italian_cards}/{total_ms}")
    print(f"Complete Coverage (both languages): {both_langs}/{total_ms}")
    print()

    if issues_count == 0:
        print("✅ ALL SYSTEM CARDS PRESENT - PERFECT")
        return 0
    else:
        print(f"⚠️ ISSUES FOUND: {issues_count}\n")

        # Raggruppa per tipo di problema
        missing_english = [i for i in report['issues'] if i['type'] == 'MISSING_ENGLISH_CARD']
        missing_italian = [i for i in report['issues'] if i['type'] == 'MISSING_ITALIAN_CARD']
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
            print(f"\nMissing Sections ({len(missing_sections)}):")
            for issue in missing_sections:
                print(f"  • {issue['microservice']} ({issue['language']}): {issue['section']}")

        return 1

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
