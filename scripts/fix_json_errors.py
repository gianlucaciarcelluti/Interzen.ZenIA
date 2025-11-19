#!/usr/bin/env python3
"""
Script per correggere errori JSON nella documentazione ZenIA.

Analizza gli errori dal report json_validation.json e suggerisce/applica correzioni.
"""

import json
import re
from pathlib import Path
from typing import List, Tuple

DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"

def extract_json_block(content: str, line_number: int) -> Tuple[str, int, int]:
    """Estrai blocco JSON da linea specificata.

    Ritorna: (blocco_json, riga_inizio, riga_fine)
    """
    lines = content.split('\n')

    # Trova inizio blocco (cercando ```json prima della riga)
    start_idx = None
    for i in range(line_number - 1, -1, -1):
        if '```json' in lines[i]:
            start_idx = i + 1
            break

    if start_idx is None:
        return None, None, None

    # Trova fine blocco (cercando ``` dopo la riga)
    end_idx = None
    for i in range(line_number, len(lines)):
        if lines[i].strip() == '```':
            end_idx = i
            break

    if end_idx is None:
        return None, None, None

    json_lines = lines[start_idx:end_idx]
    json_content = '\n'.join(json_lines)

    return json_content, start_idx, end_idx

def diagnose_json_error(json_content: str, error_msg: str) -> str:
    """Diagnostica l'errore JSON e suggerisci correzione.

    Ritorna descrizione del problema e suggerimento.
    """
    lines = json_content.split('\n')

    diagnosis = []

    # Analizza per common issues

    # Issue 1: Empty JSON block
    if json_content.strip() == '':
        diagnosis.append("❌ Blocco JSON vuoto")
        diagnosis.append("✅ Soluzione: Rimuovi il blocco ```json...``` o aggiungi contenuto")
        return '\n'.join(diagnosis)

    # Issue 2: Missing quotes on keys
    if 'Expecting property name enclosed in double quotes' in error_msg:
        diagnosis.append("❌ Chiave senza virgolette doppie")
        # Cerca linea con = invece di :
        for i, line in enumerate(lines):
            if ' = ' in line and '{' in line:
                diagnosis.append(f"✅ Linea {i+1}: Cambia '{line.strip()}' in '{line.replace(' = ', ': ').strip()}'")
                break
        return '\n'.join(diagnosis)

    # Issue 3: Missing comma between properties
    if "Expecting ',' delimiter" in error_msg:
        diagnosis.append("❌ Virgola mancante tra proprietà")
        diagnosis.append("✅ Soluzione: Aggiungi virgola dopo la proprietà precedente")
        return '\n'.join(diagnosis)

    # Issue 4: Extra data (multiple JSON objects)
    if 'Extra data' in error_msg:
        diagnosis.append("❌ Dati extra (probabilmente 2 JSON objects sequenziali)")
        diagnosis.append("✅ Soluzione: Racchiudi in array [] oppure separa in due blocchi diversi")
        return '\n'.join(diagnosis)

    # Issue 5: Unquoted values
    if 'Expecting value' in error_msg:
        diagnosis.append("❌ Valore non valido (possibilmente non quoted)")
        for i, line in enumerate(lines):
            # Cerca valori senza quotes (ma non null, true, false, numeri)
            if ':' in line and not any(x in line for x in ['"', "'", 'null', 'true', 'false', '{']):
                value_part = line.split(':', 1)[1].strip()
                if value_part and not value_part[0].isdigit():
                    diagnosis.append(f"✅ Linea {i+1}: Probabilmente aggiungi quote al valore: {value_part}")
                    break
        return '\n'.join(diagnosis)

    return "⚠️  Errore sconosciuto: " + error_msg

def main():
    print("🔧 ZenIA JSON Error Fixer - FASE 2")
    print("=" * 80)
    print()

    # Carica report errori
    with open(REPORTS_DIR / 'json_validation.json') as f:
        report = json.load(f)

    print(f"📊 Trovati {len(report['errors'])} errori JSON\n")

    # Analizza primi 5 errori
    for i, error_line in enumerate(report['errors'][:5], 1):
        print(f"\n{'='*80}")
        print(f"Errore {i}/{len(report['errors'])}")
        print(f"{'='*80}")

        # Parse error
        match = re.search(r'(.+?):(\d+) - Errore JSON: (.+)', error_line)
        if not match:
            continue

        file_path = match.group(1)
        line_num = int(match.group(2))
        error_msg = match.group(3)

        full_path = DOCS_DIR / file_path

        if not full_path.exists():
            print(f"❌ File non trovato: {file_path}")
            continue

        # Estrai blocco JSON
        content = full_path.read_text(encoding='utf-8')
        json_block, start_idx, end_idx = extract_json_block(content, line_num)

        if json_block is None:
            print(f"⚠️  Non riesco a estrarre il blocco JSON da {file_path}:{line_num}")
            continue

        print(f"📁 File: {file_path}")
        print(f"📍 Linea: {line_num}")
        print(f"❌ Errore: {error_msg}")
        print()
        print("📄 Contenuto JSON:")
        print("-" * 40)
        print(json_block[:300] + ("..." if len(json_block) > 300 else ""))
        print("-" * 40)
        print()

        # Diagnostica
        diagnosis = diagnose_json_error(json_block, error_msg)
        print("🔍 Diagnostica:")
        print(diagnosis)
        print()

if __name__ == "__main__":
    main()
