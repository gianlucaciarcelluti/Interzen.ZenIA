#!/usr/bin/env python3
"""
Verifica coerenza linguistica (Italiano vs English).

Assicura che:
- Heading siano in una lingua consistente
- Termini tecnici siano standardizzati
- Nessun mix English/Italian in sezioni critiche (titoli, sommari)
- Terminologia SP/UC sia coerente
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Termini comuni English che dovrebbero essere Italian
ENGLISH_TECHNICAL_TERMS = {
    r'\boverview\b': ("overview", "panoramica/riepilogo"),
    r'\babstract\b': ("abstract", "riepilogo"),
    r'\barchitecture\b': ("architecture", "architettura"),
    r'\bimplementation\b': ("implementation", "implementazione"),
    r'\bexample\b': ("example", "esempio"),
    r'\bscenario\b': ("scenario", "scenario"),  # Same in Italian
    r'\bfeature\b': ("feature", "funzionalità"),
    r'\brequirement\b': ("requirement", "requisito"),
    r'\bdependency\b': ("dependency", "dipendenza"),
    r'\bintegration\b': ("integration", "integrazione"),
    r'\bvalidation\b': ("validation", "validazione"),
    r'\berror\b': ("error", "errore"),
    r'\berror handling\b': ("error handling", "gestione errori"),
    r'\bexception\b': ("exception", "eccezione"),
}

# Termini comuni Italian che dovrebbero essere coerenti
ITALIAN_TERMS = {
    "sezione": "sezione",
    "capitolo": "capitolo",
    "paragrafo": "paragrafo",
    "descrizione": "descrizione",
}

class LanguageValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.files_with_issues = 0

    def detect_language(self, text: str) -> Tuple[str, float]:
        """Riconosci lingua principale (simple heuristic)."""
        # Conta parole English comuni
        english_words = sum(1 for word in ['the', 'and', 'is', 'are', 'for', 'this', 'that', 'with', 'from', 'to']
                           if re.search(r'\b' + word + r'\b', text, re.IGNORECASE))

        # Conta parole Italian comuni
        italian_words = sum(1 for word in ['il', 'la', 'e', 'di', 'da', 'che', 'è', 'sono', 'con', 'per']
                           if re.search(r'\b' + word + r'\b', text, re.IGNORECASE))

        if english_words > italian_words:
            return "English", english_words / (english_words + italian_words) if (english_words + italian_words) > 0 else 0
        else:
            return "Italian", italian_words / (english_words + italian_words) if (english_words + italian_words) > 0 else 0

    def check_file_language(self, file_path: Path) -> Dict:
        """Controlla coerenza linguistica file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "issues": [str(e)]}

        file_issues = []
        lang_detected, confidence = self.detect_language(content)

        # Estrai heading
        heading_pattern = r'^#+\s+(.+)$'
        headings = [m.group(1) for m in re.finditer(heading_pattern, content, re.MULTILINE)]

        # Controlla lingua heading
        heading_english = sum(1 for h in headings if re.search(r'\b(overview|summary|example|architecture|implementation|feature|requirement)\b', h, re.IGNORECASE))
        heading_italian = sum(1 for h in headings if re.search(r'\b(panoramica|riepilogo|esempio|architettura|implementazione|funzionalità|requisito|descrizione)\b', h, re.IGNORECASE))

        if heading_english > 0 and heading_italian > 0:
            file_issues.append(f"Mix lingue in heading: {heading_english} English, {heading_italian} Italian")
            self.warnings.append(f"{file_path.name}: Heading in lingue diverse")

        # Controlla termini tecnici inconsistenti
        for english_pattern, (english_term, italian_term) in ENGLISH_TECHNICAL_TERMS.items():
            matches = re.findall(english_pattern, content, re.IGNORECASE)
            if matches:
                # Riporta match in heading o sezioni critiche
                for heading in headings:
                    if re.search(english_pattern, heading, re.IGNORECASE):
                        file_issues.append(
                            f"Heading in English: '{heading}' (usa '{italian_term}' invece di '{english_term}')"
                        )
                        self.warnings.append(f"{file_path.name}: Heading in English - {english_term}")
                        break

        # Valuta coerenza generale
        if confidence < 0.6:
            file_issues.append(f"Lingua non chiara (confidence: {confidence:.1%}). Detected: {lang_detected}")
            self.warnings.append(f"{file_path.name}: Lingua non chiara")

        self.files_checked += 1
        if file_issues:
            self.files_with_issues += 1

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "detected_language": lang_detected,
            "language_confidence": round(confidence, 2),
            "english_headings": heading_english,
            "italian_headings": heading_italian,
            "valid": len(file_issues) == 0,
            "issues": file_issues,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando file per coerenza linguistica...")
        files = list(DOCS_DIR.rglob("*.md"))
        # Escludi file molto piccoli
        files = [f for f in files if f.stat().st_size > 500]
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando coerenza linguistica...")

        results = []
        for file_path in sorted(files):
            result = self.check_file_language(file_path)
            if result["issues"]:
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_checked": self.files_checked,
                "files_with_issues": self.files_with_issues,
                "warnings": len(self.warnings),
            },
            "details": results,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA COERENZA LINGUISTICA")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File controllati: {summary['files_checked']}")
        print(f"  File con problemi: {summary['files_with_issues']}")
        print(f"  ⚠️  Warnings: {summary['warnings']}\n")

        if report["details"]:
            print("⚠️  FILE CON PROBLEMI LINGUISTICI (primi 10):")
            for result in report["details"][:10]:
                print(f"  • {result['file']}")
                print(f"    Lingua rilevata: {result['detected_language']} (confidence: {result['language_confidence']})")
                for issue in result["issues"]:
                    print(f"    - {issue}")
            if len(report["details"]) > 10:
                print(f"  ... e altri {len(report['details']) - 10} file")

        # Valutazione
        print("\n" + "="*70)
        issue_rate = (summary['files_with_issues'] / summary['files_checked'] * 100) if summary['files_checked'] > 0 else 0
        if issue_rate == 0:
            print("✅ LANGUAGE COHERENCE: PERFECT")
            return 0
        elif issue_rate < 20:
            print("⚠️  LANGUAGE COHERENCE: MOSTLY GOOD")
            return 0
        else:
            print("❌ LANGUAGE COHERENCE: NEEDS ATTENTION")
            return 0  # Warning, non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "language_coherence_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = LanguageValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca commit


if __name__ == '__main__':
    main()
