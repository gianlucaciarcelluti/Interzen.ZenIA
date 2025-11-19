# UC10 - Supporto all'Utente

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Help desk integrato, knowledge base, chatbot assistente e self-service portal per supporto utenti con analytics.

### Obiettivi Principali

- **Help desk con ticketing**: Help desk con ticketing
- **Knowledge base searchable**: Knowledge base searchable
- **Chatbot assistente AI**: Chatbot assistente AI
- **Self-service portal**: Self-service portal

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Supporto all'Utente**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC10.md` | Architecture | ✅ | [Vai](./00 Architettura UC10.md) |
| SP51 - Help Desk System | `01 SP51 - Help Desk System.md` | Specification | ✅ | [Vai](./01 SP51 - Help Desk System.md) |
| SP52 - Knowledge Base Management | `01 SP52 - Knowledge Base Management.md` | Specification | ✅ | [Vai](./01 SP52 - Knowledge Base Management.md) |
| SP53 - Virtual Assistant & Chatbot | `01 SP53 - Virtual Assistant & Chatbot.md` | Specification | ✅ | [Vai](./01 SP53 - Virtual Assistant \& Chatbot.md) |
| SP54 - User Training Platform | `01 SP54 - User Training Platform.md` | Specification | ✅ | [Vai](./01 SP54 - User Training Platform.md) |
| SP55 - Self-Service Portal | `01 SP55 - Self-Service Portal.md` | Specification | ✅ | [Vai](./01 SP55 - Self-Service Portal.md) |
| SP56 - Support Analytics & Reporting | `01 SP56 - Support Analytics & Reporting.md` | Specification | ✅ | [Vai](./01 SP56 - Support Analytics \& Reporting.md) |
| SP57 - User Feedback Management | `01 SP57 - User Feedback Management.md` | Specification | ✅ | [Vai](./01 SP57 - User Feedback Management.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Help

- **[SP51](./01 SP51 - Help Desk System.md)** - Help Desk System

### Knowledge

- **[SP52](./01 SP52 - Knowledge Base Management.md)** - Knowledge Base Management

### Virtual

- **[SP53](./01 SP53 - Virtual Assistant \& Chatbot.md)** - Virtual Assistant & Chatbot

### User

- **[SP54](./01 SP54 - User Training Platform.md)** - User Training Platform
- **[SP57](./01 SP57 - User Feedback Management.md)** - User Feedback Management

### Self

- **[SP55](./01 SP55 - Self-Service Portal.md)** - Self-Service Portal

### Support

- **[SP56](./01 SP56 - Support Analytics \& Reporting.md)** - Support Analytics & Reporting

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD
- ☑ GDPR
- ☐ L. 241/1990 - Procedimento Amministrativo
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
UC10 - Supporto all'Utente/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC10.md       ← Architecture
├── 01 SP51 - Help Desk System.md
├── 01 SP52 - Knowledge Base Management.md
├── 01 SP53 - Virtual Assistant & Chatbot.md
├── 01 SP54 - User Training Platform.md
├── 01 SP55 - Self-Service Portal.md
├── 01 SP56 - Support Analytics & Reporting.md
├── 01 SP57 - User Feedback Management.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC10.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC10.md` | 1 hour |

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
