#!/usr/bin/env python3
"""
Script per sostituire nomi SP in inglese con versioni italiane nella sezione Conformità.

Esempio: "Procedural Classifier" → "Classificatore Procedurale"
"""

import sys
import re
from pathlib import Path

class ConformitaSPNamesFixer:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'

        # Mapping SP names EN → IT per sezione Conformità
        self.sp_name_fixes = {
            # UC1
            "Document Extractor & Attachment Classifier": "Estrattore Documenti e Classificatore Allegati",
            "Content Classifier": "Classificatore Contenuti",
            "Semantic Search & Q&A Engine": "Ricerca Semantica e Motore Q&A",
            "Document Summarizer": "Sintetizzatore Documenti",
            "Metadata Indexer": "Indicizzatore Metadati",
            "Document Workflow Orchestrator": "Orchestratore Workflow Documenti",
            "Security & Audit": "Sicurezza e Audit",

            # UC2
            "EML Parser & Email Intelligence": "Parser EML e Intelligenza Email",
            "Correspondence Classifier": "Classificatore Corrispondenza",
            "Register Suggester": "Suggeritore Registro",
            "Anomaly Detector": "Rilevatore Anomalie",
            "Protocol Workflow Orchestrator": "Orchestratore Workflow Protocollo",

            # UC3
            "Organization Chart Manager": "Gestione Organigramma",
            "Procedure Manager": "Gestore Procedure",
            "Process Governance": "Governance Processi",
            "Compliance Monitor": "Monitor Conformità",

            # UC4
            "Process Mining Engine": "Motore Process Mining",
            "Forecasting & Predictive Scheduling Engine": "Motore Previsioni e Pianificazione Predittiva",
            "Intelligent Workflow Designer": "Progettista Workflow Intelligente",
            "Process Analytics": "Analitiche Processi",

            # UC5
            "Knowledge Base": "Base Conoscenze",
            "Template Engine": "Motore Template",
            "Quality Checker": "Verificatore Qualità",
            "Workflow Engine": "Motore Workflow",
            "Dashboard": "Pannello di Controllo",
            "Procedural Classifier": "Classificatore Procedurale",
            "Validator": "Validatore",
            "Control Dashboard": "Pannello di Controllo",

            # UC6
            "Digital Signature Engine": "Motore Firma Digitale",
            "Certificate Manager": "Gestore Certificati",
            "Signature Workflow": "Workflow Firma",
            "Timestamp Authority & Temporal Marking": "Autorità Timestamp e Marcatura Temporale",

            # UC7
            "Archive Manager": "Gestore Archivio",
            "Preservation Engine": "Motore Conservazione",
            "Integrity Validator": "Validatore Integrità",
            "Storage Optimizer": "Ottimizzatore Archiviazione",
            "Archive Metadata Manager": "Gestore Metadati Archivio",

            # UC8
            "SIEM Collector": "Collettore SIEM",
            "SIEM Processor": "Elaboratore SIEM",
            "SIEM Storage": "Archiviazione SIEM",
            "SIEM Analytics & Reporting": "Analitiche SIEM e Reporting",

            # UC9
            "Policy Engine": "Motore Politiche",
            "Risk Assessment Engine": "Motore Valutazione Rischi",
            "Compliance Monitoring System": "Sistema Monitoraggio Conformità",
            "Regulatory Intelligence Hub": "Hub Intelligenza Normativa",
            "Compliance Automation Platform": "Piattaforma Automazione Conformità",
            "Compliance Analytics & Reporting": "Analitiche Conformità e Reporting",
            "Compliance Intelligence Platform": "Piattaforma Intelligenza Conformità",
            "Regulatory Change Management": "Gestione Cambiamenti Normativi",
            "Compliance Training & Certification": "Formazione Conformità e Certificazione",

            # UC10
            "Help Desk System": "Sistema Help Desk",
            "Knowledge Base Management": "Gestione Base Conoscenze",
            "Virtual Assistant & Chatbot": "Assistente Virtuale e Chatbot",
            "User Training Platform": "Piattaforma Formazione Utenti",
            "Self-Service Portal": "Portale Self-Service",
            "Support Analytics & Reporting": "Analitiche Supporto e Reporting",
            "User Feedback Management": "Gestione Feedback Utenti",

            # UC11
            "Data Lake & Storage Management": "Data Lake e Gestione Archiviazione",
            "ETL & Data Processing Pipelines": "Pipeline ETL e Elaborazione Dati",
            "Advanced Analytics & ML": "Analitiche Avanzate e Machine Learning",
            "Self-Service Analytics Portal": "Portale Analitiche Self-Service",
            "Data Quality & Governance": "Qualità Dati e Governance",
            "Real-Time Analytics & Streaming": "Analitiche Real-Time e Streaming",
            "Predictive Analytics & Forecasting": "Analitiche Predittive e Previsioni",
            "Performance Monitoring & Alerting": "Monitoraggio Prestazioni e Avvisi",
            "Data Security & Compliance": "Sicurezza Dati e Conformità",
            "API Gateway & Integration Layer": "Gateway API e Livello Integrazione",
            "DevOps & CI CD Pipeline": "DevOps e Pipeline CI CD",
            "Disaster Recovery & Business Continuity": "Disaster Recovery e Continuità Aziendale",
            "Compliance & Audit Management": "Gestione Conformità e Audit",
            "Performance Optimization & Scaling": "Ottimizzazione Prestazioni e Scalabilità",
            "Incident Management & Escalation": "Gestione Incidenti e Escalation",
        }

        self.files_processed = 0
        self.files_updated = 0

    def fix_file(self, filepath: Path, dry_run: bool = False) -> bool:
        """Applica correzioni ai nomi SP."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ❌ Error reading {filepath.name}: {e}")
            return False

        original_content = content

        # Additional fixes for parenthetical references and headers
        additional_fixes = {
            'UC Appartenance': 'UC di Appartenenza',
            'UC appartenance': 'UC di appartenenza',
            '(SP01)': '(SP01)',  # Keep SP IDs
            '(SP02)': '(SP02)',
            '(Procedural Classifier)': '(Classificatore Procedurale)',
            '(Policy Engine)': '(Motore Politiche)',
        }

        # Apply terminology replacements - ONLY in Conformità sections
        def replace_in_conformita(match):
            conformita_section = match.group(0)
            # SP name fixes
            for english_name, italian_name in self.sp_name_fixes.items():
                conformita_section = conformita_section.replace(english_name, italian_name)
            # Additional fixes
            for english_term, italian_term in additional_fixes.items():
                conformita_section = conformita_section.replace(english_term, italian_term)
            return conformita_section

        # Match Conformità sections with re.DOTALL flag
        content = re.sub(
            r'## 🏛️ Conformità Normativa.+?(?=\n## |\Z)',
            replace_in_conformita,
            content,
            flags=re.DOTALL
        )

        # Check if changes were made
        if content == original_content:
            return False

        # Write file if not dry-run
        if not dry_run:
            filepath.write_text(content, encoding='utf-8')

        return True

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui correzioni."""

        print("\n" + "="*80)
        print("CONFORMITÀ SP NAMES FIXER")
        print("="*80)
        print(f"Dry run: {dry_run}\n")

        files = list(self.docs_path.rglob('01 SP*.md'))
        print(f"Found {len(files)} SP files\n")

        for filepath in sorted(files):
            self.files_processed += 1
            if self.fix_file(filepath, dry_run):
                self.files_updated += 1
                if verbose or not dry_run:
                    print(f"✅ Fixed: {filepath.parent.name}/")
                    print(f"   {filepath.name}")

        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Files processed: {self.files_processed}")
        print(f"Files updated: {self.files_updated}")

        if dry_run:
            print(f"\n⚠️  DRY RUN MODE - No files were modified")
        else:
            print(f"\n✅ SP names standardized in {self.files_updated} files")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = ConformitaSPNamesFixer()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
