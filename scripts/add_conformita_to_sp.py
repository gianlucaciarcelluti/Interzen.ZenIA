#!/usr/bin/env python3
"""
Script per aggiungere sezione "Conformità Normativa" standardizzata a tutti gli SP.

Funzionamento:
1. Trova tutti i file SP (01 SP*.md) nella cartella docs/use_cases
2. Estrae il template di base da conformita-normativa-standard.md
3. Per ogni SP:
   - Identifica l'UC di appartenenza
   - Determina i framework normativi applicabili (basato su tipo SP)
   - Aggiunge una sezione "Conformità Normativa" prima di "Roadmap Evoluzione"
   - Mantiene il contesto specifico dello SP

Uso:
    python3 add_conformita_to_sp.py [--dry-run] [--verbose]

Opzioni:
    --dry-run       Mostra cosa farebbe senza modificare file
    --verbose       Output dettagliato per debugging
"""

import os
import re
import sys
from pathlib import Path
from typing import Tuple, List, Optional
import json

# Mapping SP → Framework normativi applicabili
SP_FRAMEWORK_MAPPING = {
    # UC1 - Sistema di Gestione Documentale
    "SP02": ["L. 241/1990", "CAD", "GDPR"],
    "SP07": ["CAD", "AI Act", "GDPR"],
    "SP12": ["CAD", "GDPR"],
    "SP13": ["CAD", "AI Act"],
    "SP14": ["CAD", "GDPR"],
    "SP15": ["CAD", "GDPR"],

    # UC2 - Protocollo Informatico
    "SP03": ["L. 241/1990", "CAD", "GDPR"],
    "SP17": ["L. 241/1990", "CAD", "GDPR"],
    "SP18": ["CAD", "GDPR"],
    "SP19": ["CAD", "GDPR"],
    "SP21": ["L. 241/1990", "CAD"],

    # UC3 - Governance
    "SP20": ["L. 241/1990", "CAD", "GDPR"],
    "SP22": ["L. 241/1990", "CAD"],

    # UC4 - BPM e Automazione
    "SP04": ["L. 241/1990", "CAD", "AI Act"],
    "SP08": ["CAD", "AI Act"],
    "SP09": ["L. 241/1990", "CAD"],
    "SP10": ["CAD", "GDPR"],
    "SP11": ["CAD", "GDPR"],

    # UC5 - Produzione Documentale
    "SP05": ["CAD", "GDPR"],
    "SP06": ["CAD", "eIDAS"],
    "SP16": ["CAD", "AI Act", "GDPR"],
    "SP23": ["CAD", "GDPR"],
    "SP24": ["CAD", "GDPR"],
    "SP25": ["CAD", "GDPR"],
    "SP26": ["CAD", "GDPR"],
    "SP27": ["CAD", "GDPR"],

    # UC6 - Firma Digitale
    "SP29": ["eIDAS", "CAD"],
    "SP30": ["eIDAS", "CAD"],
    "SP31": ["eIDAS", "CAD"],

    # UC7 - Archivio e Conservazione
    "SP32": ["CAD", "D.Lgs 42/2004", "GDPR"],
    "SP33": ["CAD", "D.Lgs 42/2004"],
    "SP34": ["CAD", "D.Lgs 42/2004", "D.Lgs 152/2006"],
    "SP35": ["CAD", "D.Lgs 42/2004"],

    # UC8 - SIEM
    "SP36": ["CAD", "GDPR"],
    "SP37": ["CAD", "GDPR"],
    "SP38": ["CAD"],
    "SP39": ["CAD", "GDPR"],

    # UC9 - Compliance
    "SP40": ["L. 241/1990", "CAD", "GDPR", "AI Act"],
    "SP41": ["CAD", "GDPR"],
    "SP42": ["CAD", "GDPR"],
    "SP43": ["CAD", "GDPR"],
    "SP44": ["L. 241/1990", "CAD", "GDPR"],
    "SP45": ["CAD"],
    "SP46": ["CAD", "D.Lgs 33/2013"],
    "SP47": ["CAD", "D.Lgs 33/2013", "GDPR"],
    "SP48": ["CAD", "D.Lgs 33/2013"],
    "SP49": ["CAD", "GDPR"],
    "SP50": ["CAD", "D.Lgs 152/2006"],

    # UC10 - Supporto Utente
    "SP51": ["CAD", "GDPR"],
    "SP52": ["CAD"],
    "SP53": ["CAD"],
    "SP54": ["CAD", "GDPR"],

    # UC11 - Analisi Dati
    "SP55": ["CAD", "D.Lgs 33/2013", "GDPR"],
    "SP56": ["CAD", "D.Lgs 33/2013", "GDPR"],
    "SP57": ["CAD", "GDPR"],
    "SP58": ["CAD", "GDPR"],
    "SP59": ["CAD", "GDPR"],
    "SP60": ["CAD", "GDPR"],
    "SP61": ["CAD", "GDPR"],
    "SP62": ["CAD", "GDPR"],
    "SP63": ["CAD", "GDPR"],
    "SP64": ["CAD"],
    "SP65": ["CAD", "GDPR"],
    "SP66": ["CAD"],
    "SP67": ["CAD", "GDPR"],
    "SP68": ["CAD", "GDPR"],
    "SP69": ["CAD", "GDPR"],
    "SP70": ["CAD", "GDPR"],
    "SP71": ["CAD"],
    "SP72": ["CAD"],
}

# Framework → Articoli principali da includere di default
FRAMEWORK_ARTICLES = {
    "L. 241/1990": ["Art. 1", "Art. 3", "Art. 6", "Art. 27"],
    "CAD": ["Art. 1", "Art. 21", "Art. 22", "Art. 62"],
    "GDPR": ["Art. 5", "Art. 32"],
    "eIDAS": ["Art. 3", "Art. 13"],
    "AI Act": ["Art. 6", "Art. 13", "Art. 22"],
    "D.Lgs 42/2004": ["Art. 1"],
    "D.Lgs 152/2006": ["Art. 3"],
    "D.Lgs 33/2013": ["Art. 1", "Art. 5"],
}

def extract_sp_number(filename: str) -> Optional[str]:
    """Estrae il numero SP dal nome del file (es. '01 SP02 - ... ' -> 'SP02')"""
    match = re.search(r'SP(\d{2})', filename)
    if match:
        return f"SP{match.group(1)}"
    return None

def get_applicable_frameworks(sp_number: str) -> List[str]:
    """Restituisce i framework normativi applicabili per un SP"""
    return SP_FRAMEWORK_MAPPING.get(sp_number, ["CAD"])

def generate_conformita_section(sp_number: str, frameworks: List[str]) -> str:
    """Genera la sezione Conformità Normativa per uno specifico SP"""

    section = """## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

"""

    # Aggiungi checkbox per i framework applicabili
    for framework in frameworks:
        section += f"☑ {framework}\n"

    # Aggiungi checkbox per framework non applicabili (per completezza)
    all_frameworks = [
        "L. 241/1990 - Procedimento Amministrativo",
        "CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale)",
        "GDPR - Regolamento 2016/679",
        "eIDAS - Regolamento 2014/910",
        "AI Act - Regolamento 2024/1689",
        "D.Lgs 42/2004 - Codice Beni Culturali",
        "D.Lgs 152/2006 - Codice dell'Ambiente",
        "D.Lgs 33/2013 - Decreto Trasparenza",
    ]

    selected_short = set(frameworks)
    for framework in all_frameworks:
        short = framework.split(" - ")[0]
        if short not in selected_short:
            section += f"☐ {framework}\n"

    section += f"""
**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
"""

    # Aggiungi righe per ogni framework
    for framework in frameworks:
        articles = FRAMEWORK_ARTICLES.get(framework, [])
        articles_str = ", ".join(articles) if articles else "Vedi template"
        status = "✅ Implementato"  # Default
        section += f"| {framework} | {articles_str} | {status} | [Dettagli](./templates/conformita-normativa-standard.md) |\n"

    section += """
### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa" del template standard.

---

"""

    return section

def find_insertion_point(content: str) -> int:
    """
    Trova il punto di inserimento per la sezione Conformità Normativa.
    Deve essere PRIMA della sezione "### Roadmap Evoluzione" o "## Roadmap Evoluzione"
    """
    # Cerca "Roadmap Evoluzione"
    roadmap_pattern = r'\n(?:###|##)\s+Roadmap\s+Evoluzione'
    match = re.search(roadmap_pattern, content)

    if match:
        return match.start()

    # Se non trovata, inserisci prima della fine del file (ma dopo l'ultimo ###)
    last_section = content.rfind('\n## ')
    if last_section != -1:
        return last_section

    return len(content) - 1

def check_conformita_exists(content: str) -> bool:
    """Verifica se la sezione Conformità Normativa esiste già"""
    return "## 🏛️ Conformità Normativa" in content or "## 🏛️ CONFORMITÀ NORMATIVA" in content

def add_conformita_to_file(filepath: Path, dry_run: bool = False, verbose: bool = False) -> Tuple[bool, str]:
    """
    Aggiunge la sezione Conformità Normativa a un file SP.
    Restituisce (success, message)
    """

    try:
        # Leggi il file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Estrai numero SP
        sp_number = extract_sp_number(filepath.name)
        if not sp_number:
            return False, f"❌ Impossibile estrarre numero SP da {filepath.name}"

        # Verifica se conformità esiste già
        if check_conformita_exists(content):
            return True, f"⏭️  {sp_number}: Conformità già presente, skipped"

        # Ottieni frameworks applicabili
        frameworks = get_applicable_frameworks(sp_number)

        # Genera sezione Conformità
        conformita_section = generate_conformita_section(sp_number, frameworks)

        # Trova punto di inserimento
        insert_pos = find_insertion_point(content)

        # Inserisci sezione
        new_content = content[:insert_pos] + conformita_section + content[insert_pos:]

        if dry_run:
            return True, f"✓ (DRY-RUN) {sp_number}: Conformità aggiunta ({len(frameworks)} framework)"
        else:
            # Scrivi il file aggiornato
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"✅ {sp_number}: Conformità aggiunta ({', '.join(frameworks[:2])}...)"

    except Exception as e:
        return False, f"❌ {filepath.name}: Errore - {str(e)}"

def main():
    # Parse argumenti
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    # Trova cartella docs/use_cases
    base_path = Path(__file__).parent.parent / 'docs' / 'use_cases'

    if not base_path.exists():
        print(f"❌ Cartella non trovata: {base_path}")
        sys.exit(1)

    # Trova tutti i file SP
    sp_files = []
    for uc_folder in sorted(base_path.glob('UC*')):
        if uc_folder.is_dir():
            for sp_file in sorted(uc_folder.glob('01 SP*.md')):
                sp_files.append(sp_file)

    if not sp_files:
        print("❌ Nessun file SP trovato")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Aggiunta Conformità Normativa a {len(sp_files)} SP")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"{'='*70}\n")

    # Processa ogni file
    success_count = 0
    skip_count = 0
    error_count = 0

    for i, sp_file in enumerate(sp_files, 1):
        success, message = add_conformita_to_file(sp_file, dry_run=dry_run, verbose=verbose)

        status = "✅" if success else "❌"
        print(f"[{i:2}/{len(sp_files)}] {message}")

        if success:
            if "già presente" in message or "DRY-RUN" in message:
                skip_count += 1
            else:
                success_count += 1
        else:
            error_count += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"RIEPILOGO:")
    print(f"  ✅ Aggiunti: {success_count}")
    print(f"  ⏭️  Saltati: {skip_count}")
    print(f"  ❌ Errori: {error_count}")
    print(f"{'='*70}\n")

    if dry_run:
        print("Modalità DRY-RUN: nessun file modificato. Esegui senza --dry-run per applicare.")

    sys.exit(0 if error_count == 0 else 1)

if __name__ == '__main__':
    main()
