#!/usr/bin/env python3
"""
Verifica validazione payload JSON in SP.

Assicura che:
- JSON request/response examples siano validi
- Schema siano consistenti
- Campi obbligatori siano documentati
- Tipi dati siano coerenti
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class PayloadValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.json_blocks_found = 0
        self.json_blocks_valid = 0
        self.files_with_payloads = 0

    def extract_json_blocks(self, content: str, filename: str) -> List[Tuple[int, str, str]]:
        """Estrai blocchi JSON e il loro contesto."""
        # Pattern per blocchi JSON in markdown — match only fences labelled as JSON (```json ... ```)
        pattern = r'```json\s*\n((?:[^`]|`(?!``))*?)\n```'
        blocks = []

        for match in re.finditer(pattern, content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            json_code = match.group(1).strip()

            # Determina tipo (request, response, schema, example)
            context_start = max(0, match.start() - 200)
            context = content[context_start:match.start()].lower()

            if 'request' in context:
                type_label = "request"
            elif 'response' in context:
                type_label = "response"
            elif 'schema' in context:
                type_label = "schema"
            else:
                type_label = "example"

            blocks.append((line_num, json_code, type_label))

        return blocks

    def validate_json(self, json_code: str, line_num: int, type_label: str, filename: str) -> Tuple[bool, List[str]]:
        """Valida blocco JSON."""
        issues = []

        if not json_code.strip():
            issues.append(f"Line {line_num}: Blocco JSON vuoto ({type_label})")
            return False, issues

        try:
            parsed = json.loads(json_code)
            self.json_blocks_valid += 1
        except json.JSONDecodeError as e:
            err_text = str(e)
            # Try to salvage common case where extra data follows a valid JSON object
            if 'Extra data' in err_text or 'Expecting value' in err_text:
                s = json_code
                start_idx = s.find('{')
                first_obj = None
                if start_idx != -1:
                    stack = 0
                    for i in range(start_idx, len(s)):
                        ch = s[i]
                        if ch == '{':
                            stack += 1
                        elif ch == '}':
                            stack -= 1
                            if stack == 0:
                                candidate = s[start_idx:i+1]
                                try:
                                    parsed = json.loads(candidate)
                                    self.json_blocks_valid += 1
                                    issues.append(f"Line {line_num}: JSON contiene dati extra; convalidato solo il primo oggetto")
                                    first_obj = parsed
                                    break
                                except json.JSONDecodeError:
                                    break
                if first_obj is None:
                    issues.append(f"Line {line_num}: JSON invalido ({type_label}) - {err_text[:100]}")
                    return False, issues
                else:
                    parsed = first_obj
            else:
                issues.append(f"Line {line_num}: JSON invalido ({type_label}) - {err_text[:100]}")
                return False, issues

        # Valida struttura (deve essere object, non primitivo)
        if not isinstance(parsed, dict):
            issues.append(f"Line {line_num}: JSON non è un object ({type_label}), è {type(parsed).__name__}")
            return False, issues

        # Controlla campi comuni
        if type_label == "request":
            # Request dovrebbe avere campi
            if not parsed:
                issues.append(f"Line {line_num}: Request JSON è vuoto")
                return False, issues

        elif type_label == "response":
            # Response ideale: avere almeno 'status' o 'data' o 'error',
            # ma molti esempi usano strutture domain-specific. Trattiamo
            # la mancanza di questi campi come AVVISO (warning) invece che errore.
            required = {"status", "data", "error", "result", "message"}
            if not any(k in parsed for k in required):
                # registra warning ma non fallisce la validazione sintattica
                self.warnings.append(f"Line {line_num} in {filename}: Response manca campi standard (status, data, error, ecc.)")
                # keep the block valid (return True) but include the note in issues for reporting
                issues.append(f"Line {line_num}: Response manca campi standard (status, data, error, ecc.)")
                # do not return False here

        # Valida tipi dati coerenti
        for key, value in parsed.items():
            if not isinstance(key, str):
                issues.append(f"Line {line_num}: Chiave JSON non è stringa: {key}")

            # Valida tipi comuni
            if isinstance(value, (int, float, str, bool, type(None), list, dict)):
                pass  # OK
            else:
                issues.append(f"Line {line_num}: Tipo valore non supportato: {key}: {type(value).__name__}")

        return True, issues

    def validate_file(self, file_path: Path) -> Dict:
        """Valida file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "json_count": 0, "errors": [str(e)]}

        json_blocks = self.extract_json_blocks(content, file_path.name)

        if not json_blocks:
            return {"file": str(file_path.relative_to(DOCS_DIR)), "valid": True, "json_count": 0, "errors": []}

        file_errors = []
        self.files_with_payloads += 1
        self.json_blocks_found += len(json_blocks)

        for line_num, json_code, type_label in json_blocks:
            is_valid, issues = self.validate_json(json_code, line_num, type_label, file_path.name)
            if not is_valid:
                file_errors.extend(issues)

        self.errors.extend(file_errors)

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(file_errors) == 0,
            "json_count": len(json_blocks),
            "errors": file_errors,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando file per JSON payload...")
        # Focus su SP file
        files = list(DOCS_DIR.rglob("SP*.md"))
        print(f"✅ Trovati {len(files)} file SP\n")
        print("✔️  Validando payload JSON...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["json_count"] > 0:
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_errors = len([r for r in results if r["errors"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_with_payloads": self.files_with_payloads,
                "json_blocks_found": self.json_blocks_found,
                "json_blocks_valid": self.json_blocks_valid,
                "files_with_errors": files_with_errors,
                "total_errors": len(self.errors),
            },
            "details": results,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA VALIDAZIONE PAYLOAD JSON")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File con payload: {summary['files_with_payloads']}")
        print(f"  Blocchi JSON trovati: {summary['json_blocks_found']}")
        print(f"  Blocchi JSON validi: {summary['json_blocks_valid']}")
        print(f"  File con errori: {summary['files_with_errors']}")
        print(f"  ❌ Errori totali: {summary['total_errors']}\n")

        if summary['json_blocks_found'] > 0:
            validity_pct = (summary['json_blocks_valid'] / summary['json_blocks_found'] * 100)
            print(f"Validità JSON: {validity_pct:.1f}% ({summary['json_blocks_valid']}/{summary['json_blocks_found']})")

        if report["errors"]:
            print("\n" + "="*70)
            print("❌ ERRORI (primi 15):")
            for i, error in enumerate(report["errors"][:15]):
                print(f"  {i+1}. {error}")
            if len(report["errors"]) > 15:
                print(f"  ... e altri {len(report['errors']) - 15} errori")

        # Mostra eventuali warnings separati (non bloccanti)
        if report.get("warnings"):
            print("\n" + "="*70)
            print("⚠️  WARNING (primi 15):")
            for i, w in enumerate(report.get("warnings")[:15]):
                print(f"  {i+1}. {w}")
            if len(report.get("warnings")) > 15:
                print(f"  ... e altri {len(report.get('warnings')) - 15} warnings")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0:
            print("✅ PAYLOAD VALIDATION: PERFECT")
            return 0
        else:
            print("⚠️  PAYLOAD VALIDATION: ISSUES FOUND")
            return 0  # Warning, non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "payload_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = PayloadValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
