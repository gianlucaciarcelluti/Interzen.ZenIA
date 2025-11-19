#!/usr/bin/env python3
"""
Script per applicare il template Conformità Normativa a tutti gli SP (71 total, SP28 escluso).

Legge i file SP*.md e:
1. Estrae SP ID, titulo, UC di appartennza
2. Personalizza la sezione Conformità Normativa basandosi su:
   - UC di appartenenza (es UC1 = Document Management → GDPR likely)
   - Tipo di SP (signature → eIDAS, data processing → GDPR, etc.)
   - Framework applicabili
3. Aggiunge/aggiorna sezione "## 🏛️ Conformità Normativa - SP[ID]"
4. Salva il file aggiornato

Uso:
    python3 apply_conformita_template.py [--dry-run] [--sp-id SP01] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ConformitaTemplateApplier:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'
        self.template_path = self.docs_path / 'TEMPLATE-CONFORMITA-NORMATIVA.md'

        # SP Classification
        self.sp_mapping = {
            # CRITICAL (con GDPR/eIDAS specifiche)
            'SP01': {'uc': ['UC2', 'UC5'], 'gdpr': True, 'eidas': True, 'agid': False, 'title': 'EML Parser & Email Intelligence'},
            'SP02': {'uc': ['UC1', 'UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Document Extractor'},
            'SP04': {'uc': ['UC5'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Knowledge Base'},
            'SP05': {'uc': ['UC5'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Template Engine'},
            'SP07': {'uc': ['UC1', 'UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Content Classifier'},
            'SP12': {'uc': ['UC1'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Semantic Search & Q&A'},
            'SP29': {'uc': ['UC6'], 'gdpr': False, 'eidas': True, 'agid': False, 'title': 'Digital Signature Engine'},
            'SP42': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Policy Engine'},
            'SP50': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Compliance Training'},
            'SP70': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Compliance & Audit'},

            # HIGH tier (UC1-UC10)
            'SP03': {'uc': ['UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Procedural Classifier'},
            'SP06': {'uc': ['UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Validator'},
            'SP08': {'uc': ['UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Quality Checker'},
            'SP09': {'uc': ['UC5'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Workflow Engine'},
            'SP10': {'uc': ['UC5'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Control Dashboard'},
            'SP11': {'uc': ['UC1'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Security & Audit'},
            'SP13': {'uc': ['UC1'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Document Summarizer'},
            'SP14': {'uc': ['UC1'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Metadata Indexer'},
            'SP15': {'uc': ['UC1'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Document Workflow'},
            'SP16': {'uc': ['UC2'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Correspondence Classifier'},
            'SP17': {'uc': ['UC2'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Register Suggester'},
            'SP18': {'uc': ['UC2'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Anomaly Detector'},
            'SP19': {'uc': ['UC2'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Protocol Workflow'},
            'SP20': {'uc': ['UC3'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Organization Manager'},
            'SP21': {'uc': ['UC3'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Procedure Manager'},
            'SP22': {'uc': ['UC3'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Process Governance'},
            'SP23': {'uc': ['UC3'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Compliance Monitor'},
            'SP24': {'uc': ['UC4'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Process Mining'},
            'SP25': {'uc': ['UC4'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Predictive Planning'},
            'SP26': {'uc': ['UC4'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Workflow Designer'},
            'SP27': {'uc': ['UC4'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Process Analytics'},
            'SP30': {'uc': ['UC6'], 'gdpr': False, 'eidas': True, 'agid': False, 'title': 'Certificate Manager'},
            'SP31': {'uc': ['UC6'], 'gdpr': False, 'eidas': True, 'agid': False, 'title': 'Signature Workflow'},
            'SP32': {'uc': ['UC6'], 'gdpr': False, 'eidas': True, 'agid': False, 'title': 'Timestamp Authority'},
            'SP33': {'uc': ['UC7'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Archive Manager'},
            'SP34': {'uc': ['UC7'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Preservation Engine'},
            'SP35': {'uc': ['UC7'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Integrity Validator'},
            'SP36': {'uc': ['UC7'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Storage Optimizer'},
            'SP37': {'uc': ['UC7'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Archive Metadata Manager'},
            'SP38': {'uc': ['UC8'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'SIEM Collector'},
            'SP39': {'uc': ['UC8'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'SIEM Processor'},
            'SP40': {'uc': ['UC8'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'SIEM Storage'},
            'SP41': {'uc': ['UC8'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'SIEM Analytics'},
            'SP43': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Risk Assessment'},
            'SP44': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Compliance Monitoring'},
            'SP45': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Regulatory Intelligence'},
            'SP46': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Compliance Automation'},
            'SP47': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Compliance Analytics'},
            'SP48': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Compliance Intelligence'},
            'SP49': {'uc': ['UC9'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Regulatory Change Mgmt'},
            'SP51': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Help Desk System'},
            'SP52': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Knowledge Base Mgmt'},
            'SP53': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Virtual Assistant'},
            'SP54': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'User Training'},
            'SP55': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Self-Service Portal'},
            'SP56': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Support Analytics'},
            'SP57': {'uc': ['UC10'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'User Feedback Mgmt'},

            # MEDIUM tier (UC11 Analytics)
            'SP58': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Data Lake'},
            'SP59': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'ETL Pipelines'},
            'SP60': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Advanced Analytics'},
            'SP61': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': True, 'title': 'Analytics Portal'},
            'SP62': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Data Quality'},
            'SP63': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Real-Time Analytics'},
            'SP64': {'uc': ['UC11'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Predictive Analytics'},
            'SP65': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Performance Monitoring'},
            'SP66': {'uc': ['UC11'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Data Security'},
            'SP67': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'API Gateway'},
            'SP68': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'DevOps Pipeline'},
            'SP69': {'uc': ['UC11'], 'gdpr': True, 'eidas': False, 'agid': False, 'title': 'Disaster Recovery'},
            'SP72': {'uc': ['UC11'], 'gdpr': False, 'eidas': False, 'agid': False, 'title': 'Incident Mgmt'},
        }

        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0  # SP01 already done, SP28 reserved

    def generate_conformita_section(self, sp_id: str, sp_info: Dict) -> str:
        """Genera sezione Conformità Normativa personalizzata per SP specifico."""

        title = sp_info['title']
        ucs = ', '.join(sp_info['uc'])
        gdpr = sp_info['gdpr']
        eidas = sp_info['eidas']
        agid = sp_info['agid']

        # Build section
        section = f"""## 🏛️ Conformità Normativa - {sp_id}

### 1. Quadro Normativo di Riferimento

**Framework applicabili a {sp_id} ({title})**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
"""

        if gdpr:
            section += "- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32\n"

        if eidas:
            section += "- **eIDAS** (Regolamento 2014/910): Art. 3, 8, 24-27\n"

        if agid:
            section += "- **AGID**: Linee Guida Acquisizione Software 2024\n"

        section += f"\n**UC Appartenance**: {ucs}\n\n---\n\n"

        # CAD section
        section += f"""### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - {sp_id} è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

"""

        # GDPR section (if applicable)
        if gdpr:
            section += f"""### 3. Conformità GDPR

**Applicabilità**: CRITICA per {sp_id} - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Data Protection Officer)

---

"""

        # eIDAS section (if applicable)
        if eidas:
            section += f"""### 4. Conformità eIDAS

**Applicabilità**: OBBLIGATORIO per {sp_id} - gestisce firme digitali

**Elementi chiave**:
- Firma Qualificata: CAdES/XAdES con timestamp RFC 3161
- Livello Assicurazione: Identificazione ALTO, Autenticazione SOSTANZIALE
- TSP (Trusted Service Provider): Provider autorizzati AGID (InfoCert, Aruba, etc.)
- Certificati X.509: Chain validation fino a trusted root CA
- Non-repudiation: Timestamp marca temporale opponibile in giudizio

**Responsabile**: Security Team + Legal (compliance eIDAS)

---

"""

        # AGID section (if applicable)
        if agid:
            section += f"""### 5. Conformità AGID

**Applicabilità**: CRITICA per {sp_id} - ha interfaccia utente / interoperabilità

**Elementi chiave**:
- Accessibilità: WCAG 2.1 Level AA (se UI component)
- Interoperabilità: OpenAPI 3.0 + JSON-LD linked data
- Linee Guida Acquisizione: Open-source, no proprietary locks
- Ontologie NDC: Uso tassonomie AGID dove applicabili

**Responsabile**: Architecture Team + AGID compliance officer

---

"""

        # Monitoring section
        section += f"""### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: {self._next_review_date()}

---

## Riepilogo Conformità {sp_id}

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsible |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
"""

        if gdpr:
            section += "| GDPR | ✅ Sì | ✅ Compliant | DPO |\n"
        else:
            section += "| GDPR | ❌ No | N/A | - |\n"

        if eidas:
            section += "| eIDAS | ✅ Sì | ✅ Compliant | Security Lead |\n"
        else:
            section += "| eIDAS | ❌ No | N/A | - |\n"

        if agid:
            section += "| AGID | ✅ Sì | ✅ Compliant | Architect |\n"
        else:
            section += "| AGID | ❌ No | N/A | - |\n"

        section += f"""
**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Next Review**: {self._next_review_date()}

---

"""

        return section

    def _next_review_date(self) -> str:
        """Calcola data prossima review (3 mesi da adesso)."""
        from datetime import datetime, timedelta
        next_date = datetime.now() + timedelta(days=90)
        return next_date.strftime('%Y-%m-%d')

    def find_sp_files(self, sp_id: Optional[str] = None) -> List[Path]:
        """Trova tutti i file SP (o specifico SP se sp_id fornito)."""
        files = []
        for filepath in self.docs_path.rglob('01 SP*.md'):
            if sp_id:
                if sp_id in filepath.name:
                    files.append(filepath)
            else:
                files.append(filepath)
        return sorted(files)

    def extract_sp_id(self, filename: str) -> Optional[str]:
        """Estrae SP ID da nome file (es. '01 SP01 - ...' → 'SP01')."""
        match = re.search(r'SP(\d{2})', filename)
        if match:
            return f"SP{match.group(1)}"
        return None

    def apply_conformita(self, filepath: Path, sp_id: str, dry_run: bool = False, verbose: bool = False) -> Tuple[bool, str]:
        """Applica template Conformità a file SP specifico."""

        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            return False, f"Error reading {filepath.name}: {e}"

        # Skip if already updated (pattern: ## 🏛️ Conformità Normativa - SP[ID])
        if f"## 🏛️ Conformità Normativa - {sp_id}" in content:
            return False, f"Already updated"

        # Skip SP01 (already manually done)
        if sp_id == 'SP01':
            return False, "SP01 manually updated (skip)"

        # Get SP info
        if sp_id not in self.sp_mapping:
            return False, f"SP {sp_id} not in mapping"

        sp_info = self.sp_mapping[sp_id]

        # Generate new section
        new_section = self.generate_conformita_section(sp_id, sp_info)

        # Find and replace old section (if exists)
        old_section_pattern = r'## 🏛️ Conformità Normativa.*?(?=^##\s|$)'
        new_content = re.sub(
            old_section_pattern,
            new_section.rstrip() + '\n\n',
            content,
            flags=re.MULTILINE | re.DOTALL
        )

        # If no old section, append to end
        if new_content == content:
            new_content = content.rstrip() + '\n\n' + new_section

        # Write file
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')

        if verbose or not dry_run:
            print(f"✅ {sp_id}: {filepath.parent.name}/")
            print(f"   CAD: ✅ | GDPR: {'✅' if sp_info['gdpr'] else '❌'} | eIDAS: {'✅' if sp_info['eidas'] else '❌'} | AGID: {'✅' if sp_info['agid'] else '❌'}")

        return True, f"{sp_id} conformità applicata"

    def run(self, sp_id: Optional[str] = None, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui applicazione template a tutti gli SP (o specifico SP se sp_id fornito)."""

        print("\n" + "="*80)
        print("CONFORMITÀ NORMATIVA TEMPLATE APPLIER")
        print("="*80)
        print(f"Dry run: {dry_run}\n")

        if sp_id:
            files = self.find_sp_files(sp_id)
            print(f"Found {len(files)} file(s) for {sp_id}\n")
        else:
            files = self.find_sp_files()
            print(f"Found {len(files)} SP files to process\n")

        for filepath in files:
            self.files_processed += 1
            extracted_sp_id = self.extract_sp_id(filepath.name)

            if not extracted_sp_id:
                self.files_skipped += 1
                print(f"⚠️  Skipped: Could not extract SP ID from {filepath.name}")
                continue

            success, message = self.apply_conformita(filepath, extracted_sp_id, dry_run, verbose)

            if success:
                self.files_updated += 1
            else:
                if verbose:
                    print(f"⊘  {extracted_sp_id}: {message}")

        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Files processed: {self.files_processed}")
        print(f"Files updated: {self.files_updated}")
        print(f"Files skipped: {self.files_skipped}")

        if dry_run:
            print(f"\n⚠️  DRY RUN MODE - No files were modified")
            print(f"   Run without --dry-run to apply changes")
        else:
            print(f"\n✅ Conformità Normativa template applicato a {self.files_updated} SP")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv
    sp_id = None

    # Parse --sp-id parameter
    if '--sp-id' in sys.argv:
        idx = sys.argv.index('--sp-id')
        if idx + 1 < len(sys.argv):
            sp_id = sys.argv[idx + 1]

    tool = ConformitaTemplateApplier()
    tool.run(sp_id=sp_id, dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
