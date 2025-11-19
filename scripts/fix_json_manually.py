#!/usr/bin/env python3
"""
Manualmente identifica i blocchi JSON che hanno problemi specifici.
"""

import json
import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"

def main():
    # Load errors
    with open(REPORTS_DIR / 'json_validation.json') as f:
        report = json.load(f)

    print("=" * 80)
    print("PROBLEMI JSON CHE RICHIEDONO CORREZIONE MANUALE")
    print("=" * 80)
    print()

    # Group by error type
    extra_data_errors = []
    expecting_value_errors = []
    expecting_comma_errors = []
    unquoted_key_errors = []

    for error in report['errors']:
        if 'Extra data' in error:
            extra_data_errors.append(error)
        elif 'Expecting value' in error:
            expecting_value_errors.append(error)
        elif "Expecting ','" in error:
            expecting_comma_errors.append(error)
        elif 'Expecting property name' in error:
            unquoted_key_errors.append(error)

    print(f"🔴 EXTRA DATA (probabilmente 2 JSON objects sequenziali): {len(extra_data_errors)}")
    for err in extra_data_errors[:3]:
        print(f"  • {err}")
    print()

    print(f"🔴 EXPECTING VALUE (JSON vuoto o incompleto): {len(expecting_value_errors)}")
    for err in expecting_value_errors[:3]:
        print(f"  • {err}")
    print()

    print(f"🟡 EXPECTING COMMA: {len(expecting_comma_errors)}")
    for err in expecting_comma_errors[:3]:
        print(f"  • {err}")
    print()

    print(f"🟡 UNQUOTED KEY: {len(unquoted_key_errors)}")
    for err in unquoted_key_errors[:3]:
        print(f"  • {err}")
    print()

    # Suggested approach
    print("=" * 80)
    print("STRATEGIA DI CORREZIONE")
    print("=" * 80)
    print()
    print("1️⃣  EXTRA DATA ERRORS (13):")
    print("    Probabilmente: 2 JSON objects uno dopo l'altro")
    print("    Soluzione: Separa in diversi blocchi ```json...``` oppure racchiudi in []")
    print()
    print("2️⃣  EXPECTING VALUE ERRORS (21):")
    print("    Probabilmente: Blocco JSON vuoto (solo comments) o valori non quoted")
    print("    Soluzione: Rimuovi commenti, aggiungi valori reali o placeholders validi")
    print()
    print("3️⃣  UNQUOTED KEY ERRORS (10):")
    print("    Probabilmente: Chiavi come true, false, null usate senza quotes")
    print("    Soluzione: Aggiungi double quotes attorno alle chiavi")
    print()

if __name__ == "__main__":
    main()
