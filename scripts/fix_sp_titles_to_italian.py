#!/usr/bin/env python3
"""
Script to standardize SP titles to Italian naming convention.

Rinomina i titoli degli SP da inglese a italiano:
- "SP12 - Semantic Search & Q&A Engine" → "SP12 - Ricerca Semantica e Motore Q&A"
- "SP51 - Help Desk System" → "SP51 - Sistema Help Desk"
- etc.

Uso:
    python3 fix_sp_titles_to_italian.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict

class SPTitlesItalianFixer:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'

        # Mapping di traduzioni SP (EN → IT)
        # Note: SP01 e SP02 hanno versioni diverse per UC2 vs UC5, ma lo script le gestisce per UC di appartenenza
        self.title_translations = {
            # UC1 - Gestione Documentale
            "01 SP02 - Document Extractor & Attachment Classifier": "01 SP02 - Estrattore Documenti e Classificatore Allegati",
            "01 SP07 - Content Classifier": "01 SP07 - Classificatore Contenuti",
            "01 SP12 - Semantic Search & Q&A Engine": "01 SP12 - Ricerca Semantica e Motore Q&A",
            "01 SP13 - Document Summarizer": "01 SP13 - Sintetizzatore Documenti",
            "01 SP14 - Metadata Indexer": "01 SP14 - Indicizzatore Metadati",
            "01 SP15 - Document Workflow Orchestrator": "01 SP15 - Orchestratore Workflow Documenti",

            # UC2 - Protocollo Informatico
            "01 SP01 - EML Parser & Email Intelligence (UC2 Protocol)": "01 SP01 - Parser EML e Intelligenza Email (Protocollo UC2)",
            "01 SP16 - Correspondence Classifier": "01 SP16 - Classificatore Corrispondenza",
            "01 SP17 - Registry Suggester": "01 SP17 - Suggeritore Registro",
            "01 SP18 - Anomaly Detector": "01 SP18 - Rilevatore Anomalie",
            "01 SP19 - Protocol Workflow Orchestrator": "01 SP19 - Orchestratore Workflow Protocollo",

            # UC3 - Governance
            "01 SP20 - Organization Chart Manager": "01 SP20 - Gestione Organigramma",
            "01 SP21 - Procedure Manager": "01 SP21 - Gestore Procedure",
            "01 SP22 - Process Governance": "01 SP22 - Governance Processi",
            "01 SP23 - Compliance Monitor": "01 SP23 - Monitor Conformità",

            # UC4 - BPM
            "01 SP24 - Process Mining Engine": "01 SP24 - Motore Process Mining",
            "01 SP25 - Forecasting & Predictive Scheduling Engine": "01 SP25 - Motore Previsioni e Pianificazione Predittiva",
            "01 SP26 - Intelligent Workflow Designer": "01 SP26 - Progettista Workflow Intelligente",
            "01 SP27 - Process Analytics": "01 SP27 - Analitiche Processi",

            # UC5 - Produzione Documentale Integrata
            "01 SP01 - EML Parser & Email Intelligence": "01 SP01 - Parser EML e Intelligenza Email",
            "01 SP04 - Knowledge Base": "01 SP04 - Base Conoscenze",
            "01 SP05 - Template Engine": "01 SP05 - Motore Template",
            "01 SP08 - Quality Checker": "01 SP08 - Verificatore Qualità",
            "01 SP09 - Workflow Engine": "01 SP09 - Motore Workflow",
            "01 SP10 - Dashboard": "01 SP10 - Pannello di Controllo",
            "01 SP11 - Security & Audit": "01 SP11 - Sicurezza e Audit",

            # UC6 - Firma Digitale
            "01 SP29 - Digital Signature Engine": "01 SP29 - Motore Firma Digitale",
            "01 SP30 - Certificate Manager": "01 SP30 - Gestore Certificati",
            "01 SP31 - Signature Workflow": "01 SP31 - Workflow Firma",
            "01 SP32 - Timestamp Authority & Temporal Marking": "01 SP32 - Autorità Timestamp e Marcatura Temporale",

            # UC7 - Archivio e Conservazione
            "01 SP33 - Archive Manager": "01 SP33 - Gestore Archivio",
            "01 SP34 - Preservation Engine": "01 SP34 - Motore Conservazione",
            "01 SP35 - Integrity Validator": "01 SP35 - Validatore Integrità",
            "01 SP36 - Storage Optimizer": "01 SP36 - Ottimizzatore Archiviazione",
            "01 SP37 - Archive Metadata Manager": "01 SP37 - Gestore Metadati Archivio",

            # UC8 - SIEM
            "01 SP38 - SIEM Collector": "01 SP38 - Collettore SIEM",
            "01 SP39 - SIEM Processor": "01 SP39 - Elaboratore SIEM",
            "01 SP40 - SIEM Storage": "01 SP40 - Archiviazione SIEM",
            "01 SP41 - SIEM Analytics & Reporting": "01 SP41 - Analitiche SIEM e Reporting",

            # UC9 - Compliance
            "01 SP42 - Policy Engine": "01 SP42 - Motore Politiche",
            "01 SP43 - Risk Assessment Engine": "01 SP43 - Motore Valutazione Rischi",
            "01 SP44 - Compliance Monitoring System": "01 SP44 - Sistema Monitoraggio Conformità",
            "01 SP45 - Regulatory Intelligence Hub": "01 SP45 - Hub Intelligenza Normativa",
            "01 SP46 - Compliance Automation Platform": "01 SP46 - Piattaforma Automazione Conformità",
            "01 SP47 - Compliance Analytics & Reporting": "01 SP47 - Analitiche Conformità e Reporting",
            "01 SP48 - Compliance Intelligence Platform": "01 SP48 - Piattaforma Intelligenza Conformità",
            "01 SP49 - Regulatory Change Management": "01 SP49 - Gestione Cambiamenti Normativi",
            "01 SP50 - Compliance Training & Certification": "01 SP50 - Formazione Conformità e Certificazione",

            # UC10 - Supporto Utente
            "01 SP51 - Help Desk System": "01 SP51 - Sistema Help Desk",
            "01 SP52 - Knowledge Base Management": "01 SP52 - Gestione Base Conoscenze",
            "01 SP53 - Virtual Assistant & Chatbot": "01 SP53 - Assistente Virtuale e Chatbot",
            "01 SP54 - User Training Platform": "01 SP54 - Piattaforma Formazione Utenti",
            "01 SP55 - Self-Service Portal": "01 SP55 - Portale Self-Service",
            "01 SP56 - Support Analytics & Reporting": "01 SP56 - Analitiche Supporto e Reporting",
            "01 SP57 - User Feedback Management": "01 SP57 - Gestione Feedback Utenti",

            # UC11 - Analytics & Reporting
            "01 SP58 - Data Lake & Storage Management": "01 SP58 - Data Lake e Gestione Archiviazione",
            "01 SP59 - ETL & Data Processing Pipelines": "01 SP59 - Pipeline ETL e Elaborazione Dati",
            "01 SP60 - Advanced Analytics & ML": "01 SP60 - Analitiche Avanzate e Machine Learning",
            "01 SP61 - Self-Service Analytics Portal": "01 SP61 - Portale Analitiche Self-Service",
            "01 SP62 - Data Quality & Governance": "01 SP62 - Qualità Dati e Governance",
            "01 SP63 - Real-Time Analytics & Streaming": "01 SP63 - Analitiche Real-Time e Streaming",
            "01 SP64 - Predictive Analytics & Forecasting": "01 SP64 - Analitiche Predittive e Previsioni",
            "01 SP65 - Performance Monitoring & Alerting": "01 SP65 - Monitoraggio Prestazioni e Avvisi",
            "01 SP66 - Data Security & Compliance": "01 SP66 - Sicurezza Dati e Conformità",
            "01 SP67 - API Gateway & Integration Layer": "01 SP67 - Gateway API e Livello Integrazione",
            "01 SP68 - DevOps & CI CD Pipeline": "01 SP68 - DevOps e Pipeline CI CD",
            "01 SP69 - Disaster Recovery & Business Continuity": "01 SP69 - Disaster Recovery e Continuità Aziendale",
            "01 SP70 - Compliance & Audit Management": "01 SP70 - Gestione Conformità e Audit",
            "01 SP71 - Performance Optimization & Scaling": "01 SP71 - Ottimizzazione Prestazioni e Scalabilità",
            "01 SP72 - Incident Management & Escalation": "01 SP72 - Gestione Incidenti e Escalation",
        }

        self.files_processed = 0
        self.files_renamed = 0
        self.references_updated = 0

    def find_sp_files(self) -> List[Path]:
        """Trova tutti i file SP"""
        files = []
        for filepath in self.docs_path.rglob('01 SP*.md'):
            files.append(filepath)
        return sorted(files)

    def rename_sp_file(self, filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
        """Rinomina un file SP se ha un titolo da tradurre"""
        filename = filepath.name

        # Estrai il titolo dal nome file (tutto dopo "01 SP")
        match = re.match(r'(01 SP\d+ - .+?)\.md$', filename)
        if not match:
            return False, f"Could not parse filename: {filename}"

        old_title = match.group(1)

        # Cerca la traduzione
        if old_title in self.title_translations:
            new_title = self.title_translations[old_title]
            new_filename = f"{new_title}.md"
            new_filepath = filepath.parent / new_filename

            if not dry_run:
                filepath.rename(new_filepath)

            return True, f"{old_title} → {new_title}"

        return False, None

    def update_references_in_readmes(self, old_title: str, new_title: str, dry_run: bool = False) -> int:
        """Aggiorna i riferimenti nei file README.md"""
        count = 0

        # Cerca tutti i file README.md
        for readme_path in self.docs_path.rglob('README.md'):
            try:
                content = readme_path.read_text(encoding='utf-8')
                if old_title in content:
                    new_content = content.replace(old_title, new_title)
                    if not dry_run:
                        readme_path.write_text(new_content, encoding='utf-8')
                    count += 1
            except Exception:
                # Skip files that cannot be read
                continue

        return count

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui le correzioni"""

        print("\n" + "="*70)
        print("SP TITLES ITALIAN STANDARDIZATION TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files = self.find_sp_files()
        print(f"Found {len(files)} SP files to process\n")

        renamed_count = 0

        for filepath in files:
            self.files_processed += 1
            success, message = self.rename_sp_file(filepath, dry_run)

            if success:
                renamed_count += 1
                if verbose or not dry_run:
                    print(f"✅ {filepath.parent.name}/")
                    print(f"   {message}")

                # Update references
                old_match = re.match(r'(01 SP\d+ - .+?)\.md$', filepath.name)
                if old_match:
                    old_title = old_match.group(1)
                    new_title = self.title_translations[old_title]
                    refs = self.update_references_in_readmes(old_title, new_title, dry_run)
                    if refs > 0:
                        self.references_updated += refs

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files renamed: {renamed_count}")
        print(f"References updated: {self.references_updated}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All SP titles standardized to Italian")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = SPTitlesItalianFixer()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
