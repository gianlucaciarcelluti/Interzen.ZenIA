# UC3 - Governance (Organigramma, Procedimenti, Procedure)

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Gestione della struttura organizzativa, procedure e competenze con alberature gerarchiche dinamiche e routing automatico.

### Obiettivi Principali

- **Gestione organigramma dinamico**: Gestione organigramma dinamico
- **Mappatura competenze e responsabilità**: Mappatura competenze e responsabilità
- **Procedure standardizzate e configurable**: Procedure standardizzate e configurable
- **Routing automatico basato competenze**: Routing automatico basato competenze

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Governance (Organigramma, Procedimenti, Procedure)**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC3.md` | Architecture | ✅ | [Vai](./00 Architettura UC3.md) |
| SP20 - Organization Chart Manager | `01 SP20 - Gestione Organigramma.md` | Specification | ✅ | [Vai](./01 SP20 - Gestione Organigramma.md) |
| SP21 - Procedure Manager | `01 SP21 - Gestore Procedure.md` | Specification | ✅ | [Vai](./01 SP21 - Gestore Procedure.md) |
| SP22 - Process Governance | `01 SP22 - Governance Processi.md` | Specification | ✅ | [Vai](./01 SP22 - Governance Processi.md) |
| SP23 - Compliance Monitor | `01 SP23 - Monitor Conformità.md` | Specification | ✅ | [Vai](./01 SP23 - Monitor Conformità.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Organization

- **[SP20](./01 SP20 - Gestione Organigramma.md)** - Organization Chart Manager

### Procedure

- **[SP21](./01 SP21 - Gestore Procedure.md)** - Procedure Manager

### Process

- **[SP22](./01 SP22 - Governance Processi.md)** - Process Governance

### Compliance

- **[SP23](./01 SP23 - Monitor Conformità.md)** - Compliance Monitor

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ L. 241/1990
- ☑ CAD
- ☐ GDPR - Regolamento 2016/679
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC3 - Governance (Organigramma, Procedimenti, Procedure)/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC3.md       ← Architecture
├── 01 SP20 - Gestione Organigramma.md
├── 01 SP21 - Gestore Procedure.md
├── 01 SP22 - Governance Processi.md
├── 01 SP23 - Monitor Conformità.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC3.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC3.md` | 1 hour |

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
