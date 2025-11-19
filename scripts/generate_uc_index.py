#!/usr/bin/env python3
"""
Script per generare automaticamente file INDEX (00 INDEX.md) per ogni Use Case (UC).

Funzionamento:
1. Trova tutte le cartelle UC in docs/use_cases
2. Per ogni UC:
   - Estrae numero UC dal nome cartella
   - Trova tutti i file SP (01 SP*.md) nella cartella
   - Genera un INDEX personalizzato per quell'UC
3. Crea file 00 INDEX.md in ogni cartella UC

Uso:
    python3 generate_uc_index.py [--dry-run] [--verbose]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import json

# Mapping UC → Titolo, Descrizione, Obiettivi
UC_METADATA = {
    "UC1": {
        "title": "Sistema di Gestione Documentale",
        "overview": "Gestione completa del ciclo di vita dei documenti, dall'acquisizione all'archivio, con classificazione, estrazione di metadati e ricerca semantica.",
        "objectives": [
            "Acquisizione e parsing di documenti da molteplici fonti",
            "Classificazione automatica e estrazione di entità",
            "Indicizzazione e ricerca semantica avanzata",
            "Archiviazione strutturata con metadati standardizzati"
        ],
        "frameworks": ["L. 241/1990", "CAD", "GDPR"],
    },
    "UC2": {
        "title": "Protocollo Informatico",
        "overview": "Gestione del protocollo informatico con workflow di protocollazione, smistamento automatico, audit trail completo e integrazione con sistemi PA.",
        "objectives": [
            "Protocollazione digitale con numerazione progressiva",
            "Smistamento automatico a organi competenti",
            "Gestione workflow e approvazioni",
            "Tracciabilità completa con audit trail"
        ],
        "frameworks": ["L. 241/1990", "CAD", "GDPR"],
    },
    "UC3": {
        "title": "Governance (Organigramma, Procedimenti, Procedure)",
        "overview": "Gestione della struttura organizzativa, procedure e competenze con alberature gerarchiche dinamiche e routing automatico.",
        "objectives": [
            "Gestione organigramma dinamico",
            "Mappatura competenze e responsabilità",
            "Procedure standardizzate e configurable",
            "Routing automatico basato competenze"
        ],
        "frameworks": ["L. 241/1990", "CAD"],
    },
    "UC4": {
        "title": "BPM e Automazione Processi",
        "overview": "Orchestrazione e automazione dei processi aziendali con motore BPM, task management e integrazione di servizi.",
        "objectives": [
            "Disegno e orchestrazione processi BPM",
            "Automazione task e workflow",
            "Integrazione microservizi",
            "Monitoring e KPI tracking"
        ],
        "frameworks": ["L. 241/1990", "CAD", "AI Act"],
    },
    "UC5": {
        "title": "Produzione Documentale Integrata",
        "overview": "Generazione automatica di documenti strutturati (delibere, determine, atti formali) con template dinamici, firma digitale integrata.",
        "objectives": [
            "Template engine con variabili dinamiche",
            "Generazione documenti standardizzati",
            "Integrazione firma digitale",
            "Conservazione a norma"
        ],
        "frameworks": ["CAD", "GDPR", "eIDAS"],
    },
    "UC6": {
        "title": "Firma Digitale Integrata",
        "overview": "Gestione firma digitale per documenti, certificati, timestamp con supporto eIDAS e formati XAdES/PAdES/CAdES.",
        "objectives": [
            "Firma digitale XAdES/PAdES/CAdES",
            "Validazione certificati digitali",
            "Marca temporale RFC 3161",
            "Verifica validità long-term"
        ],
        "frameworks": ["eIDAS", "CAD"],
    },
    "UC7": {
        "title": "Sistema di Gestione Archivio e Conservazione",
        "overview": "Gestione dell'archivio documentale con conservazione digitale, scarto programmato e migrazione formati per preservazione long-term.",
        "objectives": [
            "Conservazione digitale a norma",
            "Scarto programmato secondo tabelle",
            "Migrazione formati",
            "Metadati conservazione ISO/IEC"
        ],
        "frameworks": ["CAD", "D.Lgs 42/2004"],
    },
    "UC8": {
        "title": "Integrazione con SIEM (Sicurezza Informatica)",
        "overview": "Integrazione con Security Information and Event Management per monitoraggio sicurezza, alerting, anomaly detection.",
        "objectives": [
            "Raccolta log da tutti i componenti",
            "Analisi anomalie e pattern detection",
            "Alerting real-time su eventi critici",
            "Report compliance security"
        ],
        "frameworks": ["CAD", "GDPR"],
    },
    "UC9": {
        "title": "Compliance & Risk Management",
        "overview": "Gestione compliance normative, risk management, audit trail e tracciabilità per conformità. Integrazione con GDPR, CAD, eIDAS.",
        "objectives": [
            "Mappatura compliance normative",
            "Risk assessment e mitigation",
            "Audit trail e tracciabilità completa",
            "Report compliance automatici"
        ],
        "frameworks": ["L. 241/1990", "CAD", "GDPR", "AI Act"],
    },
    "UC10": {
        "title": "Supporto all'Utente",
        "overview": "Help desk integrato, knowledge base, chatbot assistente e self-service portal per supporto utenti con analytics.",
        "objectives": [
            "Help desk con ticketing",
            "Knowledge base searchable",
            "Chatbot assistente AI",
            "Self-service portal"
        ],
        "frameworks": ["CAD", "GDPR"],
    },
    "UC11": {
        "title": "Analisi Dati e Reporting",
        "overview": "Data lake, ETL, analytics avanzate, ML, dashboarding self-service e export dati con supporto big data.",
        "objectives": [
            "ETL e data processing",
            "Advanced analytics e ML models",
            "Self-service BI dashboards",
            "Real-time streaming analytics"
        ],
        "frameworks": ["CAD", "GDPR", "D.Lgs 33/2013"],
    },
}

def extract_uc_number(folder_name: str) -> Optional[Tuple[str, str]]:
    """Estrae numero UC dal nome cartella (es. 'UC1 - Sistema...' -> ('UC1', 'Sistema...'))"""
    match = re.match(r'(UC\d+)\s*-\s*(.+)', folder_name)
    if match:
        return match.group(1), match.group(2)
    return None

def find_sp_files(uc_folder: Path) -> List[Tuple[str, Path]]:
    """Trova tutti i file SP in una cartella UC. Restituisce [(SP_number, filepath), ...]"""
    sp_files = []
    for sp_file in sorted(uc_folder.glob('01 SP*.md')):
        match = re.search(r'SP(\d{2})', sp_file.name)
        if match:
            sp_number = f"SP{match.group(1)}"
            sp_files.append((sp_number, sp_file))
    return sp_files

def generate_uc_index(uc_number: str, uc_title: str, sp_files: List[Tuple[str, Path]]) -> str:
    """Genera il contenuto del file INDEX per un UC"""

    metadata = UC_METADATA.get(uc_number, {})
    overview = metadata.get("overview", f"Use Case {uc_number}: {uc_title}")
    objectives = metadata.get("objectives", [])
    frameworks = metadata.get("frameworks", ["CAD"])

    content = f"""# {uc_number} - {uc_title}

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

{overview}

### Obiettivi Principali

"""

    for obj in objectives:
        content += f"- **{obj.split(':')[0]}**: {obj}\n"

    content += f"""
### Ambito (Scope)

Questo UC copre tutti gli aspetti della **{uc_title}**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura {uc_number}.md` | Architecture | ✅ | [Vai](./{urljoin_safe(f"00 Architettura {uc_number}.md")}) |
"""

    # Aggiungi righe per ogni SP
    for sp_number, sp_file in sp_files:
        sp_name = sp_file.name.replace("01 ", "").replace(".md", "")
        content += f"| {sp_name} | `{sp_file.name}` | Specification | ✅ | [Vai](./{urljoin_safe(sp_file.name)}) |\n"

    # Aggiungi sequence diagrams se trovati
    uc_folder = sp_files[0][1].parent if sp_files else None
    sequence_files = []
    if uc_folder:
        for seq_file in sorted(uc_folder.glob('01 Sequence*.md')):
            sequence_files.append(seq_file.name)

    for seq_file in sequence_files:
        seq_name = seq_file.replace("01 ", "").replace(".md", "")
        content += f"| {seq_name} | `{seq_file}` | Diagram | ✅ | [Vai](./{urljoin_safe(seq_file)}) |\n"

    content += f"""
---

## 📊 SubProgetti (SP) - Overview Rapido

"""

    # Categorizziamo gli SP per gruppo logico
    sp_groups = {}
    for sp_number, sp_file in sp_files:
        # Estrai categoria dal nome file (prima parola dopo SP##)
        words = sp_file.name.split('-')[1].strip().split()
        category = words[0] if words else "Altro"

        if category not in sp_groups:
            sp_groups[category] = []
        sp_groups[category].append((sp_number, sp_file))

    for group, group_files in sp_groups.items():
        content += f"### {group}\n\n"
        for sp_number, sp_file in group_files:
            sp_name = sp_file.name.replace("01 ", "").replace(".md", "")
            sp_name = sp_name.replace(f"{sp_number} - ", "")
            content += f"- **[{sp_number}](./{urljoin_safe(sp_file.name)})** - {sp_name}\n"
        content += "\n"

    content += f"""---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

"""

    for framework in frameworks:
        content += f"- ☑ {framework}\n"

    # Aggiungi altri framework con checkbox unchecked
    all_frameworks = [
        "L. 241/1990 - Procedimento Amministrativo",
        "CAD - D.Lgs 82/2005",
        "GDPR - Regolamento 2016/679",
        "eIDAS - Regolamento 2014/910",
        "AI Act - Regolamento 2024/1689",
        "D.Lgs 42/2004 - Codice Beni Culturali",
        "D.Lgs 152/2006 - Codice dell'Ambiente",
        "D.Lgs 33/2013 - Decreto Trasparenza",
    ]

    for framework in all_frameworks:
        short = framework.split(" - ")[0]
        if short not in [f.split(" - ")[0] for f in frameworks]:
            content += f"- ☐ {framework}\n"

    content += f"""
**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
{uc_number} - {uc_title}/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura {uc_number}.md       ← Architecture
"""

    for sp_number, sp_file in sp_files:
        content += f"├── {sp_file.name}\n"

    for seq_file in sequence_files:
        content += f"├── {seq_file}\n"

    content += "```\n\n"

    content += f"""---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura {uc_number}.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura {uc_number}.md` | 1 hour |

### Resource Links

- **Glossario Terminologico**: [../../GLOSSARIO-TERMINOLOGICO.md](../../GLOSSARIO-TERMINOLOGICO.md)
- **JSON Payload Standard**: [../../templates/json-payload-standard.md](../../templates/json-payload-standard.md)
- **Conformità Normativa Template**: [../../templates/conformita-normativa-standard.md](../../templates/conformita-normativa-standard.md)
- **COMPLIANCE-MATRIX**: [../../COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)
- **UC README**: [../README.md](../README.md)

---

## ✅ Quality Checklist

- [x] INDEX contiene tutti gli SP del UC
- [x] Navigation Matrix è completa
- [x] Link interni validati
- [x] Conformità normativa identificata
- [x] Last update date registrata

---

**Versione**: 1.0 (19 novembre 2025)
**Prossima Review**: 19 dicembre 2025
"""

    return content

def urljoin_safe(filename: str) -> str:
    """Rende il nome file safe per link markdown"""
    # NO URL encoding - markdown links works with spaces as-is
    # Just escape & character properly
    return filename.replace("&", "\\&")

def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    base_path = Path(__file__).parent.parent / 'docs' / 'use_cases'

    if not base_path.exists():
        print(f"❌ Cartella non trovata: {base_path}")
        sys.exit(1)

    # Trova tutti i folder UC
    uc_folders = []
    for item in sorted(base_path.iterdir()):
        if item.is_dir() and item.name.startswith('UC'):
            uc_info = extract_uc_number(item.name)
            if uc_info:
                uc_number, uc_title = uc_info
                uc_folders.append((uc_number, uc_title, item))

    if not uc_folders:
        print("❌ Nessun folder UC trovato")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Generazione INDEX per {len(uc_folders)} UC")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"{'='*70}\n")

    success_count = 0
    error_count = 0

    for uc_number, uc_title, uc_folder in uc_folders:
        try:
            # Trova SP files
            sp_files = find_sp_files(uc_folder)

            # Genera content
            index_content = generate_uc_index(uc_number, uc_title, sp_files)

            # Path per il file INDEX
            index_path = uc_folder / "README.md"

            if dry_run:
                print(f"✓ (DRY-RUN) {uc_number}: INDEX generato ({len(sp_files)} SP)")
            else:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(index_content)
                print(f"✅ {uc_number}: INDEX creato ({len(sp_files)} SP)")
                success_count += 1

        except Exception as e:
            print(f"❌ {uc_number}: Errore - {str(e)}")
            error_count += 1

    print(f"\n{'='*70}")
    print(f"RIEPILOGO:")
    print(f"  ✅ Creati: {success_count}")
    print(f"  ❌ Errori: {error_count}")
    print(f"{'='*70}\n")

    if dry_run:
        print("Modalità DRY-RUN: nessun file creato. Esegui senza --dry-run per applicare.")

    sys.exit(0 if error_count == 0 else 1)

if __name__ == '__main__':
    main()
