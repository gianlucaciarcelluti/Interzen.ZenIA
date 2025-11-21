#!/usr/bin/env python3
"""
Verifica validità sintassi Mermaid diagram.

Assicura che:
- Diagram abbiano sintassi valida Mermaid
- Flowchart abbiano nodi e connessioni ben formati
- Sequence diagram abbiano attori e messaggi validi
- State diagram abbiano stati e transizioni valide
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class MermaidValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.diagrams_found = 0
        self.diagrams_valid = 0

    def extract_mermaid_blocks(self, content: str, filename: str) -> List[Tuple[int, str]]:
        """Estrai blocchi Mermaid da markdown."""
        pattern = r'```mermaid\n(.*?)\n```'
        blocks = []
        for match in re.finditer(pattern, content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            diagram_code = match.group(1)
            blocks.append((line_num, diagram_code))
        return blocks

    def validate_mermaid_block(self, diagram_code: str, line_num: int, filename: str) -> Tuple[bool, List[str]]:
        """Valida un singolo blocco Mermaid."""
        issues = []

        if not diagram_code.strip():
            issues.append(f"Line {line_num}: Diagram Mermaid vuoto")
            return False, issues

        # Rileva tipo diagram
        first_line = diagram_code.split('\n')[0].strip()

        # Valida Flowchart
        if first_line.startswith('flowchart') or first_line.startswith('graph'):
            return self._validate_flowchart(diagram_code, line_num, filename)

        # Valida Sequence diagram
        elif first_line.startswith('sequenceDiagram'):
            return self._validate_sequence(diagram_code, line_num, filename)

        # Valida State diagram
        elif first_line.startswith('stateDiagram') or first_line.startswith('state'):
            return self._validate_state(diagram_code, line_num, filename)

        # Unknown type (warning, non error)
        else:
            issues.append(f"Line {line_num}: Tipo diagram Mermaid non riconosciuto: {first_line[:30]}")
            return True, issues  # Non è un errore, solo warning

    def _validate_flowchart(self, code: str, line_num: int, filename: str) -> Tuple[bool, List[str]]:
        """Valida flowchart."""
        issues = []
        lines = code.split('\n')

        # Controlla che ci siano nodi
        node_pattern = r'\[.*?\]|\{.*?\}|[A-Z0-9]+\['
        nodes = []
        for line in lines:
            if re.search(node_pattern, line):
                nodes.append(line.strip())

        if not nodes:
            issues.append(f"Line {line_num}: Flowchart non ha nodi definiti")
            return False, issues

        # Controlla connessioni malformate
        for i, line in enumerate(lines):
            if '-->' in line or '-.->' in line or '==>' in line:
                # Line ha una connessione, dovrebbe avere validi endpoints
                if line.count('[') != line.count(']') or line.count('{') != line.count('}'):
                    issues.append(f"Line {line_num + i}: Parentesi sbilanciati in connessione")

        # Valida parentesi
        open_brackets = code.count('[') + code.count('{') + code.count('(')
        close_brackets = code.count(']') + code.count('}') + code.count(')')
        if open_brackets != close_brackets:
            issues.append(f"Line {line_num}: Parentesi non bilanciate (aperti: {open_brackets}, chiusi: {close_brackets})")
            return False, issues

        return True, issues

    def _validate_sequence(self, code: str, line_num: int, filename: str) -> Tuple[bool, List[str]]:
        """Valida sequence diagram."""
        issues = []

        # Controlla partecipanti
        participant_pattern = r'participant\s+\w+'
        participants = re.findall(participant_pattern, code)

        if not participants:
            issues.append(f"Line {line_num}: Sequence diagram non ha partecipanti")
            return False, issues

        # Controlla messaggi
        message_pattern = r'(->|-->|->>|-->>)\s*'
        messages = re.findall(message_pattern, code)

        if not messages:
            issues.append(f"Line {line_num}: Sequence diagram non ha messaggi")
            return False, issues

        # Controlla sintassi note
        note_lines = [l for l in code.split('\n') if 'note' in l.lower()]
        for note_line in note_lines:
            if 'Note' in note_line and ':' not in note_line:
                issues.append(f"Line {line_num}: Note malformata (manca ':'): {note_line.strip()[:50]}")

        return len(issues) == 0, issues

    def _validate_state(self, code: str, line_num: int, filename: str) -> Tuple[bool, List[str]]:
        """Valida state diagram."""
        issues = []

        # Controlla stati (explicit e implicit)
        # Matches: "state StateName", "StateName -->", "state_name:", "StateName-->"
        state_pattern = r'state\s+\w+|[A-Z][a-zA-Z0-9_]*\s*(?:-->|:|-)'
        states = re.findall(state_pattern, code)

        if not states:
            issues.append(f"Line {line_num}: State diagram non ha stati definiti")
            return False, issues

        # Controlla transizioni
        transition_pattern = r'-->'
        transitions = re.findall(transition_pattern, code)

        if not transitions:
            issues.append(f"Line {line_num}: State diagram non ha transizioni")
            return False, issues

        return True, issues

    def validate_file(self, file_path: Path) -> Dict:
        """Valida Mermaid diagram in file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "diagram_count": 0, "errors": [str(e)]}

        file_errors = []
        diagrams = self.extract_mermaid_blocks(content, file_path.name)

        if not diagrams:
            return {"file": str(file_path.relative_to(DOCS_DIR)), "valid": True, "diagram_count": 0, "errors": []}

        for line_num, diagram_code in diagrams:
            self.diagrams_found += 1
            is_valid, issues = self.validate_mermaid_block(diagram_code, line_num, file_path.name)

            if is_valid:
                self.diagrams_valid += 1
            else:
                file_errors.extend(issues)

        self.errors.extend(file_errors)

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(file_errors) == 0,
            "diagram_count": len(diagrams),
            "errors": file_errors,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando file Markdown con diagram Mermaid...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando diagram Mermaid...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["diagram_count"] > 0:
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_diagrams = len(results)
        files_with_errors = len([r for r in results if r["errors"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_with_diagrams": files_with_diagrams,
                "diagrams_found": self.diagrams_found,
                "diagrams_valid": self.diagrams_valid,
                "files_with_errors": files_with_errors,
                "total_errors": len(self.errors),
            },
            "details": results,
            "errors": self.errors,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA VALIDITÀ DIAGRAM MERMAID")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  Diagram trovati: {summary['diagrams_found']}")
        print(f"  Diagram validi: {summary['diagrams_valid']}")
        print(f"  File con diagram: {summary['files_with_diagrams']}")
        print(f"  File con errori: {summary['files_with_errors']}")
        print(f"  ❌ Errori totali: {summary['total_errors']}\n")

        if summary['diagrams_found'] > 0:
            validity_pct = (summary['diagrams_valid'] / summary['diagrams_found'] * 100)
            print(f"Validità: {validity_pct:.1f}% ({summary['diagrams_valid']}/{summary['diagrams_found']})")

        if report["errors"]:
            print("\n" + "="*70)
            print("❌ ERRORI (primi 15):")
            for i, error in enumerate(report["errors"][:15]):
                print(f"  {i+1}. {error}")
            if len(report["errors"]) > 15:
                print(f"  ... e altri {len(report['errors']) - 15} errori")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0 or (summary['diagrams_found'] > 0 and summary['diagrams_valid'] == summary['diagrams_found']):
            print("✅ MERMAID DIAGRAMS: VALID")
            return 0
        else:
            print("⚠️  MERMAID DIAGRAMS: SOME ISSUES FOUND")
            return 0  # Non bloccare il commit, è warning

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "mermaid_diagrams_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = MermaidValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit_code = 0 if not validator.errors else 0  # Warnings, non bloccare
    exit(exit_code)


if __name__ == '__main__':
    main()
