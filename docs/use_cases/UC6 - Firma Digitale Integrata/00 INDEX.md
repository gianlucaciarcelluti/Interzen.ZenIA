# UC6 - Firma Digitale Integrata

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Gestione firma digitale per documenti, certificati, timestamp con supporto eIDAS e formati XAdES/PAdES/CAdES.

### Obiettivi Principali

- **Firma digitale XAdES/PAdES/CAdES**: Firma digitale XAdES/PAdES/CAdES
- **Validazione certificati digitali**: Validazione certificati digitali
- **Marca temporale RFC 3161**: Marca temporale RFC 3161
- **Verifica validità long-term**: Verifica validità long-term

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Firma Digitale Integrata**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC6.md` | Architecture | ✅ | [Vai](./00 Architettura UC6.md) |
| SP29 - Digital Signature Engine | `01 SP29 - Digital Signature Engine.md` | Specification | ✅ | [Vai](./01 SP29 - Digital Signature Engine.md) |
| SP30 - Certificate Manager | `01 SP30 - Certificate Manager.md` | Specification | ✅ | [Vai](./01 SP30 - Certificate Manager.md) |
| SP31 - Signature Workflow | `01 SP31 - Signature Workflow.md` | Specification | ✅ | [Vai](./01 SP31 - Signature Workflow.md) |
| SP32 - Timestamp Authority & Temporal Marking | `01 SP32 - Timestamp Authority & Temporal Marking.md` | Specification | ✅ | [Vai](./01 SP32 - Timestamp Authority & Temporal Marking.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Digital

- **[SP29](./01 SP29 - Digital Signature Engine.md)** - Digital Signature Engine

### Certificate

- **[SP30](./01 SP30 - Certificate Manager.md)** - Certificate Manager

### Signature

- **[SP31](./01 SP31 - Signature Workflow.md)** - Signature Workflow

### Timestamp

- **[SP32](./01 SP32 - Timestamp Authority & Temporal Marking.md)** - Timestamp Authority & Temporal Marking

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ eIDAS
- ☑ CAD
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ GDPR - Regolamento 2016/679
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC6 - Firma Digitale Integrata/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC6.md       ← Architecture
├── 01 SP29 - Digital Signature Engine.md
├── 01 SP30 - Certificate Manager.md
├── 01 SP31 - Signature Workflow.md
├── 01 SP32 - Timestamp Authority & Temporal Marking.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC6.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC6.md` | 1 hour |

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
