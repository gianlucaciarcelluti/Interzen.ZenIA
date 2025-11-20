#!/usr/bin/env python3
"""
Verifica immagini orfane.

Assicura che:
- Tutte le immagini referenziate esistano
- Nessuna immagine sia inutilizzata (orfana)
- Path immagini siano corretti (relativi, non assoluti)
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Estensioni immagini riconosciute
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}

class ImageValidator:
    def __init__(self):
        self.referenced_images = set()  # Immagini referenziate
        self.existing_images = set()    # Immagini che esistono
        self.errors = []
        self.warnings = []

    def find_all_images(self):
        """Trova tutte le immagini nel repo."""
        print("🔍 Scoprendo immagini...")
        for file_path in DOCS_DIR.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                rel_path = str(file_path.relative_to(DOCS_DIR)).replace('\\', '/')
                self.existing_images.add(rel_path)

        print(f"✅ Trovate {len(self.existing_images)} immagini\n")

    def extract_image_references(self, content: str) -> Set[str]:
        """Estrai riferimenti immagini da markdown."""
        references = set()

        # Pattern markdown: ![alt](path) oppure <img src="path">
        md_pattern = r'!\[.*?\]\((.*?)\)'
        html_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'

        for match in re.finditer(md_pattern, content):
            path = match.group(1).strip()
            if path:
                references.add(path.replace('\\', '/'))

        for match in re.finditer(html_pattern, content):
            path = match.group(1).strip()
            if path:
                references.add(path.replace('\\', '/'))

        return references

    def validate_file(self, file_path: Path) -> Dict:
        """Valida file per riferimenti immagini."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        file_errors = []
        image_refs = self.extract_image_references(content)

        for img_ref in image_refs:
            # Escludi URL esterni (HTTP/HTTPS) - sono validi e non "orfani"
            if img_ref.startswith('http://') or img_ref.startswith('https://'):
                continue

            self.referenced_images.add(img_ref)

            # Controlla path assoluto interno (bad practice)
            if img_ref.startswith('/'):
                file_errors.append(f"Immagine con path assoluto (usa relativi): {img_ref}")
                continue

            # Risolvi path relativo
            file_dir = file_path.parent
            resolved_path = (file_dir / img_ref).resolve()

            # Controlla se esiste
            if not resolved_path.exists():
                rel_to_docs = str(resolved_path.relative_to(DOCS_DIR)).replace('\\', '/') if DOCS_DIR in resolved_path.parents or resolved_path.parent == DOCS_DIR else img_ref
                file_errors.append(f"Immagine non trovata: {img_ref} (resolved: {rel_to_docs})")

        self.errors.extend(file_errors)

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(file_errors) == 0,
            "image_count": len(image_refs),
            "errors": file_errors,
        }

    def validate_all(self):
        """Valida tutti i file."""
        self.find_all_images()
        print("🔍 Scansionando file per riferimenti immagini...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando immagini...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["image_count"] > 0:
                results.append(result)

        # Trova immagini orfane (referenziate ma non trovate)
        self.find_orphaned_images()

        return results

    def find_orphaned_images(self):
        """Trova immagini che non sono referenziate."""
        orphaned = self.existing_images - self.referenced_images

        # Escludiammagini system (favicon, .git, ecc)
        orphaned = {img for img in orphaned if not any(x in img for x in ['.git', 'favicon', 'node_modules'])}

        if orphaned:
            for img in sorted(orphaned)[:10]:
                self.warnings.append(f"Immagine orfana (non referenziata): {img}")
            if len(orphaned) > 10:
                self.warnings.append(f"... e altre {len(orphaned) - 10} immagini orfane")

    def generate_report(self, results: list) -> Dict:
        """Genera report."""
        files_with_errors = len([r for r in results if r["errors"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "total_images": len(self.existing_images),
                "referenced_images": len(self.referenced_images),
                "orphaned_images": len(self.existing_images - self.referenced_images),
                "files_with_images": len(results),
                "files_with_errors": files_with_errors,
                "total_errors": len(self.errors),
                "total_warnings": len(self.warnings),
            },
            "details": results,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA IMMAGINI ORFANE")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  Immagini totali: {summary['total_images']}")
        print(f"  Immagini referenziate: {summary['referenced_images']}")
        print(f"  Immagini orfane: {summary['orphaned_images']}")
        print(f"  File con immagini: {summary['files_with_images']}")
        print(f"  File con errori: {summary['files_with_errors']}")
        print(f"  ❌ Errori: {summary['total_errors']}")
        print(f"  ⚠️  Warnings: {summary['total_warnings']}\n")

        if report["errors"]:
            print("="*70)
            print("❌ ERRORI (primi 15):")
            for i, error in enumerate(report["errors"][:15]):
                print(f"  {i+1}. {error}")
            if len(report["errors"]) > 15:
                print(f"  ... e altri {len(report['errors']) - 15} errori")

        if report["warnings"]:
            print("\n" + "="*70)
            print("⚠️  WARNINGS (primi 10):")
            for warning in report["warnings"][:10]:
                print(f"  • {warning}")
            if len(report["warnings"]) > 10:
                print(f"  ... e altri {len(report['warnings']) - 10} warnings")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0:
            print("✅ IMAGES: ALL VALID")
            return 0
        else:
            print("⚠️  IMAGES: ISSUES FOUND")
            return 0  # Non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "orphaned_images_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = ImageValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
