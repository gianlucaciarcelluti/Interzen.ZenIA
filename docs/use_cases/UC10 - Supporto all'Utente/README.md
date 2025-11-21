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

## ⚡ Quick Start

1. **Help Desk**: Gestione ticket con routing automatico
2. **Knowledge Base**: Ricerca articles e risoluzioni comuni
3. **Chatbot**: Assistente AI per domande frequenti
4. **Self-Service**: Utenti risolvono problemi autonomamente
5. **Analytics**: Dashboard con metriche di supporto e SLA

**Documentazione correlata**:
- Help Desk Manager e Knowledge Base components

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC10.md` | Architecture | ✅ | @-ARCHITETTURA.md) |
| SP51 - Help Desk System | `01 SP51 - Sistema Help Desk.md` | Specification | ✅ | [Vai](./SP51 - Sistema Help Desk.md) |
| SP52 - Knowledge Base Management | `01 SP52 - Gestione Base Conoscenze.md` | Specification | ✅ | [Vai](./SP52 - Gestione Base Conoscenze.md) |
| SP53 - Virtual Assistant & Chatbot | `01 SP53 - Assistente Virtuale e Chatbot.md` | Specification | ✅ | [Vai](./SP53 - Assistente Virtuale e Chatbot.md) |
| SP54 - User Training Platform | `01 SP54 - Piattaforma Formazione Utenti.md` | Specification | ✅ | [Vai](./SP54 - Piattaforma Formazione Utenti.md) |
| SP55 - Self-Service Portal | `01 SP55 - Portale Self-Service.md` | Specification | ✅ | [Vai](./SP55 - Portale Self-Service.md) |
| SP56 - Support Analytics & Reporting | `01 SP56 - Analitiche Supporto e Reporting.md` | Specification | ✅ | [Vai](./SP56 - Analitiche Supporto e Reporting.md) |
| SP57 - User Feedback Management | `01 SP57 - Gestione Feedback Utenti.md` | Specification | ✅ | [Vai](./SP57 - Gestione Feedback Utenti.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Help

- **[SP51](./SP51 - Sistema Help Desk.md)** - Help Desk System

### Knowledge

- **[SP52](./SP52 - Gestione Base Conoscenze.md)** - Knowledge Base Management

### Virtual

- **[SP53](./SP53 - Assistente Virtuale e Chatbot.md)** - Virtual Assistant & Chatbot

### User

- **[SP54](./SP54 - Piattaforma Formazione Utenti.md)** - User Training Platform
- **[SP57](./SP57 - Gestione Feedback Utenti.md)** - User Feedback Management

### Self

- **[SP55](./SP55 - Portale Self-Service.md)** - Self-Service Portal

### Support

- **[SP56](./SP56 - Analitiche Supporto e Reporting.md)** - Support Analytics & Reporting

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
├── 01 SP51 - Sistema Help Desk.md
├── 01 SP52 - Gestione Base Conoscenze.md
├── 01 SP53 - Assistente Virtuale e Chatbot.md
├── 01 SP54 - Piattaforma Formazione Utenti.md
├── 01 SP55 - Portale Self-Service.md
├── 01 SP56 - Analitiche Supporto e Reporting.md
├── 01 SP57 - Gestione Feedback Utenti.md
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
