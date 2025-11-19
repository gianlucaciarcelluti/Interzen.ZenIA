# Matrice Compliance ZenIA

Mapping completo delle fonti normative ai microservizi (MS) e sub-progetti (SP).

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

### CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Digital-first | MS11-GATEWAY, MS02-ANALYZER | SP01-Intake Manager | Tutti processi digital-native |
| Art. 2 | Interoperabilità | MS16-REGISTRY, MS11-GATEWAY | SP02-Document Analyzer | Standard API |
| Art. 3 | Accessibilità | MS07-DISTRIBUTOR | SP10-Dashboard | WCAG 2.1 AA |
| Art. 21 | Documenti elettronici | MS01-CLASSIFIER, MS04-VALIDATOR | SP06-Validator | Validazione documenti |
| Art. 22 | Firma digitale | MS13-SECURITY, MS04-VALIDATOR | SP32-Timestamp Authority | RFC 3161 + eIDAS |
| Art. 23 | Marcatura temporale | MS13-SECURITY | SP32-Timestamp Authority | RFC 3161 TSA |
| Art. 41 | Conservazione dati | MS05-TRANSFORMER, MS06-AGGREGATOR | SP34-Preservation Engine | Conservazione + disposizione |
| Art. 62 | Standard metadati | MS02-ANALYZER | SP03-Procedural Classifier | ISO/IEC 23081 |

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

### AI Act (Regolamento 2024/1689)

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 6 | Valutazione rischio | MS02-ANALYZER, MS14-AUDIT | SP03-Procedural Classifier | Analisi rischio modello AI |
| Art. 8 | Compliance | MS14-AUDIT | SP08-Quality Checker | Documentazione test modello |
| Art. 13 | Trasparenza | MS14-AUDIT | SP03-Procedural Classifier | Spiegabilità modello |
| Art. 22 | Supervisione umana | MS02-ANALYZER | SP03-Procedural Classifier | Human-in-the-loop obbligatorio |

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

**Versione**: 1.0
**Ultimo Aggiornamento**: 2024-11-18
**Prossimo Review**: 2025-05-18
**Maintainers**: ZenIA Compliance Team
