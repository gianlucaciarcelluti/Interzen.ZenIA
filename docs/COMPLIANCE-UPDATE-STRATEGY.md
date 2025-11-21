# Strategia di Aggiornamento Compliance UC/MS

**Data**: 21 Novembre 2025
**Versione**: 1.0
**Ultimo Aggiornamento**: 21 Novembre 2025

---

## 📋 Obiettivo Strategico

Integrare sistematicamente i requisiti PNRR (Missione 1 & 5) e Piano Triennale AgID 2024-2026 nella documentazione di tutti i Use Case (UC) e Microservizi (MS) per raggiungere **100% compliance** entro Q2 2026.

---

## 📊 Stato Attuale Compliance

| Ambito | Copertura | Stato | Gap |
|--------|-----------|-------|-----|
| **UC Files** | 7/11 (64%) | 🟡 Parziale | 4 UC richiedono updates |
| **MS Files** | 5/16 (31%) | 🔴 Critico | 11 MS richiedono updates |
| **COMPLIANCE-MATRIX.md** | 100% | ✅ Completo | Master document aggiornato |
| **COMPLIANCE-MAPPING-PNRR.md** | 100% | ✅ Completo | PNRR mapping completo |
| **COMPLIANCE-MAPPING-PIANO-TRIENNALE.md** | 100% | ✅ Completo | Piano Triennale mapping completo |

---

## 🎯 FASE 1: CRITICAL PATH (Q4 2025 - Q1 2026)

### 7 file critici da aggiornare immediatamente

#### 1. UC6 - Firma Digitale Integrata ⭐ PRIORITÀ 1
**Motivazione**: Firma digitale è requisito fondamentale per PA compliance
**Sforzo**: 8 ore
**Cross-references**: CAD Art. 22-24, eIDAS, PNRR sicurezza

**Sezioni da aggiungere**:
```
### 📋 Conformità PNRR
- M1C1.4: Sicurezza informatica
- Crittografia end-to-end
- Audit trail immutabile

### 📚 Conformità Piano Triennale
- Cap 4: Piattaforme digitali (SPID, CIE, firma avanzata)
- Cap 7: Sicurezza informatica (NIS2, encryption)
- Integrazione CIE (Carta Identità Elettronica)
- Integrazione SPID (Sistema Pubblico Identità Digitale)

### 🏛️ Conformità CAD
- Art. 22: Firma digitale con certificati qualificati
- Art. 23: Marcatura temporale (RFC 3161)
- Art. 24: Non-ripudio e audit trail
```

#### 2. UC7 - Conservazione Digitale ⭐ PRIORITÀ 2
**Motivazione**: Conservazione è requisito normativo per PA
**Sforzo**: 6 ore
**Cross-references**: PNRR disaster recovery, Piano Triennale Cap 3, ISO 14721 OAIS

**Sezioni da aggiungere**:
```
### 📋 Conformità PNRR
- M1C1.3: Cloud consolidation (RTO 4h, RPO 1h)
- M1C1.4: Backup geo-redundante
- Disaster recovery SLA

### 📚 Conformità Piano Triennale
- Cap 3: Gestione documenti informatici (long-term preservation)
- Cap 6: Infrastrutture (backup automatico, disaster recovery)
- Modello OAIS (ISO 14721)
- PDF/A-1b formato archivio

### 🏛️ CAD Conformità
- Art. 41: Conservazione dati (30+ anni)
- Art. 42: Autenticità documento (catena custodia)
- Art. 43: Integrità (hash validation, blockchain optional)
```

#### 3. UC8 - Integrazione SIEM (Sicurezza) ⭐ PRIORITÀ 3
**Motivazione**: Sicurezza è infrastruttura critica (NIS2)
**Sforzo**: 10 ore
**Cross-references**: NIS2 Directive, Piano Triennale Cap 5, PNRR M1C1.4

**Sezioni da aggiungere**:
```
### 📋 Conformità PNRR
- M1C1.4: Sicurezza informatica della PA
- SIEM 24/7 monitoring
- Incident response < 30 minuti

### 📚 Conformità Piano Triennale
- Cap 5: Sicurezza informatica (SIEM requirements)
- Cap 5: NIS2 Directive compliance (entità critiche)
- Zero Trust architecture
- Real-time alerting & SOAR integration

### 🏛️ Conformità NIS2 (Direttiva 2022/2555/EU)
- Identificazione entità critiche
- Incident reporting 72 ore
- Supply chain security
- Security updates & patching
```

#### 4. UC9 - Compliance & Risk Management ⭐ PRIORITÀ 4
**Motivazione**: Fondazione per tutte le attività compliance
**Sforzo**: 12 ore
**Cross-references**: AI Act, PNRR risk framework, Piano Triennale Cap 5

**Sezioni da aggiungere**:
```
### 📋 Conformità PNRR
- M1C1.4: Risk assessment framework
- Evidence collection (PNRR audit trail)
- Compliance dashboard

### 📚 Conformità Piano Triennale
- Cap 5: Governance dell'AI (AI Act integration)
- Cap 5: Risk management framework
- Cap 7: Security monitoring & incident management

### 🏛️ Conformità AI Act + GDPR
- Art. 6 AI Act: Risk Assessment sistemica
- Art. 27-33 AI Act: Annex III risk management
- GDPR Art. 35: Data Protection Impact Assessment (DPIA)
- GDPR Art. 33-34: Breach notification procedures
```

#### 5. MS13-SECURITY ⭐ PRIORITÀ 5
**Motivazione**: Core di tutta autenticazione & autorizzazione
**Sforzo**: 15 ore
**Cross-references**: NIS2, eIDAS, SPID, CIE, PNRR

**Sezioni da aggiungere**:
```
### 🔐 Conformità PNRR
- M1C1.4: Crittografia (AES-256 at rest, TLS 1.3 in transit)
- M1C1.4: Zero Trust architecture
- M1C1.4: MFA (Multi-Factor Authentication) obbligatorio

### 📚 Conformità Piano Triennale
- Cap 7: Crittografia (FIPS 140-2 Level 2 minimum)
- Cap 7: Access control (RBAC + ABAC)
- Cap 4: SPID integration (SAML 2.0)
- Cap 4: CIE integration (eIDAS certificate validation)

### 🏛️ Conformità eIDAS + NIS2
- eIDAS Art. 13: Firma avanzata con certificati qualificati
- eIDAS Art. 24: Marca temporale (TSA RFC 3161)
- NIS2: Encrypted storage + secure key management
- NIS2: Biometric authentication optional
```

#### 6. MS14-AUDIT ⭐ PRIORITÀ 6
**Motivazione**: Non-repudiation & compliance proof
**Sforzo**: 12 ore
**Cross-references**: PNRR evidence collection, AI Act Art. 14, GDPR Art. 33

**Sezioni da aggiungere**:
```
### 📋 Conformità PNRR
- M1C1.4: Audit trail immutabile (blockchain optional)
- Evidence collection per PNRR milestone
- Compliance attestation

### 📚 Conformità AI Act
- Art. 14: Record keeping automatico
- Art. 27: Risk management documentation
- Art. 31: Human oversight log
- Art. 30: Automated decision records

### 🏛️ Conformità GDPR + CAD
- GDPR Art. 5: Legittimità & integrità
- GDPR Art. 33-34: Breach notification procedure
- GDPR Art. 32: Integrity & confidentiality logs
- CAD Art. 24: Diritti accesso (audit trail accessible)
```

---

## 🔄 FASE 2: HIGH PRIORITY (Q1 2026)

### 5 file ad alta priorità

#### UC1 - Sistema Gestione Documentale
**Sforzo**: 6 ore
**Aggiunte**: PNRR M1C1 (PA modernization), Piano Triennale Cap 4 (interoperability), PDND integration

#### UC5 - Produzione Documentale Integrata
**Sforzo**: 8 ore
**Aggiunte**: PNRR M1C2 (Digital transformation), Modello 3+2, PDND data sharing, API Design standards

#### UC11 - Analisi Dati e Reporting
**Sforzo**: 7 ore
**Aggiunte**: PNRR open data (M1C1.2), Piano Triennale disaster recovery SLA (Cap 6), DCAT-AP metadata

#### MS11-GATEWAY
**Sforzo**: 8 ore
**Aggiunte**: Piano Triennale API Portal, SPID/CIE authentication endpoints, OpenAPI 3.0 compliance, rate limiting

#### MS16-REGISTRY
**Sforzo**: 10 ore
**Aggiunte**: PDND integration requirements, AgID service discovery, DCAT-AP catalog registration

---

## 📅 FASE 3: MEDIUM PRIORITY (Q2 2026)

### 8 file a media priorità

| File | Sforzo | Aggiunte Principali |
|------|--------|-------------------|
| UC2 - Protocollo Informatico | 6h | CAD Art. 23, SPID/CIE auth, PNRR M1C1.2 |
| UC3 - Governance | 6h | PNRR M1C1.1, Piano Triennale Cap 5, AgID governance |
| UC4 - BPM e Automazione | 8h | PNRR M1C1.2, NIS2 automation safety, Piano Triennale |
| UC10 - Supporto Utente | 6h | PNRR M5C1.2 (inclusione), WCAG 2.1 AA, CAD Art. 3 |
| MS01-CLASSIFIER | 5h | PNRR bias detection, AI Act Art. 6, data quality |
| MS02-ANALYZER | 7h | PNRR transparency, AI Act Art. 13, GDPR Art. 22 HITL |
| MS03-ORCHESTRATOR | 6h | Piano Triennale workflow standards, PNRR automation |
| MS04-VALIDATOR | 5h | AI Act Art. 12, eIDAS validation, CAD signature |

---

## 📝 TEMPLATE STANDARD PER UPDATES

### Sezione CONFORMITÀ NORMATIVA (da aggiungere a ogni UC/MS README.md)

```markdown
## 📋 Conformità Normativa & Framework Nazionali

### 🇮🇹 Framework Italiano

#### CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale)
| Articolo | Requisito | Implementazione | Status |
|----------|-----------|-----------------|--------|
| Art. X | [Descrizione] | [MS/SP mapping] | ✅ Implementato |

### 🇪🇺 Normative Europee

#### AI Act (Regolamento 2024/1689) - se applicabile
| Articolo | Requisito | Implementazione | Status |
|----------|-----------|-----------------|--------|
| Art. X | [Descrizione] | [MS/SP mapping] | ✅ Implementato |

#### eIDAS (Regolamento 2014/910) - se applicabile
| Articolo | Requisito | Implementazione | Status |
|----------|-----------|-----------------|--------|
| Art. X | [Descrizione] | [MS/SP mapping] | ✅ Implementato |

### 🎯 PNRR (Piano Nazionale Ripresa e Resilienza)

#### Missione 1: Digitalizzazione, Innovazione, Competitività
| Componente | Requisito | Implementazione | Status |
|-----------|-----------|-----------------|--------|
| M1Cx.y | [Descrizione] | [MS/SP mapping] | ✅ Implementato |

**Obiettivi di Misurazione**:
- [ ] Target 1: [Description]
- [ ] Target 2: [Description]
- [ ] Target 3: [Description]

### 📚 Piano Triennale AgID 2024-2026

#### Capitoli Pertinenti
| Capitolo | Requisito | Implementazione | Status |
|----------|-----------|-----------------|--------|
| Cap. X | [Descrizione] | [MS/SP mapping] | ✅ Implementato |

**Linee Guida AgID Applicate**:
- [ ] Modello 3+2 della PA Digitale
- [ ] API Design Standards (OpenAPI 3.0)
- [ ] Data Format Standards (DCAT-AP)
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Cloud Security (SPC deployment)

### 🔗 Cross-References
- Master Matrix: [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)
- PNRR Mapping: [COMPLIANCE-MAPPING-PNRR.md](COMPLIANCE-MAPPING-PNRR.md)
- Piano Triennale Mapping: [COMPLIANCE-MAPPING-PIANO-TRIENNALE.md](COMPLIANCE-MAPPING-PIANO-TRIENNALE.md)

### ✅ Compliance Checklist
- [ ] Tutti i requisiti normativi identificati
- [ ] MS/SP mapping completo
- [ ] System Card compilate (per ML systems)
- [ ] Security review eseguita
- [ ] Audit trail abilitato
- [ ] Disaster recovery testato (RTO/RPO met)
```

---

## 🔍 INTEGRATION CHECKLIST PER OGNI FILE

### Per ogni UC/MS file da aggiornare:

- [ ] **1. ANALISI**
  - [ ] Leggere file corrente completamente
  - [ ] Identificare gap tra documentation e nuovi requisiti
  - [ ] Cross-reference con COMPLIANCE-MATRIX.md v2.1

- [ ] **2. PLANNING**
  - [ ] Elencare tutti i requisiti PNRR applicabili
  - [ ] Elencare tutti i requisiti Piano Triennale applicabili
  - [ ] Mappare a MS/SP concreti
  - [ ] Identificare new section locations

- [ ] **3. WRITING**
  - [ ] Aggiungere "## 📋 Conformità Normativa & Framework Nazionali"
  - [ ] Compilare tabelle CAD, AI Act (se applicabile), eIDAS (se applicabile)
  - [ ] Aggiungere sezione PNRR con componenti specifiche
  - [ ] Aggiungere sezione Piano Triennale con capitoli pertinenti
  - [ ] Aggiungere sezione "🔗 Cross-References"
  - [ ] Aggiungere sezione "✅ Compliance Checklist"

- [ ] **4. VALIDATION**
  - [ ] Verificare che MS/SP reference sono corretti
  - [ ] Fare cross-check con COMPLIANCE-MATRIX.md
  - [ ] Verificare che link funzionano
  - [ ] Eseguire spell-check in italiano

- [ ] **5. TESTING**
  - [ ] Eseguire `./scripts/run_all_checks.sh`
  - [ ] Verificare che file pass TIER 1 validation
  - [ ] Controllare cross-references validation

- [ ] **6. COMMIT**
  - [ ] `git add docs/use_cases/UCX/README.md` (o MS path)
  - [ ] Commit message format:
    ```
    Docs: Add PNRR & Piano Triennale compliance to [UC/MS X]

    ## Changes
    - Added PNRR Missione X conformità mapping
    - Added Piano Triennale Cap X requirements
    - Added cross-references to COMPLIANCE-MATRIX.md v2.1
    - Added compliance checklist
    ```

---

## 📊 EFFORT ESTIMATION & TIMELINE

### Total Effort: 108 ore (13,5 giorni lavorativi)

#### Phase Breakdown:
- **Phase 1 (Critical)**: 63 hours → 4-5 settimane (Nov-Dec 2025)
- **Phase 2 (High)**: 33 hours → 4-5 settimane (Jan-Feb 2026)
- **Phase 3 (Medium)**: 42 hours → 5-6 settimane (Feb-Mar 2026)

#### Velocity: ~10-12 hours/week (assuming 2 file updates/week)

#### Realistic Timeline: **Q4 2025 - Q1 2026**

---

## 🎯 SUCCESS CRITERIA

### Per file aggiornato:
- ✅ Sezione "Conformità Normativa" completa
- ✅ Tutti i requisiti PNRR/Piano Triennale mappati a MS/SP
- ✅ Cross-reference con COMPLIANCE-MATRIX.md v2.1
- ✅ System Card presente (per ML systems)
- ✅ Security review completata
- ✅ File passa run_all_checks.sh TIER 1

### Completion Goal:
- ✅ 7/11 UC updated (64% → 100%)
- ✅ 5/16 MS updated (31% → 100%)
- ✅ 0 broken cross-references
- ✅ 100% PNRR requirements mapped
- ✅ 100% Piano Triennale requirements mapped

---

## 🚀 NEXT IMMEDIATE ACTIONS

### Week 1 (21-27 Nov 2025):
1. Create UC6 compliance section (2-3 hours)
2. Create UC7 compliance section (2 hours)
3. Create UC8 compliance section (3 hours)

### Week 2-3 (28 Nov - 11 Dec 2025):
4. Create UC9 compliance section (3-4 hours)
5. Create MS13 compliance section (4-5 hours)
6. Create MS14 compliance section (3-4 hours)

### Week 4-5 (12-27 Dec 2025):
7. Create UC1 compliance section (2 hours)
8. Create UC5 compliance section (3 hours)
9. Create UC11 compliance section (2 hours)
10. Create MS11 compliance section (3 hours)
11. Create MS16 compliance section (3-4 hours)

---

## 📚 Reference Documents

### Master Compliance Documents:
- `/docs/COMPLIANCE-MATRIX.md` (v2.1) - Complete regulatory mapping
- `/docs/COMPLIANCE-MAPPING-PNRR.md` - PNRR-specific matrix
- `/docs/COMPLIANCE-MAPPING-PIANO-TRIENNALE.md` - Piano Triennale-specific

### Regulatory Source Documents:
- `/docs/fonti/txt_output/PNRR.txt` - Full PNRR text
- `/docs/fonti/txt_output/Piano_Triennale_2024-2026_Aggiornamento_2026.txt`
- `/docs/fonti/txt_output/AI_Act.txt` - Full AI Act text
- `/docs/fonti/txt_output/CAD.txt` - Full CAD text

### Templates:
- `/docs/templates/conformita-normativa-standard.md`
- Individual UC/MS README.md files as working examples

---

**Document Owner**: ZenIA Compliance Team
**Last Updated**: 21 Novembre 2025
**Next Review**: Giugno 2026
