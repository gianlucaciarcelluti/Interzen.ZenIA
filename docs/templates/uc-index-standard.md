# Template Standard - UC INDEX

**Versione**: 1.0
**Data**: 2025-11-19
**Scopo**: Template standardizzato per il file INDEX centralizzato di ogni Use Case (UC)

---

## 📋 ISTRUZIONI PER L'USO

Ogni UC DEVE avere un file `00 INDEX.md` nella propria cartella come **punto di ingresso centralizzato**.

### Struttura del file:
1. **Header**: Titolo UC e overview
2. **Navigation Matrix**: Mappa di accesso rapido ai componenti
3. **SP Overview**: Elenco con breve descrizione di ogni SP
4. **Architecture Diagrams**: Link ai diagrammi e architetture
5. **Key Flows**: Descrizione dei flussi principali
6. **Cross-UC Dependencies**: UC correlati e dipendenze
7. **Related Resources**: Link a documentazione correlata

---

## 🔄 TEMPLATE UC INDEX

```markdown
# [UC#] - [Titolo Completo UC]

**Status**: [Active / In Development / Planned]
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: [Team/Persona responsabile]

---

## 📌 Overview

[Paragrafo breve (2-3 righe) che spiega lo scopo del UC in modo conciso]

### Obiettivi Principali

- **Obiettivo 1**: [Descrizione]
- **Obiettivo 2**: [Descrizione]
- **Obiettivo 3**: [Descrizione]

### Ambito (Scope)

[Elenco delle aree coperte da questo UC, cosa è INCLUSO]

**Escluso**: [Cosa NON è coperto da questo UC]

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura [UC#].md` | Architecture | ✅ | [Link] |
| [Componente 1] | `01 SP## - [Nome].md` | Specification | ✅ | [Link] |
| [Componente 2] | `01 SP## - [Nome].md` | Specification | ✅ | [Link] |
| [Componente 3] | `01 SP## - [Nome].md` | Specification | ✅ | [Link] |
| Sequence - Overview | `01 Sequence - Overview Semplificato.md` | Diagram | ✅ | [Link] |
| Sequence - Dettagliato | `01 Sequence - Generazione Atto Completo.md` | Diagram | ✅ | [Link] |

---

## 📊 SubProgetti (SP) - Overview Rapido

### [Categoria SP 1]

#### [SP##] - [Nome]
- **Responsabilità**: [Una riga]
- **Tecnologie**: [Tech stack principale]
- **Input/Output**: [Brevissimo]
- **Conformità**: [Framework normativi applicabili]
- **Documentazione**: [Link a SPECIFICATION.md]

#### [SP##] - [Nome]
- **Responsabilità**: [Una riga]
- **Tecnologie**: [Tech stack principale]
- **Input/Output**: [Brevissimo]
- **Conformità**: [Framework normativi applicabili]
- **Documentazione**: [Link a SPECIFICATION.md]

### [Categoria SP 2]

#### [SP##] - [Nome]
- **Responsabilità**: [Una riga]
- **Tecnologie**: [Tech stack principale]
- **Input/Output**: [Brevissimo]
- **Conformità**: [Framework normativi applicabili]
- **Documentazione**: [Link a SPECIFICATION.md]

---

## 🏗️ Architecture & Diagrams

### Diagrammi Disponibili

| Tipo | Nome | Descrizione | File |
|------|------|-------------|------|
| Architecture | [UC#] - System Architecture | Overview architettura generale | `00 Architettura [UC#].md` |
| Flow | Core Process Flow | Flusso processo principale | Sequence Diagram |
| State | State Transitions | Transizioni di stato | Sequence Diagram |
| Data | Data Model | Modello dati | `00 Architettura [UC#].md` |

### Schema Architettura Generale

```mermaid
[Inserire diagramma mermaid rappresentativo]
```

---

## 🔄 Key Workflows

### Workflow 1: [Nome Workflow Principale]

**Trigger**: [Cosa lo attiva]
**Attori**: [Chi è coinvolto]
**Fasi**:
1. [Fase 1]
2. [Fase 2]
3. [Fase 3]
**Outcome**: [Risultato]
**Tempo Medio**: [X minuti/ore]

**Documentazione Dettagliata**: [Link a Sequence Diagram]

### Workflow 2: [Nome Workflow Secondario]

**Trigger**: [Cosa lo attiva]
**Attori**: [Chi è coinvolto]
**Fasi**:
1. [Fase 1]
2. [Fase 2]
**Outcome**: [Risultato]

---

## 🔗 Dipendenze Inter-UC

### UC che dipendono da questo UC

| UC | Dipendenza | Tipo | Note |
|----|-----------|------|------|
| [UC#] | [Descrizione dipendenza] | Soft / Hard | [Dettagli] |
| [UC#] | [Descrizione dipendenza] | Soft / Hard | [Dettagli] |

### UC da cui dipende questo UC

| UC | Dipendenza | Tipo | Note |
|----|-----------|------|------|
| [UC#] | [Descrizione dipendenza] | Soft / Hard | [Dettagli] |
| [UC#] | [Descrizione dipendenza] | Soft / Hard | [Dettagli] |

### Integrazione con Microservizi (MS)

| MS | Ruolo | Interazione | Note |
|----|-------|-------------|------|
| MS## | [Ruolo] | [Tipo interazione] | [Dettagli] |
| MS## | [Ruolo] | [Tipo interazione] | [Dettagli] |

**Mappa MS completa**: [Vedi docs/microservices/MS-ARCHITECTURE-MASTER.md]

---

## 📋 Conformità Normativa

### Framework Normativi Applicabili

- ☑ L. 241/1990 - Procedimento Amministrativo
- ☑ CAD - D.Lgs 82/2005
- ☑ GDPR - Regolamento 2016/679
- ☑ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP

---

## 🎓 Learning Path

### Per Principianti

1. Leggere questo **INDEX** (2 minuti)
2. Leggere **Architettura Generale UC** (5 minuti)
3. Guardare diagrammi **Sequence - Overview Semplificato** (3 minuti)
4. Leggere **1-2 SP principali** (10 minuti)

**Tempo totale**: ~20 minuti per comprensione base

### Per Sviluppatori

1. Studio approfondito **Architettura UC** (30 minuti)
2. Analisi **Sequence Diagram dettagliato** (20 minuti)
3. Lettura completa **SPECIFICATION.md di SP rilevanti** (1-2 ore)
4. Studio **JSON payload examples** (30 minuti)
5. Review **Conformità Normativa** (15 minuti)

**Tempo totale**: ~2.5-3 ore per padronanza tecnica

### Per Compliance Officer

1. Review **Conformità Normativa** in questo INDEX (10 minuti)
2. Verifica **🏛️ Conformità Normativa** in ogni SP (30 minuti)
3. Controllo **COMPLIANCE-MATRIX.md** (20 minuti)

**Tempo totale**: ~1 ora

---

## 📂 Struttura File UC

```
UC[#] - [Titolo]/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura [UC#].md             ← Architecture
├── 01 SP##  - [Nome 1].md
├── 01 SP##  - [Nome 2].md
├── 01 SP##  - [Nome 3].md
├── 01 Sequence - Overview Semplificato.md
├── 01 Sequence - Generazione Atto Completo.md
└── 01 Sequence - Ultra Semplificato.md
```

---

## 🔍 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura [UC#].md` | 15 min |
| Developer | `01 Sequence - Generazione Atto Completo.md` | 30 min |
| Tester | `00 INDEX.md` → SP Rilevanti | 45 min |
| Compliance | `00 INDEX.md` → Conformità Normativa | 30 min |
| Architect | `00 Architettura [UC#].md` + MS References | 1 hour |

### Resource Links

- **GLOSSARIO-TERMINOLOGICO**: [../../GLOSSARIO-TERMINOLOGICO.md](../../GLOSSARIO-TERMINOLOGICO.md)
- **JSON Payload Standard**: [../../templates/json-payload-standard.md](../../templates/json-payload-standard.md)
- **Conformità Normativa Standard**: [../../templates/conformita-normativa-standard.md](../../templates/conformita-normativa-standard.md)
- **COMPLIANCE-MATRIX**: [../../COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)
- **MS Architecture Master**: [../../microservices/MS-ARCHITECTURE-MASTER.md](../../microservices/MS-ARCHITECTURE-MASTER.md)
- **Use Cases README**: [../README.md](../README.md)

---

## ✅ Quality Checklist

- [ ] INDEX contiene tutti gli SP del UC
- [ ] Navigation Matrix è completa e aggiornata
- [ ] Architettura diagrams presenti e link funzionanti
- [ ] Sequence diagrams collegati
- [ ] Dependencies con altri UC documentate
- [ ] Conformità normativa identificata
- [ ] Ultimo update date registrata
- [ ] All'interno di 2000 righe (readability)
- [ ] Link interni validati
- [ ] Referenze cross-UC coerenti

---

## 📞 Support & Questions

Per domande su questo UC:

- **Technical**: [Contact Architecture Team]
- **Compliance**: [Contact Compliance Team]
- **Product**: [Contact Product Owner]

---

**Approvato da**: Architecture Team
**Versione**: 1.0 (19 novembre 2025)
**Prossima Review**: 19 dicembre 2025

```

---

## 📝 NOTE IMPLEMENTATIVE

### Come usare questo template per creare UC INDEX:

1. **Copia il contenuto** di questo template
2. **Personalizza** con dati dello specifico UC:
   - Numero UC e titolo
   - Overview e obiettivi
   - Elenco SP specifici
   - Diagrammi Mermaid appropriati
   - Workflow specifici del UC
3. **Completa Navigation Matrix** con file effettivi
4. **Aggiungi diagrammi Mermaid** specifici UC
5. **Valida link interni** con verify_links.py
6. **Review** con team di architettura

### Tempo di creazione per UC:

- Raccolta dati: 30 minuti
- Compilazione template: 45 minuti
- Aggiunta diagrammi: 30 minuti
- Review & validazione: 15 minuti
- **Total**: ~2 ore per UC completo

### Manutenzione:

- **Review settimanale**: Verificare SP aggiornamenti
- **Review mensile**: Aggiornare se cambiano dipendenze
- **Review annuale**: Completa re-validazione contenuti

---

**Template Version**: 1.0
**Creato**: 2025-11-19
**Compatibility**: Markdown + Mermaid
