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

## ⚡ Quick Start

1. **Firma Digitale**: SP29 firma documenti (XAdES/PAdES/CAdES)
2. **Certificati**: SP30 gestisce certificati digitali
3. **Workflow Firma**: SP31 coordina workflow firme
4. **Timestamp**: SP32 applica marca temporale RFC 3161
5. **Archiviazione**: SP33 archivia documenti firmati

**Documentazione correlata**:
- [SP29 - Digital Signature Engine](./SP29%20-%20Motore%20Firma%20Digitale.md)
- [SP30 - Certificate Manager](./SP30%20-%20Gestore%20Certificati.md)

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC6.md` | Architecture | ✅ | @-ARCHITETTURA.md) |
| SP29 - Digital Signature Engine | `01 SP29 - Motore Firma Digitale.md` | Specification | ✅ | [Vai](./SP29 - Motore Firma Digitale.md) |
| SP30 - Certificate Manager | `01 SP30 - Gestore Certificati.md` | Specification | ✅ | [Vai](./SP30 - Gestore Certificati.md) |
| SP31 - Signature Workflow | `01 SP31 - Workflow Firma.md` | Specification | ✅ | [Vai](./SP31 - Workflow Firma.md) |
| SP32 - Timestamp Authority & Temporal Marking | `01 SP32 - Autorità Timestamp e Marcatura Temporale.md` | Specification | ✅ | [Vai](./SP32 - Autorità Timestamp e Marcatura Temporale.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | C-SEQUENCES.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Digital

- **[SP29](./SP29 - Motore Firma Digitale.md)** - Digital Signature Engine

### Certificate

- **[SP30](./SP30 - Gestore Certificati.md)** - Certificate Manager

### Signature

- **[SP31](./SP31 - Workflow Firma.md)** - Signature Workflow

### Timestamp

- **[SP32](./SP32 - Autorità Timestamp e Marcatura Temporale.md)** - Timestamp Authority & Temporal Marking

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

### Dettagli Conformità PNRR

#### Missione 1: Digitalizzazione, Innovazione, Competitività

| Componente | Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-----------|-------------------|--------------------|-------|
| M1C1.4 | Sicurezza informatica della PA | MS13-SECURITY, MS08-MONITOR | SP11-Security & Audit | Crittografia end-to-end, audit trail immutabile |

#### Obiettivi PNRR per UC6

- **Cybersecurity PA**: 100% conformità con crittografia + audit trail
- **Firma digitale qualificata**: XAdES/PAdES/CAdES con certificati qualificati
- **Audit trail immutabile**: Registrazione completa di tutte le operazioni di firma

### Dettagli Conformità Piano Triennale AgID 2024-2026

#### Capitolo 4: Piattaforme

| Piattaforma | Requisito | Implementazione MS | Implementazione SP | Note |
|-------------|-----------|-------------------|--------------------|-------|
| SPID | Identità digitale | MS13-SECURITY, MS11-GATEWAY | SP11-Security & Audit | Integrazione SAML 2.0 per autenticazione utenti |
| CIE | Carta identità elettronica | MS13-SECURITY | SP11-Security & Audit | Autenticazione CIE per firma digitale |

#### Capitolo 7: Sicurezza Informatica

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-------------------|--------------------|-------|
| Crittografia dati | MS13-SECURITY | SP11-Security & Audit | AES-256 at rest, TLS 1.3 in transit |
| Protezione certificati digitali | MS13-SECURITY | SP32-Timestamp Authority | HSM (Hardware Security Module) per key management |

### Dettagli Conformità CAD - D.Lgs 82/2005

#### Titolo II: Documenti e Firme Digitali

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 22 | Firma digitale qualificata | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | Certificati qualificati, controllo integrità |
| Art. 23 | Marcatura temporale | MS13-SECURITY | SP32-Timestamp Authority | RFC 3161 TSA per non-repudio temporale |
| Art. 24 | Non-ripudio | MS14-AUDIT | SP11-Security & Audit | Registrazione immutabile di firma e timestamp |

### Dettagli Conformità eIDAS - Regolamento 2014/910

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 3 | Firma elettronica avanzata | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | XAdES, PAdES, CAdES compliance |
| Art. 13 | Firma qualificata | MS13-SECURITY | SP32-Timestamp Authority | Certificati qualificati + timestamp |
| Art. 24 | Servizi marca temporale | MS13-SECURITY | SP32-Timestamp Authority | TSA RFC 3161 con RFC 5652 |
| Art. 32 | Validazione long-term | MS04-VALIDATOR | SP32-Timestamp Authority | LTV (Long-Term Validation) per archivio |

### Cross-References Compliance

- **Master Matrix**: [COMPLIANCE-MATRIX.md v2.1](../../COMPLIANCE-MATRIX.md) - Mapping completo AI Act, CAD, PNRR, Piano Triennale
- **PNRR Strategy**: [COMPLIANCE-UPDATE-STRATEGY.md](../../COMPLIANCE-UPDATE-STRATEGY.md) - Roadmap implementazione UC/MS

### ✅ Compliance Checklist UC6

**Prima di Deployment**:
- [ ] Firma digitale XAdES/PAdES/CAdES implementate con certificati qualificati
- [ ] Marcatura temporale RFC 3161 integrata da TSA certificata
- [ ] Crittografia end-to-end (TLS 1.3, AES-256) abilitata
- [ ] Audit trail immutabile per tutte le operazioni di firma
- [ ] SPID + CIE authentication integrata per utenti PA
- [ ] HSM (Hardware Security Module) per protezione chiavi private
- [ ] LTV (Long-Term Validation) supportato per archivio digitale
- [ ] Validazione di certificati e marca temporale implementata

**Annual Compliance Review**:
- [ ] Validità certificati qualificati verificata
- [ ] Algoritmi crittografici allineati con NIST guidelines
- [ ] Audit trail completezza verificata
- [ ] Disaster recovery testato (RTO/RPO met)
- [ ] Security audit eseguito
- [ ] Certificazione eIDAS aggiornata

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC6 - Firma Digitale Integrata/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC6.md       ← Architecture
├── 01 SP29 - Motore Firma Digitale.md
├── 01 SP30 - Gestore Certificati.md
├── 01 SP31 - Workflow Firma.md
├── 01 SP32 - Autorità Timestamp e Marcatura Temporale.md
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

**Versione**: 1.1 (21 novembre 2025 - PNRR & Piano Triennale compliance added)
**Prossima Review**: 21 dicembre 2025
