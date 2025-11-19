#!/usr/bin/env python3
"""
Script to rename all "README.md" files to "README.md" and update all references.

Performs:
- Rename: 00 INDEX.md → README.md in all UC folders
- Update: All references to "README.md" in documentation and scripts
- Update: Navigation links and cross-references

Uso:
    python3 rename_index_to_readme.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict
import shutil

class IndexToReadmeRenamingTool:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'
        self.scripts_path = self.root_path / 'scripts'
        self.files_processed = 0
        self.files_changed = 0
        self.files_renamed = 0
        self.replacements = 0
        self.changes_log = []

    def find_index_files(self) -> List[Path]:
        """Trova tutti i file "README.md" """
        files = []
        for filepath in self.docs_path.rglob('README.md'):
            files.append(filepath)
        return sorted(files)

    def find_files_with_index_references(self) -> List[Tuple[Path, List[str]]]:
        """Trova tutti i file che contengono riferimenti a 00 INDEX.md"""
        files_with_refs = []
        patterns_to_find = [
            r'00 INDEX\.md',
            r'\(00 INDEX\.md\)',
            r'\[.*?\]\(.*?00 INDEX\.md\)',
            r'./00 INDEX\.md',
        ]

        for filepath in self.docs_path.rglob('*.md'):
            try:
                content = filepath.read_text(encoding='utf-8')
                refs = []
                for pattern in patterns_to_find:
                    if re.search(pattern, content):
                        refs.append(pattern)
                if refs:
                    files_with_refs.append((filepath, refs))
            except:
                pass

        # Anche i file Python negli scripts
        for filepath in self.scripts_path.glob('*.py'):
            try:
                content = filepath.read_text(encoding='utf-8')
                if 'README.md' in content:
                    files_with_refs.append((filepath, ['README.md']))
            except:
                pass

        return sorted(files_with_refs)

    def update_file_references(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """Aggiorna i riferimenti a 00 INDEX.md in un file"""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Sostituzioni specifiche a seconda del tipo di file
            replacements_count = 0

            # Pattern 1: Markdown links [text](path/README.md) → [text](path/README.md)
            new_content = re.sub(
                r'(\[.*?\]\(.*?)00 INDEX\.md',
                r'\1README.md',
                content
            )
            if new_content != content:
                replacements_count += content.count('README.md') - new_content.count('README.md')
                content = new_content
                changes.append(f"Updated markdown links: 00 INDEX.md → README.md")

            # Pattern 2: Plain text references ./README.md → ./README.md
            new_content = content.replace('./README.md', './README.md')
            if new_content != content:
                replacements_count += content.count('./README.md') - new_content.count('./README.md')
                content = new_content
                changes.append(f"Updated relative paths: ./README.md → ./README.md")

            # Pattern 3: Plain references in Python strings
            new_content = content.replace("'README.md'", "'README.md'")
            if new_content != content:
                replacements_count += content.count("'README.md'") - new_content.count("'README.md'")
                content = new_content
                changes.append(f"Updated Python string references")

            new_content = content.replace('"README.md"', '"README.md"')
            if new_content != content:
                replacements_count += content.count('"README.md"') - new_content.count('"README.md"')
                content = new_content
                changes.append(f"Updated Python string references (double quotes)")

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                return replacements_count, changes

            return 0, []

        except Exception as e:
            return 0, [f"Error: {e}"]

    def rename_files(self, index_files: List[Path], dry_run: bool = False) -> List[str]:
        """Rinomina tutti i file 00 INDEX.md in README.md"""
        results = []

        for filepath in index_files:
            target_path = filepath.parent / 'README.md'

            # Verifica se il README esiste già
            if target_path.exists() and not dry_run:
                results.append(f"⚠️  {target_path.relative_to(self.docs_path)} already exists - skipping")
                continue

            if not dry_run:
                shutil.move(str(filepath), str(target_path))
                self.files_renamed += 1
                results.append(f"✅ Renamed: {filepath.relative_to(self.docs_path)} → {target_path.relative_to(self.docs_path)}")
            else:
                results.append(f"📝 [DRY RUN] Would rename: {filepath.relative_to(self.docs_path)} → {target_path.relative_to(self.docs_path)}")

        return results

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui tutte le operazioni di rinomina"""

        print("\n" + "="*70)
        print("INDEX.MD → README.MD RENAMING TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        # Step 1: Find all INDEX files
        index_files = self.find_index_files()
        print(f"Found {len(index_files)} INDEX files to rename:\n")
        for f in index_files:
            print(f"  - {f.relative_to(self.docs_path)}")

        # Step 2: Find all references
        print(f"\nSearching for references to 00 INDEX.md...\n")
        files_with_refs = self.find_files_with_index_references()
        print(f"Found {len(files_with_refs)} files with references:\n")

        if verbose:
            for filepath, _ in files_with_refs:
                print(f"  - {filepath.relative_to(self.root_path)}")

        # Step 3: Update references
        print("\n" + "="*70)
        print("UPDATING REFERENCES")
        print("="*70 + "\n")

        for filepath, _ in files_with_refs:
            self.files_processed += 1
            count, changes = self.update_file_references(filepath, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                if filepath.is_relative_to(self.docs_path):
                    rel_path = filepath.relative_to(self.docs_path)
                else:
                    rel_path = filepath.relative_to(self.root_path)

                print(f"✅ {rel_path}")

                if verbose:
                    for change in changes:
                        print(f"   • {change}")
                else:
                    print(f"   {count} reference(s) updated")

        # Step 4: Rename files
        print("\n" + "="*70)
        print("RENAMING FILES")
        print("="*70 + "\n")

        rename_results = self.rename_files(index_files, dry_run)
        for result in rename_results:
            print(result)

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed for reference updates: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Total references updated: {self.replacements}")
        print(f"Files renamed: {self.files_renamed}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All changes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = IndexToReadmeRenamingTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
