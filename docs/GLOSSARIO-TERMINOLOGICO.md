# GLOSSARIO TERMINOLOGICO ZENÍA

**Data Creazione**: 2025-11-19
**Versione**: 1.0
**Status**: ATTIVO
**Owner**: Tech Writing Team

---

## INTRODUZIONE

Questo glossario stabilisce le decisioni standardizzate per la terminologia **inglese-italiana** (EN/IT) utilizzata nella documentazione ZenIA. Fornisce:

1. **Mappature ufficiali EN→IT** per oltre 50 termini ricorrenti
2. **Criteri decisionali** per le scelte terminologiche
3. **Contesto d'uso** e **patterns di applicazione**
4. **Eccezioni e varianti** documentate

### Principi di Standardizzazione

| Principio | Descrizione | Esempio |
|-----------|-------------|---------|
| **Precisione Dominio** | Usare terminologia specializzata PA digitale italiana quando disponibile | "Classificatore" (non "Categorizzatore") |
| **Coerenza UC/SP** | Stessa traduzione per stesso concetto in tutti i contesti | "Workflow" → sempre "Workflow" o sempre "Flusso di Lavoro" |
| **Internazionalizzazione** | Mantenere alcuni termini in inglese se universalmente riconosciuti | "API" (non "Interfaccia Applicativa") |
| **Leggibilità** | Preferire brevi forme composte rispetto a lunghe perifrasi | "Motore Workflow" (non "Sistema di gestione e orchestrazione dei flussi di lavoro") |
| **Conformità Normativa** | Allinearsi a vocabolario CAD, GDPR, AGID quando disponibile | "Titolarità Dati" (da GDPR) |

---

## SEZIONE 1: CORE INFRASTRUCTURE TERMS

### 1.1 Architettura e Componenti

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP Applicabili |
|---------|-------------------|-----------------|------------------|
| **Workflow** | Workflow / Flusso di Lavoro¹ | UC1-UC11 | UC5, UC9, UC3 |
| **Dashboard** | Pannello di Controllo / Dashboard² | Monitoraggio realtime | SP10, SP41, SP56 |
| **Pipeline** | Pipeline / Catena di Elaborazione¹ | Dati, Deployment | SP59, SP68 |
| **Parser** | Parser / Analizzatore | Elaborazione file | SP01, SP02 |
| **Classifier** | Classificatore | ML/IA workflow | SP07, SP03 |
| **Validator** | Validatore / Verificatore¹ | Quality control | SP06, SP08 |
| **Scheduler** | Schedulatore / Pianificatore¹ | Esecuzione risorse | SP25, SP27 |
| **API Gateway** | Gateway API | Integrazione | SP67 |

¹ **Nota**: Forme composte preferibili per leggibilità
² **Dashboard**: Mantenere forma inglese in contesti tecnici

### 1.2 Sicurezza e Compliance

| Termine | Traduzione Ufficiale | Contesto d'Uso | Standard | SP |
|---------|-------------------|-----------------|----------|-------|
| **Policy** | Politica / Norma¹ | Regole aziendali, compliance | CAD, GDPR | SP42, SP44, SP11 |
| **Enforcement** | Applicazione / Enforcement² | Imposizione di norma | Compliance | SP23, SP46 |
| **Audit Log** | Registro di Audit / Log Audit | Traccia attività | CAD art.15-bis | SP11, SP70 |
| **Compliance** | Conformità | Allineamento normativo | GDPR, CAD | SP44, SP46 |
| **Permission** | Permesso / Autorizzazione | Diritto accesso | IAM | SP11, SP20 |

¹ **Policy**: "Politica" in contesti organizzativi; "Norma" per compliance normative
² **Enforcement**: Termine tecnico; accettabile in contesti specializzati

### 1.3 Data Management

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|---------|
| **Data Lake** | Data Lake / Lago Dati¹ | Repository centralizzato | SP58 |
| **ETL** | ETL (Extract-Transform-Load) | Pipeline dati | SP59 |
| **Data Quality** | Qualità Dati | Validazione integrità | SP62 |
| **Metadata** | Metadati | Descrizione dati | SP14, SP37 |
| **Data Governance** | Governance dei Dati | Gestione dati enterprise | SP62, SP66 |

¹ **Data Lake/Warehouse**: Mantenere nomi inglesi per uso internazionale

---

## SEZIONE 2: DOCUMENT PROCESSING TERMS

### 2.1 Extraction & Classification

| Termine | Traduzione Ufficiale | Contesto d'Uso | Normativa | SP |
|---------|-------------------|-----------------|-----------|-----|
| **Document Extraction** | Estrazione Documenti | OCR, NLP processing | CAD | SP02 |
| **Content Classification** | Classificazione Contenuti | Categorizzazione automatica | - | SP07 |
| **Procedural Classification** | Classificazione Procedurale | Categorizzazione UC specifici | CAD | SP03 |
| **Attachment Classification** | Classificazione Allegati | Riconoscimento file | CAD | SP02 |
| **Quality Checking** | Controllo Qualità / Verifica Qualità | QA automated | ISO 9001 | SP08 |

### 2.2 Document Generation

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Template Engine** | Motore Template / Motore Modelli¹ | Generazione documenti | SP05 |
| **Document Generation** | Generazione Documenti | Creazione automatica | SP05, SP49 |
| **Knowledge Base** | Base Conoscenze / Knowledge Base² | Repository informazioni | SP04, SP52 |
| **Semantic Search** | Ricerca Semantica | Ricerca intelligente | SP12 |
| **Q&A Engine** | Motore Q&A / Motore Domande e Risposte¹ | Question-Answering system | SP12 |

---

## SEZIONE 3: DIGITAL SIGNATURE & CONSERVATION

### 3.1 Digital Signature

| Termine | Traduzione Ufficiale | Contesto d'Uso | Normativa | SP |
|---------|-------------------|-----------------|-----------|-----|
| **Digital Signature** | Firma Digitale | Signing autenticato | CAD art.20-22, eIDAS | SP29 |
| **Certificate Manager** | Gestore Certificati | Gestione certificati X.509 | CAD art.11, eIDAS | SP30 |
| **Timestamp Authority** | Autorità Timestamp | Marcatura temporale | RFC 3161, eIDAS | SP32 |
| **Temporal Marking** | Marcatura Temporale | TSA process | RFC 3161 | SP32 |
| **Signature Workflow** | Workflow Firma | Flusso firma multipla | eIDAS | SP31 |

### 3.2 Archive & Preservation

| Termine | Traduzione Ufficiale | Contesto d'Uso | Normativa | SP |
|---------|-------------------|-----------------|-----------|-----|
| **Archive Manager** | Gestore Archivio | Gestione archivio digitale | CAD art.43-44 | SP33 |
| **Preservation Engine** | Motore Conservazione | Long-term preservation | DPCM 2014 | SP34 |
| **Integrity Validation** | Validazione Integrità | Verifica integrità documenti | CAD art.23 | SP35 |
| **Storage Optimization** | Ottimizzazione Archiviazione | Compressione, deduplicazione | DPCM 2014 | SP36 |

---

## SEZIONE 4: MONITORING & ANALYTICS

### 4.1 SIEM & Monitoring

| Termine | Traduzione Ufficiale | Contesto d'Uso | Standard | SP |
|---------|-------------------|-----------------|----------|-----|
| **SIEM** | SIEM (Gestione Eventi Sicurezza)¹ | Security monitoring | ISO 27035 | SP38-41 |
| **SIEM Collector** | Collettore SIEM | Data collection | - | SP38 |
| **SIEM Processor** | Elaboratore SIEM | Event processing | - | SP39 |
| **SIEM Storage** | Archiviazione SIEM | Event repository | ISO 27001 | SP40 |
| **SIEM Analytics** | Analitiche SIEM / Analisi SIEM² | Event analytics | - | SP41 |
| **Alert** | Avviso / Allarme | Notifica di evento | ISO 27035 | SP65, SP41 |

### 4.2 Analytics & Reporting

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Advanced Analytics** | Analitiche Avanzate | BI/IA analytics | SP60 |
| **Predictive Analytics** | Analitiche Predittive | Forecasting | SP64 |
| **Real-Time Analytics** | Analitiche Real-Time | Streaming analytics | SP63 |
| **Performance Monitoring** | Monitoraggio Prestazioni | KPI tracking | SP65 |
| **Business Intelligence** | Business Intelligence / Intelligenza Aziendale | Data-driven decisions | SP60, SP61 |
| **Reporting** | Reporting / Generazione Rapporti¹ | Report generation | SP47, SP56 |

---

## SEZIONE 5: SUPPORT & TRAINING

### 5.1 Help Desk & Support

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Help Desk** | Help Desk / Servizio di Supporto¹ | User support | SP51 |
| **Knowledge Base Management** | Gestione Base Conoscenze | KB maintenance | SP52 |
| **Virtual Assistant** | Assistente Virtuale | Chatbot system | SP53 |
| **Chatbot** | Chatbot / Bot Conversazionale² | Conversational AI | SP53 |
| **User Training** | Formazione Utenti | Training platform | SP54 |
| **Self-Service Portal** | Portale Self-Service | User portal | SP55 |
| **User Feedback Management** | Gestione Feedback Utenti | Feedback system | SP57 |

### 5.2 Compliance Training

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Compliance Training** | Formazione Conformità | Compliance education | SP50 |
| **Certification Program** | Programma Certificazione | Certification tracking | SP50 |

---

## SEZIONE 6: COMPLIANCE & GOVERNANCE

### 6.1 Governance

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Organization Chart Manager** | Gestore Organigramma | Organizational structure | SP20 |
| **Procedure Manager** | Gestore Procedure | Procedure management | SP21 |
| **Process Governance** | Governance Processi | Process management | SP22 |
| **Compliance Monitoring** | Monitoraggio Conformità | Continuous compliance | SP44, SP23 |
| **Regulatory Intelligence** | Intelligenza Normativa | Regulation tracking | SP45 |
| **Regulatory Change Management** | Gestione Cambiamenti Normativi | Compliance updates | SP49 |

---

## SEZIONE 7: INTEGRATION & DEVOPS

### 7.1 Integration & APIs

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **API Gateway** | Gateway API | API aggregation | SP67 |
| **Integration Layer** | Livello Integrazione | System integration | SP67 |
| **Microservices** | Microservizi | Service architecture | MS (all) |

### 7.2 DevOps & CI/CD

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **CI/CD Pipeline** | Pipeline CI/CD¹ | Continuous integration | SP68 |
| **DevOps** | DevOps | Development operations | SP68 |
| **Infrastructure as Code** | Infrastruttura come Codice | IaC | SP68 |
| **Disaster Recovery** | Disaster Recovery / Recupero da Disastri¹ | DR planning | SP69 |
| **Business Continuity** | Continuità Aziendale | BC planning | SP69 |
| **Performance Optimization** | Ottimizzazione Prestazioni | Performance tuning | SP71 |

---

## SEZIONE 8: MACHINE LEARNING & AI

### 8.1 ML/AI Terminology

| Termine | Traduzione Ufficiale | Contesto d'Uso | SP |
|---------|-------------------|-----------------|-----|
| **Machine Learning** | Machine Learning / Apprendimento Automatico¹ | ML algorithms | SP60 |
| **Artificial Intelligence** | Intelligenza Artificiale (IA) | AI systems | SP60, SP53 |
| **Natural Language Processing** | Elaborazione Linguaggio Naturale (PLN)² | Text processing | SP12 |
| **Named Entity Recognition** | Riconoscimento Entità Nominate | Entity extraction | SP12 |
| **Model Training** | Addestramento Modello | ML training | SP60 |
| **Neural Network** | Rete Neurale | Deep learning | SP60 |

---

## SEZIONE 9: CROSS-CUTTING CONCERNS

### 9.1 General Terms

| Termine | Traduzione Ufficiale | Nota |
|---------|-------------------|------|
| **System** | Sistema | Usare in contesti architetturali |
| **Service** | Servizio | Usare in contesti applicativi |
| **Component** | Componente | Usare per parti discrete |
| **Module** | Modulo | Usare per unità software |
| **Interface** | Interfaccia | Uso generico |
| **Request** | Richiesta / Request¹ | "Richiesta" in italiano, "Request" in JSON |
| **Response** | Risposta / Response¹ | "Risposta" in italiano, "Response" in JSON |

¹ **Request/Response**: In contesti JSON, mantenere forma inglese

---

## SEZIONE 10: ACRONYMS & ABBREVIATIONS

### 10.1 Technical Acronyms (Maintain English)

| Acronimo | Espansione | Italiano | Uso Raccomandato |
|----------|-----------|---------|-----------------|
| **API** | Application Programming Interface | Interfaccia Applicativa | Mantenere API |
| **RBAC** | Role-Based Access Control | Controllo Accesso Basato Ruolo | Mantenere RBAC |
| **ETL** | Extract-Transform-Load | Estrazione-Trasformazione-Caricamento | Mantenere ETL |
| **BI** | Business Intelligence | Intelligenza Aziendale | Mantenere BI |
| **KPI** | Key Performance Indicator | Indicatore Prestazioni Chiave | Mantenere KPI |
| **SIEM** | Security Information & Event Management | Gestione Eventi Sicurezza | Espandere al primo uso |
| **ML** | Machine Learning | Apprendimento Automatico | Mantenere ML |
| **AI / IA** | Artificial Intelligence | Intelligenza Artificiale | Preferire IA in contesti italiani |
| **JSON** | JavaScript Object Notation | - | Mantenere JSON |
| **REST** | Representational State Transfer | - | Mantenere REST |
| **K8s** | Kubernetes | - | Mantenere K8s |
| **CI/CD** | Continuous Integration / Continuous Deployment | Integrazione/Deployment Continuo | Mantenere CI/CD |
| **GDPR** | General Data Protection Regulation | Regolamento Protezione Dati | Mantenere GDPR |
| **CAD** | Codice Amministrazione Digitale | - | Mantenere CAD |
| **AGID** | Agenzia per l'Italia Digitale | - | Mantenere AGID |
| **eIDAS** | Electronic Identification, Authentication and Trust Services | - | Mantenere eIDAS |

---

## SEZIONE 11: NORMATIVA & REGULATORY TERMS

### 11.1 Italian Regulatory Framework

| Termine | Acronimo | Applicazione | SP/UC |
|---------|----------|--------------|--------|
| **Codice dell'Amministrazione Digitale** | CAD | Firma digitale, Conservazione | UC6, UC7, UC9 |
| **Conservazione Sostitutiva** | - | Long-term document preservation | UC7, SP34 |
| **Titolarità Dati** | - | Data ownership (GDPR) | SP62, SP66 |

### 11.2 EU/International Standards

| Termine | Acronimo | Applicazione |
|---------|----------|--------------|
| **General Data Protection Regulation** | GDPR | Data management, Privacy |
| **eIDAS Regulation** | eIDAS | Digital signatures, Trust |
| **RFC 3161** | TSA Standard | Timestamp Authority |
| **ISO 27001** | Information Security | Information security |

---

## SEZIONE 12: DECISION MATRIX

### 12.1 How to Choose Between EN/IT Terms

**Usa INGLESE quando**:
1. Termine non ha traducibilità univoca in italiano
2. Acronimo/forma abbreviata è universalmente riconosciuta (API, RBAC, K8s)
3. Termine è standard tecnico internazionale (RFC 3161, JSON, REST)
4. Documento è tecnico e target è developer/architect
5. Continuità con documentazione internazionale è importante

**Usa ITALIANO quando**:
1. Traduzione è chiara, breve e non ambigua
2. Documento è per audience non-tecnico
3. Allineamento con normativa italiana è richiesto
4. Coerenza con documentazione PA italiana è importante
5. Contesto amministrativo/aziendale lo richiede

**Usa BILINGUAL (EN → IT) quando**:
1. Primo uso di termine nel documento
2. Termine è critico ma target non è technical
3. Glossario ha entrambe le forme

### 12.2 Special Cases

| Caso | Regola | Esempio |
|------|--------|---------|
| **JSON Fields** | Sempre INGLESE | Mantenere `"workflow_id"` |
| **Code/Pseudo-code** | Sempre INGLESE | Mantenere keyword programming |
| **Product Names** | Mantieni ORIGINALE | "Kubernetes", "Docker", "PostgreSQL" |
| **Normative References** | Mantieni ACRONIMO italiano | "CAD (Codice Amministrazione Digitale) art.20" |

---

## SEZIONE 13: CONSISTENCY CHECKLIST

Quando si aggiorna documentazione SP:
- [ ] Titoli SP usano traduzioni standardizzate
- [ ] Termine "workflow" è coerente
- [ ] JSON mantiene chiavi in inglese
- [ ] Acronimi tecnici (API, RBAC) non sono tradotti
- [ ] Normativa italiana (CAD, GDPR) è corretta
- [ ] Cross-references usano titoli ufficiali

---

## SEZIONE 14: VERSION CONTROL

| Versione | Data | Modifiche |
|----------|------|-----------|
| 1.0 | 2025-11-19 | Creazione iniziale. 50+ termini mappati. |

---

**FINE GLOSSARIO**

*Per domande o suggerimenti su termini non coperti, contattare Tech Writing Team.*

