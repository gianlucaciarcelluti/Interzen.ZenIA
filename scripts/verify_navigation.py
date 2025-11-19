#!/usr/bin/env python3
"""
Script per verificare la navigabilità completa della documentazione ZenIA.

Testa:
1. Entry points principali (README.md files)
2. Accessibilità UC INDEX da README.md
3. Accessibilità SP da UC INDEX
4. Accessibilità template da SP
5. Cross-references tra file
6. Ricercabilità termini da GLOSSARIO

Uso:
    python3 verify_navigation.py [--verbose] [--report]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import defaultdict

class NavigationVerifier:
    def __init__(self):
        # Trova la cartella docs in maniera robusta
        script_dir = Path(__file__).parent.parent
        self.base_path = script_dir / 'docs'

        # Verifica che il path esiste
        if not self.base_path.exists():
            print(f"❌ Errore: cartella docs non trovata in {self.base_path}")
            sys.exit(1)

        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)

    def verify_all(self, verbose: bool = False) -> bool:
        """Esegue tutte le verifiche di navigabilità"""

        print("\n" + "="*70)
        print("🗺️  VERIFICA NAVIGABILITÀ DOCUMENTAZIONE ZenIA")
        print("="*70 + "\n")

        # Test 1: Entry Points
        print("1️⃣  Testing Entry Points...")
        self.test_entry_points(verbose)

        # Test 2: UC INDEX Accessibility
        print("\n2️⃣  Testing UC INDEX Accessibility...")
        self.test_uc_index_accessibility(verbose)

        # Test 3: SP Accessibility from UC INDEX
        print("\n3️⃣  Testing SP Accessibility from UC INDEX...")
        self.test_sp_accessibility(verbose)

        # Test 4: Template Links
        print("\n4️⃣  Testing Template References...")
        self.test_template_links(verbose)

        # Test 5: Cross-References
        print("\n5️⃣  Testing Cross-References...")
        self.test_cross_references(verbose)

        # Test 6: Glossario Accessibility
        print("\n6️⃣  Testing Glossario Accessibility...")
        self.test_glossario_accessibility(verbose)

        # Test 7: Navigation Paths
        print("\n7️⃣  Testing Common Navigation Paths...")
        self.test_navigation_paths(verbose)

        # Report
        self.print_report()

        return len(self.errors) == 0

    def test_entry_points(self, verbose: bool):
        """Verifica che gli entry point principali esistono e sono ben formati"""

        entry_points = [
            ('README.md', 'Main README'),
            ('use_cases/README.md', 'Use Cases README'),
            ('GLOSSARIO-TERMINOLOGICO.md', 'Glossario'),
        ]

        for file_path, desc in entry_points:
            full_path = self.base_path / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Verifica struttura base
                    if '# ' in content:
                        self.stats['entry_points_ok'] += 1
                        if verbose:
                            print(f"  ✅ {desc}: OK")
                    else:
                        self.errors.append(f"{desc} manca di header principale")
            else:
                self.errors.append(f"Entry point mancante: {file_path}")

    def test_uc_index_accessibility(self, verbose: bool):
        """Verifica che tutti gli UC INDEX sono accessibili e linked"""

        use_cases_path = self.base_path / 'use_cases'
        uc_folders = [f for f in use_cases_path.iterdir() if f.is_dir() and f.name.startswith('UC')]

        for uc_folder in sorted(uc_folders):
            index_file = uc_folder / 'README.md'

            if index_file.exists():
                self.stats['uc_index_found'] += 1
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Verifica elementi cruciali nell'INDEX
                checks = [
                    ('# UC', 'Header principale'),
                    ('Navigation Matrix', 'Navigation Matrix'),
                    ('Overview', 'Overview section'),
                ]

                all_ok = True
                for pattern, name in checks:
                    if pattern not in content:
                        self.warnings.append(f"{uc_folder.name}/00 INDEX.md manca: {name}")
                        all_ok = False

                if all_ok:
                    self.stats['uc_index_complete'] += 1
                    if verbose:
                        print(f"  ✅ {uc_folder.name}/00 INDEX.md: Completo")
            else:
                self.errors.append(f"INDEX mancante: {uc_folder.name}/00 INDEX.md")

    def test_sp_accessibility(self, verbose: bool):
        """Verifica che SP sono linkati negli UC INDEX"""

        use_cases_path = self.base_path / 'use_cases'

        for uc_folder in sorted(use_cases_path.glob('UC*')):
            if not uc_folder.is_dir():
                continue

            index_file = uc_folder / 'README.md'
            if not index_file.exists():
                continue

            # Trova tutti gli SP in questa UC
            sp_files = list(uc_folder.glob('01 SP*.md'))

            with open(index_file, 'r', encoding='utf-8') as f:
                index_content = f.read()

            # Verifica che gli SP sono linkati nell'INDEX
            linked_count = 0
            for sp_file in sp_files:
                # Cerca link al file SP nell'INDEX (con o senza anchor)
                sp_name = sp_file.name
                if sp_name in index_content or f"[{sp_name}" in index_content:
                    linked_count += 1
                else:
                    self.warnings.append(f"{uc_folder.name}: SP {sp_name} non linkato in INDEX")

            if linked_count > 0:
                self.stats['sp_linked'] += linked_count
                if verbose and linked_count == len(sp_files):
                    print(f"  ✅ {uc_folder.name}: Tutti {len(sp_files)} SP linkati")

    def test_template_links(self, verbose: bool):
        """Verifica che i template sono linkati dove necessario"""

        templates = [
            ('templates/json-payload-standard.md', 'JSON Payload Standard'),
            ('templates/conformita-normativa-standard.md', 'Conformità Normativa'),
            ('templates/uc-index-standard.md', 'UC INDEX Standard'),
        ]

        # Verifica che i template esistono
        for file_path, desc in templates:
            full_path = self.base_path / file_path
            if full_path.exists():
                self.stats['templates_found'] += 1
                if verbose:
                    print(f"  ✅ {desc}: Esiste")
            else:
                self.errors.append(f"Template mancante: {file_path}")

        # Verifica che i template sono referenziati in SP
        sp_files = list(self.base_path.glob('use_cases/**/*.md'))
        sp_files = [f for f in sp_files if re.search(r'01 SP\d{2}', f.name)]

        template_references = defaultdict(int)
        for sp_file in sp_files:
            with open(sp_file, 'r', encoding='utf-8') as f:
                content = f.read()

            for file_path, desc in templates:
                filename = Path(file_path).name
                if filename in content:
                    template_references[desc] += 1

        for desc, count in template_references.items():
            if count > 0:
                self.stats[f'template_ref_{desc}'] = count
                if verbose:
                    print(f"  ✅ {desc}: Referenziato in {count} SP")

    def test_cross_references(self, verbose: bool):
        """Verifica cross-references tra UC"""

        # Cartella use_cases README
        readme_path = self.base_path / 'use_cases' / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Verifica che cita i file principali
            checks = [
                ('GLOSSARIO-TERMINOLOGICO', 'Glossario'),
                ('COMPLIANCE-MATRIX', 'Compliance Matrix'),
            ]

            for pattern, name in checks:
                if pattern in content:
                    self.stats[f'cross_ref_{name}'] = 1
                    if verbose:
                        print(f"  ✅ use_cases/README.md cita: {name}")
                else:
                    self.warnings.append(f"use_cases/README.md non cita: {name}")

    def test_glossario_accessibility(self, verbose: bool):
        """Verifica che il Glossario è ben formato e linkabile"""

        glossario_path = self.base_path / 'GLOSSARIO-TERMINOLOGICO.md'

        if glossario_path.exists():
            with open(glossario_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Conta termini (header ### per ogni termine)
            term_count = len(re.findall(r'^### ', content, re.MULTILINE))

            if term_count > 40:  # Dovrebbe averne 50+
                self.stats['glossario_terms'] = term_count
                if verbose:
                    print(f"  ✅ Glossario contiene {term_count} termini")
            else:
                self.warnings.append(f"Glossario contiene solo {term_count} termini (attesi 50+)")

            # Verifica anchor link format (### Termine)
            if '###' in content:
                self.stats['glossario_anchors'] = 1
                if verbose:
                    print(f"  ✅ Glossario ha structure con anchor link")
        else:
            self.errors.append("Glossario non trovato")

    def test_navigation_paths(self, verbose: bool):
        """Testa percorsi di navigazione comuni per verificare usabilità"""

        paths = [
            ('Scenario 1: Nuovo developer → UC1', [
                ('README.md', 'entry point'),
                ('use_cases/README.md', 'use case list'),
                ('use_cases/UC1 - Sistema di Gestione Documentale/00 INDEX.md', 'uc index'),
                ('use_cases/UC1 - Sistema di Gestione Documentale/01 SP02 - Document Extractor & Attachment Classifier.md', 'sp detail'),
            ]),
            ('Scenario 2: Compliance Officer → Conformità', [
                ('README.md', 'entry point'),
                ('GLOSSARIO-TERMINOLOGICO.md', 'termini'),
                ('COMPLIANCE-MATRIX.md', 'compliance matrix'),
            ]),
            ('Scenario 3: Developer → JSON Standard', [
                ('README.md', 'entry point'),
                ('templates/json-payload-standard.md', 'json template'),
            ]),
        ]

        for scenario_name, path_steps in paths:
            all_exist = True
            missing = []

            for file_path, desc in path_steps:
                full_path = self.base_path / file_path
                if not full_path.exists():
                    all_exist = False
                    missing.append(f"{desc} ({file_path})")

            if all_exist:
                self.stats['navigation_paths_ok'] += 1
                if verbose:
                    print(f"  ✅ {scenario_name}: Completo")
            else:
                self.warnings.append(f"{scenario_name}: Missing {', '.join(missing)}")

    def print_report(self):
        """Stampa report finale"""

        print("\n" + "="*70)
        print("📊 REPORT NAVIGABILITÀ")
        print("="*70 + "\n")

        # Summary
        print("✅ VERIFICHE PASSATE:")
        for key, value in sorted(self.stats.items()):
            if isinstance(value, int) and value > 0:
                # Semplifica nomi di stat
                display_key = key.replace('_', ' ').title()
                print(f"   • {display_key}: {value}")

        if self.warnings:
            print("\n⚠️  WARNINGS (non-critiche):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")

        if self.errors:
            print("\n❌ ERRORI (critici):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")

        # Overall assessment
        print("\n" + "="*70)
        if not self.errors and len(self.warnings) < 3:
            print("✅ NAVIGABILITÀ: ECCELLENTE")
            print("   La documentazione è ben organizzata e facilmente navigabile")
        elif not self.errors:
            print("✅ NAVIGABILITÀ: BUONA")
            print("   La documentazione è navigabile con piccole migliorie consigliate")
        else:
            print("⚠️  NAVIGABILITÀ: MEDIOCRE")
            print("   Sono necessarie correzioni critiche")

        print("="*70 + "\n")

        # Score
        total_checks = sum(1 for _ in self.stats) + len(self.warnings) + len(self.errors)
        passed_checks = sum(self.stats.values())
        if total_checks > 0:
            score = (passed_checks / (total_checks + len(self.errors))) * 100
            print(f"📈 Score di Navigabilità: {score:.1f}%")

        return len(self.errors) == 0


def main():
    verbose = '--verbose' in sys.argv

    verifier = NavigationVerifier()
    success = verifier.verify_all(verbose=verbose)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
