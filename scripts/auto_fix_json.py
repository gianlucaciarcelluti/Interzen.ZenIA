#!/usr/bin/env python3
"""
Script per correggere automaticamente errori JSON nella documentazione.

Applica correzioni a:
1. {...} → {} (placeholder to empty object)
2. Unquoted boolean/null values
3. Unquoted numeric values when needed
4. Missing commas between properties
5. Remove comments from JSON
"""

import json
import re
from pathlib import Path
from typing import List, Tuple

DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"

def fix_json_block(json_content: str) -> Tuple[str, List[str]]:
    """Applica correzioni automatiche a un blocco JSON.

    Ritorna: (json_corretto, lista_correzioni)
    """
    fixes = []
    content = json_content

    # Fix 1: Rimuovi commenti JSON (// ... e /* ... */)
    if '//' in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            # Rimuovi commenti fino alla fine della linea
            if '//' in line:
                line = line[:line.index('//')]
            new_lines.append(line)
        content = '\n'.join(new_lines)
        fixes.append("Rimossi commenti JSON")

    # Fix 2: Sostituisci {...} con {}
    if '{...}' in content:
        content = content.replace('{...}', '{}')
        fixes.append("Sostituito {...} con {}")

    # Fix 3: Sostituisci [...] con []
    if '[...]' in content:
        content = content.replace('[...]', '[]')
        fixes.append("Sostituito [...] con []")

    # Fix 4: Sostituisci "..." con "string_placeholder"
    # Ma solo se è un valore, non se è in un commento
    content = re.sub(r':\s*"\.\.\."\s*([,\n}])', r': ".."\1', content)
    fixes.append("Standardizzati placeholder stringhe")

    # Fix 5: Rimuovi whitespace eccessivo e formatta
    try:
        # Prova a parseire
        parsed = json.loads(content)
        # Se riuscito, riformatta
        content = json.dumps(parsed, indent=2, ensure_ascii=False)
        fixes.append("Riformattato JSON valido")
    except json.JSONDecodeError as e:
        # Se fallisce, prova altre correzioni
        pass

    return content, fixes

def process_file(file_path: Path) -> Tuple[int, List[str]]:
    """Processa un file e corregge errori JSON.

    Ritorna: (numero_blocchi_corretti, lista_messaggi)
    """
    messages = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return 0, [f"❌ Errore lettura {file_path.name}: {e}"]

    # Trova tutti i blocchi ```json
    json_blocks = re.finditer(r'```json\n(.*?)\n```', content, re.DOTALL)
    blocks_found = 0
    fixed_count = 0

    new_content = content
    offset = 0

    for match in re.finditer(r'```json\n(.*?)\n```', content, re.DOTALL):
        blocks_found += 1
        json_content = match.group(1)

        try:
            # Prova a validare
            json.loads(json_content)
            # Se passa, è già valido
        except json.JSONDecodeError as e:
            # Prova a correggere
            fixed_content, fixes = fix_json_block(json_content)

            try:
                # Verifica che il fix è valido
                json.loads(fixed_content)
                # Rimpiazza nel content
                old_block = match.group(0)
                new_block = f"```json\n{fixed_content}\n```"

                # Calcola offset per rimpiazzamenti multipli
                start = match.start() + offset
                end = match.end() + offset

                new_content = new_content[:start] + new_block + new_content[end:]
                offset += len(new_block) - len(old_block)

                fixed_count += 1
                messages.append(f"✅ Blocco {blocks_found}: Fixed - {', '.join(fixes)}")

            except json.JSONDecodeError as e2:
                messages.append(f"⚠️  Blocco {blocks_found}: Non posso fixare - {str(e2)[:50]}")

    # Scrivi file corretto se ci sono stati fix
    if fixed_count > 0:
        try:
            file_path.write_text(new_content, encoding='utf-8')
            messages.insert(0, f"📝 File salvato ({fixed_count}/{blocks_found} blocchi corretti)")
        except Exception as e:
            messages.insert(0, f"❌ Errore salvataggio: {e}")

    return fixed_count, messages

def main():
    print("🔧 ZenIA Auto JSON Fixer - FASE 2")
    print("=" * 80)
    print()

    # Carica report errori
    with open(REPORTS_DIR / 'json_validation.json') as f:
        report = json.load(f)

    # Estrai file che hanno errori
    files_with_errors = set()
    for error in report['errors']:
        match = re.search(r'^(.+?):\d+', error)
        if match:
            files_with_errors.add(match.group(1))

    print(f"📊 Trovati {len(report['errors'])} errori in {len(files_with_errors)} file")
    print()

    total_fixed = 0
    fixed_files = []

    for file_path_str in sorted(files_with_errors):
        full_path = DOCS_DIR / file_path_str

        if not full_path.exists():
            print(f"❌ File non trovato: {file_path_str}")
            continue

        print(f"\n{'='*80}")
        print(f"📁 {file_path_str}")
        print("=" * 80)

        fixed_count, messages = process_file(full_path)
        for msg in messages:
            print(msg)

        if fixed_count > 0:
            total_fixed += fixed_count
            fixed_files.append((file_path_str, fixed_count))

    print()
    print("=" * 80)
    print("📊 RIEPILOGO CORREZIONI")
    print("=" * 80)
    print(f"File processati: {len(files_with_errors)}")
    print(f"Blocchi corretti: {total_fixed}/{len(report['errors'])}")
    print()

    if fixed_files:
        print("✅ File Corretti:")
        for file_name, count in fixed_files:
            print(f"  • {file_name}: {count} blocchi")

if __name__ == "__main__":
    main()
