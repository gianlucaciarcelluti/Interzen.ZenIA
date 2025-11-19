# Template Standard - Conformità Normativa SP

**Versione**: 1.0
**Data**: 2025-11-19
**Scopo**: Template standardizzato per documentare conformità normativa in ogni Sottoprogetto (SP)

---

## 📋 ISTRUZIONI PER L'USO

Questo template definisce la struttura standard per la sezione **"Conformità Normativa"** in ogni SP. Ogni SP DEVE includere questa sezione con i requisiti applicabili.

### Come usare questo template:

1. **Copiare questa sezione** nel vostro SP (prima della sezione "Roadmap Evoluzione")
2. **Selezionare i framework normativi applicabili** da quelli elencati sotto
3. **Per ogni framework**: includere solo gli articoli/requisiti rilevanti per lo specifico SP
4. **Aggiungere riferimenti diretti** ai capitoli di implementazione del SP che soddisfano il requisito
5. **Includere link** a COMPLIANCE-MATRIX.md per la tracciabilità completa

---

## 🏛️ CONFORMITÀ NORMATIVA

### Framework Normativi Applicabili

```
[Selezionare uno o più]:
☐ L. 241/1990 - Procedimento Amministrativo
☐ CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale)
☐ D.Lgs 152/2006 (Codice dell'Ambiente)
☐ D.Lgs 42/2004 (Codice Beni Culturali)
☐ D.Lgs 33/2013 (Decreto Trasparenza)
☐ GDPR - Regolamento 2016/679
☐ eIDAS - Regolamento 2014/910
☐ AI Act - Regolamento 2024/1689
☐ PNRR - Modalità esecuzione PNRR
☐ Linee Guida AGID
```

---

## 📌 TEMPLATE PER CONFORMITÀ NORMATIVA

### L. 241/1990 - Procedimento Amministrativo

**Applicabilità**: [SÌ / NO - Se SÌ, aggiungere articoli rilevanti]

| Articolo | Requisito | Implementazione SP | Riferimento | Status |
|----------|-----------|------------------|-------------|--------|
| Art. 1 | Trasparenza | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 3 | Economicità & Efficacia | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 6 | Garanzie procedurali | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 7 | Competenze istituzionali | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 15 | Silenzio assenso | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 23 | Comunicazione scritta | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 24 | Diritti accesso | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 27 | Motivazione | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |

**Microservizi Correlati**: MS14-AUDIT, MS10-LOGGER, MS03-ORCHESTRATOR, MS07-DISTRIBUTOR, MS16-REGISTRY, MS15-CONFIG, MS02-ANALYZER

---

### CAD - D.Lgs 82/2005 (Codice dell'Amministrazione Digitale)

**Applicabilità**: [SÌ / NO - Se SÌ, aggiungere articoli rilevanti]

| Articolo | Requisito | Implementazione SP | Riferimento | Status |
|----------|-----------|------------------|-------------|--------|
| Art. 1 | Digital-first | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 2 | Interoperabilità | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 3 | Accessibilità | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 21 | Documenti elettronici | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 22 | Firma digitale | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 23 | Marcatura temporale | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 41 | Conservazione dati | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 62 | Standard metadati | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |

**Microservizi Correlati**: MS11-GATEWAY, MS02-ANALYZER, MS16-REGISTRY, MS07-DISTRIBUTOR, MS01-CLASSIFIER, MS04-VALIDATOR, MS13-SECURITY, MS05-TRANSFORMER, MS06-AGGREGATOR

---

### GDPR - Regolamento 2016/679 (Protezione Dati Personali)

**Applicabilità**: [SÌ / NO - Se SÌ, aggiungere articoli rilevanti]

| Articolo | Requisito | Implementazione SP | Riferimento | Status |
|----------|-----------|------------------|-------------|--------|
| Art. 5 | Legittimità & lealtà | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 12 | Trasparenza | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 15 | Diritto accesso | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 17 | Diritto cancellazione | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 20 | Portabilità dati | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 22 | Decisioni automatizzate | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 32 | Integrità & confidenzialità | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 33-34 | Notifica violazione | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 35 | DPIA | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 37 | DPO | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |

**Microservizi Correlati**: MS13-SECURITY, MS14-AUDIT, MS05-TRANSFORMER, MS08-MONITOR, MS02-ANALYZER

**Nota Importante**: GDPR applica a tutti gli SP che processano dati personali. Verificare applicabilità con il Data Protection Officer (DPO).

---

### eIDAS - Regolamento 2014/910 (Firma Digitale)

**Applicabilità**: [SÌ / NO - Se SÌ, aggiungere articoli rilevanti]

| Articolo | Requisito | Implementazione SP | Riferimento | Status |
|----------|-----------|------------------|-------------|--------|
| Art. 3 | Firma elettronica | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 13 | Firma avanzata | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 24 | Servizi marca temporale | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 32 | Validazione long-term | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |

**Microservizi Correlati**: MS13-SECURITY, MS04-VALIDATOR

**Formati Supportati**: XAdES (XML), PAdES (PDF), CAdES (CMS)

---

### AI Act - Regolamento 2024/1689 (Intelligenza Artificiale)

**Applicabilità**: [SÌ / NO - Se contiene modelli AI, aggiungere articoli rilevanti]

| Articolo | Requisito | Implementazione SP | Riferimento | Status |
|----------|-----------|------------------|-------------|--------|
| Art. 6 | Valutazione rischio | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 8 | Compliance | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 13 | Trasparenza | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |
| Art. 22 | Supervisione umana | [Descrizione] | [Link a sezione SP] | ✅ / 🔄 / ❌ |

**Microservizi Correlati**: MS02-ANALYZER, MS14-AUDIT

**Modelli AI Utilizzati**: [Elencare BERT, spaCy, DistilBERT, GPT-based models, ecc.]

**Human-in-the-Loop**: [SÌ / NO] - Descrizione meccanismo di supervisione umana

---

## ✅ CHECKLIST DI CONFORMITÀ

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle implementazioni SP
- [ ] Riferimenti incrociati a sezioni SP specifiche forniti
- [ ] Status di implementazione (✅/🔄/❌) indicato per ogni articolo
- [ ] Microservizi correlati (MS) identificati
- [ ] Link a COMPLIANCE-MATRIX.md aggiunto
- [ ] DPIA completata (se applicabile GDPR)
- [ ] Documentazione modelli AI completata (se applicabile AI Act)
- [ ] Validazione compliance eseguita da compliance expert
- [ ] Data ultimo review conformità registrata

---

## 📊 MATRICE DI COMPLIANCE RIASSUNTIVA

| Framework | Status | Articoli | Implementazioni | Risk Level | Review Date |
|-----------|--------|----------|-----------------|------------|-------------|
| L. 241/1990 | [Compliant/Partial/Non-Compliant] | [N] | [Elenco MS/SP] | [Low/Medium/High] | [YYYY-MM-DD] |
| CAD | [Compliant/Partial/Non-Compliant] | [N] | [Elenco MS/SP] | [Low/Medium/High] | [YYYY-MM-DD] |
| GDPR | [Compliant/Partial/Non-Compliant] | [N] | [Elenco MS/SP] | [Low/Medium/High] | [YYYY-MM-DD] |
| eIDAS | [Compliant/Partial/Non-Compliant] | [N] | [Elenco MS/SP] | [Low/Medium/High] | [YYYY-MM-DD] |
| AI Act | [Compliant/Partial/Non-Compliant] | [N] | [Elenco MS/SP] | [Low/Medium/High] | [YYYY-MM-DD] |

---

## 🔗 RIFERIMENTI CORRELATI

- **COMPLIANCE-MATRIX.md**: Mapping completo normative → MS/SP
- **GLOSSARIO-TERMINOLOGICO.md**: Definizioni termini conformità
- **GDPR-DPIA-TEMPLATE.md**: Template DPIA (se applicabile)
- **AI-RISK-ASSESSMENT-TEMPLATE.md**: Template valutazione rischio AI
- **docs/GOVERNANCE**: Processi approvazione conformità

---

## 📝 NOTE IMPORTANTI

### Quando compilare questo template:

1. **Nella creazione iniziale di un nuovo SP**
2. **Quando le normative cambiano** (es. nuove versioni del CAD, AI Act aggiornato)
3. **Durante la revisione annuale** della documentazione SP
4. **Prima di implementare nuove funzionalità** che potrebbero avere implicazioni normative

### Chi compila:

- **Technical Writer**: Struttura iniziale e documentazione tecnica
- **Compliance Expert**: Validazione conformità articoli/requisiti
- **Legal Team**: Approvazione finale conformità e interpretazione normativa
- **Architecture Team**: Validazione mapping MS/SP

### Rischi di non-conformità:

| Rischio | Impatto | Mitigation |
|--------|--------|-----------|
| Violazione normativa | Alto | Review trimestrale compliance |
| Audit fallito | Alto | Documentazione tracciabile con evidence |
| Contenzioso legale | Critico | Supervisione legal team |
| Multa GDPR | Critico | DPIA + Privacy by design |

---

## 🔄 STORICO REVIEW CONFORMITÀ

| Data | Versione | Revisore | Articoli Aggiunti | Articoli Rimossi | Note |
|------|----------|----------|------------------|-----------------|------|
| [YYYY-MM-DD] | 1.0 | [Nome] | [Elenco] | [Elenco] | Creazione iniziale |
| | | | | | |

---

## 📞 CONTATTI COMPLIANCE

- **Data Protection Officer (DPO)**: [Email/Contatto]
- **Legal Team**: [Email/Contatto]
- **Compliance Manager**: [Email/Contatto]
- **Architecture Lead**: [Email/Contatto]

---

**Approvato da**: Compliance & Legal Team
**Versione**: 1.0 (19 novembre 2025)
**Prossima Review**: 19 dicembre 2025 o quando normative cambiano
