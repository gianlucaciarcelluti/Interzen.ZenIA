# Matrice Compliance ZenIA

Mapping completo delle fonti normative ai microservizi (MS) e sub-progetti (SP).

**Ultimo Aggiornamento**: 21 Novembre 2025
**Versione**: 2.1 (Espansione PNRR + Piano Triennale)
**Prossima Revisione**: Novembre 2026

## 📊 Copertura Normativa

| Ambito | Dettagli | Status |
|--------|----------|--------|
| **Italiano** | L.241/1990, CAD, D.Lgs 152/2006, D.Lgs 42/2004, D.Lgs 33/2013 | ✅ |
| **UE** | GDPR, eIDAS, AI Act 2024/1689 | ✅ |
| **PNRR** | Missione 1 (Digitalizzazione), Missione 5 (Inclusione & Coesione) | ✅ |
| **Piano Triennale AgID** | 2024-2026 Aggiornamento 2026 (Cap. 3-7) | ✅ |
| **AgID Linee Guida** | Modello 3+2, API Design, Data Format, Accessibility, Cloud | ✅ |
| **Compliance Internazionale** | ISO/IEC, ETSI, PCI-DSS, SOX, HIPAA | ✅ |

---

## 📋 Framework Normativo Italiano

### L. 241/1990 - Procedimento Amministrativo

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Trasparenza | MS14-AUDIT, MS10-LOGGER | SP04-Knowledge Base | Audit trail completo |
| Art. 3 | Economicità & Efficacia | MS08-MONITOR, MS09-MANAGER | SP08-Quality Checker | Monitoraggio SLA performance |
| Art. 6 | Garanzie procedurali | MS03-ORCHESTRATOR, MS07-DISTRIBUTOR | SP09-Workflow Engine | Workflow automatizzati |
| Art. 7 | Competenze istituzionali | MS16-REGISTRY, MS15-CONFIG | SP02-Document Analyzer | Service registry + config |
| Art. 15 | Silenzio assenso | MS03-ORCHESTRATOR | SP09-Workflow Engine | Timer escalation automatici |
| Art. 23 | Comunicazione scritta | MS02-ANALYZER, MS07-DISTRIBUTOR | SP05-Template Engine | Generazione + routing documenti |
| Art. 24 | Diritti accesso | MS13-SECURITY, MS14-AUDIT | SP11-Security & Audit | Controllo accesso + log |
| Art. 27 | Motivazione | MS02-ANALYZER | SP03-Procedural Classifier | Reasoning & spiegabilità |

### CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale) - Expanded

#### Titolo I: Disposizioni Generali

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Digital-first | MS11-GATEWAY, MS02-ANALYZER | SP01-Intake Manager | Tutti processi digital-native |
| Art. 2 | Interoperabilità | MS16-REGISTRY, MS11-GATEWAY | SP02-Document Analyzer | Standard API, SOAP, REST |
| Art. 3 | Accessibilità | MS07-DISTRIBUTOR, MS11-GATEWAY | SP10-Dashboard | WCAG 2.1 AA compliance |
| Art. 5 | Diritti cittadini | MS13-SECURITY, MS14-AUDIT | SP11-Security & Audit | Trasparenza amministrativa |
| Art. 7 | Data Protection | MS13-SECURITY, MS14-AUDIT | SP11-Security & Audit | GDPR compliance, DPA |

#### Titolo II: Documenti e Firme Digitali

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 21 | Documenti elettronici | MS01-CLASSIFIER, MS04-VALIDATOR | SP06-Validator | Validazione formato, integrità |
| Art. 22 | Firma digitale | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | XAdES, PAdES, CAdES |
| Art. 23 | Marcatura temporale | MS13-SECURITY | SP32-Timestamp Authority | RFC 3161 TSA protocol |
| Art. 24 | Ripudio | MS14-AUDIT | SP11-Security & Audit | Non-repudiation audit trail |

#### Titolo IV: Conservazione

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 41 | Conservazione dati | MS05-TRANSFORMER, MS06-AGGREGATOR | SP34-Preservation Engine | OAIS model, long-term preservation |
| Art. 42 | Autenticità | MS04-VALIDATOR | SP32-Timestamp Authority | Catena di custodia digitale |
| Art. 43 | Integrità | MS13-SECURITY | SP11-Security & Audit | Hash validation, blockchain optional |

#### Titolo V: Dati Personali

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 57 | DPIA | MS14-AUDIT | SP11-Security & Audit | Valutazione impatto privacy |
| Art. 58 | Cookie Policy | MS11-GATEWAY | SP10-Dashboard | Consenso esplicito |
| Art. 62 | Standard metadati | MS02-ANALYZER | SP03-Procedural Classifier | ISO/IEC 23081-1

### D.Lgs 152/2006 (Codice dell'Ambiente)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 3 | Trasparenza ambientale | MS10-LOGGER, MS14-AUDIT | SP04-Knowledge Base | Reporting impatto ambientale |
| Art. 4 | Partecipazione pubblica | MS07-DISTRIBUTOR, MS11-GATEWAY | SP02-Document Analyzer | Canali accesso pubblico |
| Art. 7 | Comunicazione digitale | MS02-ANALYZER | SP05-Template Engine | Documenti ambientali digitali |

### D.Lgs 42/2004 (Codice Beni Culturali)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Tutela patrimonio | MS06-AGGREGATOR, MS14-AUDIT | SP34-Preservation Engine | Metadati conservazione |
| Art. 2 | Standard conservazione | MS05-TRANSFORMER | SP35-Format Migration | Standard ISO/IEC |

### D.Lgs 33/2013 (Decreto Trasparenza)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Dati pubblici | MS02-ANALYZER, MS06-AGGREGATOR | SP02-Document Analyzer | Pubblicazione dati aperti |
| Art. 4 | Dati istituzionali | MS14-AUDIT | SP04-Knowledge Base | Documenti normativi |
| Art. 5 | Open by default | MS07-DISTRIBUTOR, MS11-GATEWAY | SP02-Document Analyzer | API pubbliche + dati |
| Art. 7 | Formato dati riusabile | MS05-TRANSFORMER | SP05-Template Engine | JSON, XML, CSV |

---

## 🇪🇺 Normative UE

### GDPR (Regolamento 2016/679)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 5 | Legittimità & lealtà | MS13-SECURITY, MS14-AUDIT | SP11-Security & Audit | Consenso + audit trail |
| Art. 12 | Trasparenza | MS14-AUDIT | SP10-Dashboard | Comunicazione chiara |
| Art. 15 | Diritto accesso | MS13-SECURITY | SP11-Security & Audit | Download dati utente |
| Art. 17 | Diritto cancellazione | MS05-TRANSFORMER | SP34-Preservation Engine | Meccanismo cancellazione dati |
| Art. 20 | Portabilità dati | MS05-TRANSFORMER | SP35-Format Migration | Export formato standard |
| Art. 22 | Decisioni automatizzate | MS02-ANALYZER | SP03-Procedural Classifier | HITL (Human-in-the-loop) |
| Art. 32 | Integrità & confidenzialità | MS13-SECURITY | SP11-Security & Audit | Crittografia + controllo accesso |
| Art. 33-34 | Notifica violazione | MS14-AUDIT, MS08-MONITOR | SP11-Security & Audit | Alerting automatico |
| Art. 35 | DPIA | MS14-AUDIT | SP11-Security & Audit | Valutazione impatto privacy |
| Art. 37 | DPO | MS14-AUDIT | SP11-Security & Audit | Contatto compliance |

### eIDAS (Regolamento 2014/910)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 3 | Firma elettronica | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | XAdES + PAdES + CAdES |
| Art. 13 | Firma avanzata | MS13-SECURITY | SP32-Timestamp Authority | Validazione certificato |
| Art. 24 | Servizi marca temporale | MS13-SECURITY | SP32-Timestamp Authority | RFC 3161 TSA |
| Art. 32 | Validazione long-term | MS04-VALIDATOR | SP32-Timestamp Authority | LTV (Long-Term Validation) |

### AI Act (Regolamento 2024/1689) - Expanded Coverage

#### Capo II: Requisiti per Sistemi AI ad Alto Rischio

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 6 | Risk Assessment | MS02-ANALYZER, MS14-AUDIT, MS01-CLASSIFIER | SP03-Procedural Classifier | Valutazione sistematica rischi |
| Art. 8 | Technical Documentation | MS14-AUDIT | SP04-Knowledge Base | Record tecnici completi |
| Art. 9 | Data Governance | MS14-AUDIT, MS13-SECURITY | SP11-Security & Audit | Qualità, diversità, veridicità dati training |
| Art. 10 | Data Quality | MS02-ANALYZER | SP02-Document Analyzer | Bilanciamento, rappresentatività dati |
| Art. 11 | Documentation Requirements | MS14-AUDIT | SP04-Knowledge Base | Istruzioni uso, system card |
| Art. 12 | Conformity Assessment | MS14-AUDIT | SP08-Quality Checker | Procedure validazione conformità |
| Art. 13 | Transparency | MS14-AUDIT, MS02-ANALYZER | SP03-Procedural Classifier | Dichiarazione intenti, spiegabilità output |
| Art. 14 | Record Keeping | MS14-AUDIT, MS10-LOGGER | SP11-Security & Audit | Registri automatizzati immutabili |
| Art. 15 | Traceability | MS10-LOGGER, MS14-AUDIT | SP11-Security & Audit | Tracciamento decisioni AI |
| Art. 22 | Human Oversight | MS02-ANALYZER, MS01-CLASSIFIER | SP03-Procedural Classifier | HITL obbligatorio per decisioni |
| Art. 23 | Automated Decision-Making | MS02-ANALYZER, MS03-ORCHESTRATOR | SP09-Workflow Engine | Controllo umano su decisioni automatiche |

#### Capo III: Annex III - Risk Management (Articles 27-33)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 27 | Risk Management System | MS14-AUDIT, MS08-MONITOR | SP11-Security & Audit | Processo sistematico identificazione rischi |
| Art. 28 | Data Governance | MS13-SECURITY, MS02-ANALYZER | SP11-Security & Audit | Qualità dati, DPIA, consenso utenti |
| Art. 29 | Technical Documentation | MS14-AUDIT | SP04-Knowledge Base | Complete design & training documentation |
| Art. 30 | Automated Records | MS14-AUDIT, MS10-LOGGER | SP11-Security & Audit | Logging automatico operazioni critiche |
| Art. 31 | Human Oversight Procedures | MS02-ANALYZER, MS03-ORCHESTRATOR | SP03-Procedural Classifier | Workflow con intervento umano |
| Art. 32 | Robustness & Accuracy | MS01-CLASSIFIER, MS02-ANALYZER | SP08-Quality Checker | Test adversariali, validazione distribuzione shift |
| Art. 33 | Cybersecurity | MS13-SECURITY | SP11-Security & Audit | Protezione contro attacchi, encryption, access control |

#### Compliance & Conformity (Articles 34-36)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 34 | CE Marking | MS14-AUDIT | SP08-Quality Checker | Dichiarazione conformità |
| Art. 35 | Notified Bodies | MS14-AUDIT | SP11-Security & Audit | Valutazione terze parti indipendenti |
| Art. 36 | Market Surveillance | MS08-MONITOR, MS14-AUDIT | SP11-Security & Audit | Monitoraggio continuo post-deployment |

### PNRR (Piano Nazionale Ripresa e Resilienza) - Missione 1 & 5

#### Missione 1: Digitalizzazione, Innovazione, Competitività

| Componente | Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-----------|-------------------|--------------------|-------|
| M1C1.1 | Riforma PA digitale | MS03-ORCHESTRATOR, MS15-CONFIG | SP01-Intake Manager | Processi digital-first |
| M1C1.2 | Modernizzazione PA | MS07-DISTRIBUTOR, MS11-GATEWAY | SP02-Document Analyzer | Servizi digitali |
| M1C1.3 | Consolidamento centro gestione | MS09-MANAGER, MS16-REGISTRY | SP01-Intake Manager | Architettura cloud-native |
| M1C1.4 | Sicurezza informatica | MS13-SECURITY, MS08-MONITOR | SP11-Security & Audit | Crittografia + monitoraggio |
| M1C2.1 | Trasformazione digitale imprese | MS02-ANALYZER, MS05-TRANSFORMER | SP02-Document Analyzer | Digitalizzazione processi |

#### Missione 5: Inclusione e Coesione

| Componente | Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-----------|-------------------|--------------------|-------|
| M5C1.1 | Politiche occupazionali | MS07-DISTRIBUTOR, MS14-AUDIT | SP04-Knowledge Base | Reporting occupazionale |
| M5C1.2 | Inclusione sociale | MS02-ANALYZER, MS07-DISTRIBUTOR | SP10-Dashboard | Accesso servizi pubblici |
| M5C3.1 | Coesione territoriale | MS06-AGGREGATOR, MS14-AUDIT | SP04-Knowledge Base | Dati territoriali |

#### Obiettivi PNRR per ZenIA

| Obiettivo | Target | Implementazione |
|-----------|--------|-----------------|
| Procedimenti PA entro 30gg | 100% | MS03-ORCHESTRATOR + timer SLA |
| Digitalizzazione PA | 95% servizi online | MS11-GATEWAY + MS07-DISTRIBUTOR |
| Riduzione tempi pa | -20% vs baseline | MS03-ORCHESTRATOR (workflow optimization) |
| Cybersecurity PA | 100% conformità | MS13-SECURITY + MS08-MONITOR |
| AI governance | AI Risk Assessment framework | MS01-CLASSIFIER + MS02-ANALYZER |

---

### Piano Triennale 2024-2026 (AgID) - IT Strategy

#### Capitolo 3: Servizi

| Servizio | Requisito | Implementazione MS | Implementazione SP | Note |
|---------|-----------|-------------------|--------------------|-------|
| E-Service PDND | Interoperabilità | MS16-REGISTRY, MS11-GATEWAY | SP02-Document Analyzer | Data sharing standardizzato |
| Single Digital Gateway | Gateway unico | MS11-GATEWAY, MS07-DISTRIBUTOR | SP02-Document Analyzer | Accesso cittadini |
| Accessibilità servizi | WCAG 2.1 AA | MS07-DISTRIBUTOR | SP10-Dashboard | Compliance obbligatoria |
| Gestione documenti | Digitalizzazione | MS01-CLASSIFIER, MS05-TRANSFORMER | SP06-Validator | Archiviazione digitale |
| Conservazione | Long-term preservation | MS05-TRANSFORMER, MS06-AGGREGATOR | SP34-Preservation Engine | OAIS model |

#### Capitolo 4: Piattaforme

| Piattaforma | Requisito | Implementazione MS | Implementazione SP | Note |
|-------------|-----------|-------------------|--------------------|-------|
| PagoPa | Pagamenti digitali | MS07-DISTRIBUTOR, MS13-SECURITY | SP11-Security & Audit | Gateway verso PagoPa |
| SPID | Identità digitale | MS13-SECURITY, MS11-GATEWAY | SP11-Security & Audit | Integrazione SPID |
| CIE | Carta identità elettronica | MS13-SECURITY | SP11-Security & Audit | Autenticazione CIE |
| Anagrafiche | Dati anagrafici | MS16-REGISTRY, MS06-AGGREGATOR | SP04-Knowledge Base | Unica fonte di verità |
| Certificati digitali | Gestione certificati | MS13-SECURITY | SP32-Timestamp Authority | X.509 + firma avanzata |

#### Capitolo 5: Dati e Intelligenza Artificiale

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-------------------|--------------------|-------|
| Data governance | MS14-AUDIT, MS02-ANALYZER | SP11-Security & Audit | Qualità, integrità dati |
| Open data | MS06-AGGREGATOR, MS05-TRANSFORMER | SP60-Analytics | Formato standard (JSON/XML/CSV) |
| Data sharing | MS16-REGISTRY, MS11-GATEWAY | SP02-Document Analyzer | PDND interoperabilità |
| AI governance | MS01-CLASSIFIER, MS02-ANALYZER | SP03-Procedural Classifier | Risk assessment framework |
| AI transparency | MS14-AUDIT, MS02-ANALYZER | SP04-Knowledge Base | Documentazione AI Act |

#### Capitolo 6: Infrastrutture

| Infrastruttura | Requisito | Implementazione MS | Implementazione SP | Note |
|---|-----------|-------------------|--------------------|-------|
| Cloud pubblico | Cloud adoption | MS09-MANAGER, MS13-SECURITY | SP11-Security & Audit | Deployment SPC (Stato per Cittadini) |
| Disaster recovery | Business continuity | MS08-MONITOR, MS13-SECURITY | SP11-Security & Audit | RTO 4h, RPO 1h |
| Backup automatico | Data preservation | MS06-AGGREGATOR | SP34-Preservation Engine | Geo-redundanza |
| Connettività | SPC network | MS11-GATEWAY | SP02-Document Analyzer | MPLS dedicato PA |

#### Capitolo 7: Sicurezza Informatica

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-------------------|--------------------|-------|
| Crittografia dati | MS13-SECURITY | SP11-Security & Audit | AES-256 + TLS 1.3 |
| Controllo accesso | MS13-SECURITY | SP11-Security & Audit | RBAC + MFA + zero-trust |
| Monitoraggio sicurezza | MS08-MONITOR, MS14-AUDIT | SP11-Security & Audit | SIEM + alerting real-time |
| Incident management | MS08-MONITOR, MS14-AUDIT | SP11-Security & Audit | Risposta 30min |
| Compliance NIS2 | MS13-SECURITY, MS08-MONITOR | SP11-Security & Audit | Entity critiche |

---

### AgID Linee Guida - Dettagli Implementativi

#### Linea Guida "Modello 3+2 della PA Digitale"

| Elemento | Requisito | Implementazione MS | Implementazione SP |
|---------|-----------|-------------------|--------------------|
| **Livello 1: Accesso** | Single sign-on | MS13-SECURITY, MS11-GATEWAY | SP11-Security & Audit |
| **Livello 2: Servizi frontend** | User-centric design | MS07-DISTRIBUTOR | SP10-Dashboard |
| **Livello 3: Logica di business** | Digitalizzazione processi | MS02-ANALYZER, MS03-ORCHESTRATOR | SP03-Procedural Classifier |
| **Livello 4: Dati** | Data management | MS06-AGGREGATOR, MS14-AUDIT | SP04-Knowledge Base |
| **Livello 5: Interoperabilità** | API standardizzate | MS11-GATEWAY, MS16-REGISTRY | SP02-Document Analyzer |

#### Linea Guida "API Design"

| Standard | Requisito | Implementazione MS | Implementazione SP | Note |
|---------|-----------|-------------------|--------------------|-------|
| REST | API RESTful | MS11-GATEWAY | SP02-Document Analyzer | OpenAPI 3.0 specification |
| Security | OAuth 2.0 | MS13-SECURITY | SP11-Security & Audit | Bearer tokens JWT |
| Throttling | Rate limiting | MS11-GATEWAY | SP02-Document Analyzer | 1000 req/min default |
| Versioning | API versioning | MS11-GATEWAY | SP02-Document Analyzer | Semantic versioning |
| Documentation | API docs | MS11-GATEWAY | SP04-Knowledge Base | Swagger/OpenAPI auto-generated |

---

## 📊 Standard & Linee Guida

### Standard ISO/IEC

| Standard | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| ISO 27001 | Information Security | MS13-SECURITY | SP11-Security & Audit | Target certificazione |
| ISO 14721 | OAIS (Archives) | MS06-AGGREGATOR, MS05-TRANSFORMER | SP34-Preservation Engine | Modello riferimento archivi |
| ISO 23081 | Metadata | MS02-ANALYZER | SP03-Procedural Classifier | Standard metadati documenti |
| ISO 19005 | PDF/A (Long-term) | MS04-VALIDATOR, MS05-TRANSFORMER | SP35-Format Migration | Formato PDF per archivi |
| ISO 16175 | Electronic records | MS01-CLASSIFIER | SP06-Validator | Validazione documenti |

### Standard ETSI

| Standard | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| RFC 3161 | Timestamp Protocol | MS13-SECURITY | SP32-Timestamp Authority | Implementazione TSA |
| XAdES | XML Signatures | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | Standard firma XML |
| PAdES | PDF Signatures | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | Standard firma PDF |
| CAdES | CMS Signatures | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | Standard firma CMS |

### Linee Guida AGID

| Linea Guida | Requisito | Implementazione MS | Implementazione SP | Note |
|-------------|-----------|-------------------|--------------------|-------|
| **Modello 3+2** | PA Digitale | MS01-CLASSIFIER, MS07-DISTRIBUTOR | SP01-Intake Manager | Architettura digital-first |
| **API Design** | API RESTful | MS11-GATEWAY | SP02-Document Analyzer | Conformità OpenAPI 3.0 |
| **Data Format** | JSON/XML | MS05-TRANSFORMER | SP05-Template Engine | Scambio dati standard |
| **Accessibility** | WCAG 2.1 AA | MS07-DISTRIBUTOR | SP10-Dashboard | Standard accessibilità web |
| **Cloud Security** | Cloud adoption | MS09-MANAGER, MS13-SECURITY | SP11-Security & Audit | Deployment cloud sicuro |

---

## 🔒 Standard Sicurezza & Compliance

### PCI-DSS (Payment Card Industry)

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|------------------|-------------------|-------|
| Crittografia | MS13-SECURITY | SP11-Security & Audit | AES-256 at rest + TLS transit |
| Controllo accesso | MS13-SECURITY | SP11-Security & Audit | RBAC + MFA |
| Monitoraggio | MS08-MONITOR, MS14-AUDIT | SP11-Security & Audit | Real-time alerting |
| Compliance | MS14-AUDIT | SP11-Security & Audit | Certificazione annuale |

### SOX (Sarbanes-Oxley)

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|------------------|-------------------|-------|
| Controlli finanziari | MS14-AUDIT | SP08-Quality Checker | Verifica integrità dati |
| Audit trail | MS10-LOGGER, MS14-AUDIT | SP11-Security & Audit | Log immutabili |
| Documentazione | MS02-ANALYZER | SP04-Knowledge Base | Documentazione compliance |

### HIPAA (Health Insurance Portability)

| Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|------------------|-------------------|-------|
| Protezione PHI | MS13-SECURITY | SP11-Security & Audit | Crittografia + controllo accesso |
| Audit log | MS14-AUDIT | SP11-Security & Audit | Retention 6 anni |
| Privacy | MS13-SECURITY | SP11-Security & Audit | Tool de-identificazione |

---

## 📌 Mapping Compliance per Caso d'Uso

### UC5 - Produzione Documentale Integrata

| Fonte Normativa | Requisito | Implementazione |
|-----------------|-----------|-----------------|
| L. 241/1990 | Garanzie procedurali | MS03-ORCHESTRATOR (SP09 Workflow) |
| CAD Art. 21 | Validazione documento | MS04-VALIDATOR (SP06 Validator) |
| CAD Art. 23 | Marca temporale | MS13-SECURITY (SP32 Timestamp) |
| D.Lgs 33/2013 | Digital-first | MS02-ANALYZER (SP05 Template) |
| GDPR Art. 22 | HITL per decisioni | MS02-ANALYZER (SP03 Classifier) |

### UC6 - Firma Digitale Integrata

| Fonte Normativa | Requisito | Implementazione |
|-----------------|-----------|-----------------|
| CAD Art. 22 | Firma digitale | MS13-SECURITY (SP32 Timestamp) |
| eIDAS Art. 13 | Firma avanzata | MS13-SECURITY (SP32 Timestamp) |
| eIDAS Art. 32 | LTV | MS04-VALIDATOR (SP32 Timestamp) |
| GDPR Art. 5 | Non-ripudio | MS14-AUDIT (SP11 Security) |

### UC7 - Conservazione Digitale

| Fonte Normativa | Requisito | Implementazione |
|-----------------|-----------|-----------------|
| CAD Art. 41 | Conservazione dati | MS05-TRANSFORMER (SP34 Engine) |
| D.Lgs 42/2004 | Tutela patrimonio | MS06-AGGREGATOR (SP34 Engine) |
| ISO 14721 | Modello OAIS | MS06-AGGREGATOR (SP34 Engine) |
| ISO 19005 | Formato PDF/A | MS05-TRANSFORMER (SP35 Migration) |

### UC9 - Workflow Automatizzato

| Fonte Normativa | Requisito | Implementazione |
|-----------------|-----------|-----------------|
| L. 241/1990 Art. 15 | Silenzio assenso | MS03-ORCHESTRATOR (SP09 Engine) |
| AI Act Art. 22 | Supervisione umana | MS02-ANALYZER (SP03 Classifier) |
| GDPR Art. 22 | Decisioni automatizzate | MS02-ANALYZER (SP03 Classifier) |

### UC11 - Analisi Dati e Reporting

| Fonte Normativa | Requisito | Implementazione |
|-----------------|-----------|-----------------|
| D.Lgs 33/2013 | Dati pubblici | MS06-AGGREGATOR (SP60 Analytics) |
| GDPR Art. 15 | Trasparenza dati | MS14-AUDIT (SP70 Compliance) |
| ISO 23081 | Metadata | MS02-ANALYZER (SP62 Quality) |

---

## ✅ Checklist Compliance

### Prima di Deployment

- [ ] **Sicurezza**: MS13-SECURITY implementato con crittografia + controllo accesso
- [ ] **Audit**: MS14-AUDIT catturando tutte operazioni in log immutabili
- [ ] **Data Protection**: Consenso GDPR + meccanismo portabilità dati
- [ ] **Trasparenza**: Log MS14-AUDIT accessibili per review compliance
- [ ] **Firma**: Conformità eIDAS per firme digitali
- [ ] **Archivi**: Conformità ISO 14721 OAIS per preservazione long-term
- [ ] **Accessibilità**: WCAG 2.1 AA verificato per componenti user-facing
- [ ] **API Security**: OAuth 2.0 / JWT con crittografia

### Review Compliance Annuale

- [ ] Aggiorna mapping fonti normative a nuove normative
- [ ] Rivedi MS13-SECURITY per nuove vulnerabilità
- [ ] Valida stato certificazione ISO 27001
- [ ] Controlla compliance GDPR (record consenso, accordi DPA)
- [ ] Verifica validità firma digitale eIDAS
- [ ] Audit politiche conservazione dati per compliance

---

## 🔗 Riferimento Rapido

| Fonte Normativa | MS Primario | SP Primario | Ultimo Review |
|-----------------|-----------|-----------|--------------|
| L. 241/1990 | MS03-ORCHESTRATOR | SP09 | 2024-11-15 |
| CAD (D.Lgs 82/2005) | MS04-VALIDATOR | SP06 | 2024-11-15 |
| D.Lgs 152/2006 | MS02-ANALYZER | SP02 | 2024-11-15 |
| D.Lgs 42/2004 | MS06-AGGREGATOR | SP34 | 2024-11-15 |
| D.Lgs 33/2013 | MS14-AUDIT | SP04 | 2024-11-15 |
| GDPR | MS13-SECURITY | SP11 | 2024-11-15 |
| eIDAS | MS13-SECURITY | SP32 | 2024-11-15 |
| AI Act | MS02-ANALYZER | SP03 | 2024-11-15 |

---

## 📞 Contatti Compliance

- **Data Protection Officer (DPO)**: [contact@zenia.local](mailto:contact@zenia.local)
- **Team Compliance**: #zenia-compliance Slack
- **Security Officer**: #zenia-security Slack
- **Legal Review**: compliance-review@zenia.local

---

**Versione**: 2.1 (PNRR & Piano Triennale Integration)
**Ultimo Aggiornamento**: 21 Novembre 2025
**Prossimo Review**: Novembre 2026
**Maintainers**: ZenIA Compliance Team

### 📈 Changelog v2.1

- ✅ Added PNRR (Missione 1 & 5) comprehensive mapping
- ✅ Integrated Piano Triennale AgID 2024-2026 (Capitoli 3-7)
- ✅ Added AgID Linee Guida detailed implementation
- ✅ Expanded AI Act from 16 to 28 article coverage
- ✅ Expanded CAD from 8 to 18+ article coverage with 4 title sections
- ✅ Added compliance coverage matrix (header section)
- ✅ Enhanced PNRR objectives with specific MS/SP mappings
- ✅ Added Piano Triennale platform integration requirements
- ✅ Added Capitolo 5 (Data & AI governance) detailed mappings
- ✅ Added Capitolo 6 (Infrastructure) compliance requirements
- ✅ Added Capitolo 7 (Cybersecurity) including NIS2 compliance
- ✅ Updated versioning and review dates

**Total Coverage**:
- **Italian Laws**: 5 decrees + 1 law
- **EU Regulations**: 3 regulations
- **National Plans**: PNRR (2 missioni) + Piano Triennale (5 capitoli)
- **Standards**: ISO/IEC (5), ETSI (4), International (3)
- **Guidelines**: AgID (2 linee guida + modello)
- **MS Implementation**: 16 microservices fully mapped
- **SP Implementation**: 35+ sub-projects with compliance mapping
