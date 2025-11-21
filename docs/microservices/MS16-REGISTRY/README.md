# MS16-REGISTRY - Microservice

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-21
**Owner**: Architecture Team

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)

---

## Avvio Rapido (5 minuti)

### Che cos'è MS16-REGISTRY?
MS16-REGISTRY fornisce service discovery centralizzato e PDND integration per la piattaforma ZenIA, con conformità a Piano Triennale e CAD.

### Responsabilità principali
- **Service Discovery**: Registrazione e discovery dinamica di microservizi
- **PDND Integration**: Interoperabilità con Piattaforma Dati Nazionale
- **Anagrafe Management**: Gestione anagrafi pubbliche (comuni, enti)
- **Data Catalog**: Catalogazione dataset e servizi
- **API Registry**: Registrazione endpoint API pubblici
- **Audit Trail**: Logging per GDPR compliance

### Primi passi
1. Consulta [SPECIFICATION.md](SPECIFICATION.md) per le specifiche tecniche dettagliate
2. Controlla `docker-compose.yml` per il setup locale
3. Rivedi [API.md](API.md) per gli endpoint di integrazione
4. Esplora la cartella [examples/](examples/) per esempi di request/response

### Stack tecnologico
- **Linguaggio**: Python 3.10+
- **API**: FastAPI (OpenAPI 3.0)
- **Database**: PostgreSQL (PDND-compatible schema)
- **Cache**: Redis
- **Integration**: PDND, Anagrafe, DCAT-AP

### Dipendenze
Vedi [SPECIFICATION.md](SPECIFICATION.md) per i dettagli sulle dipendenze.

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ Piano Triennale AgID 2024-2026 (Cap. 3 & 4)
- ☑ CAD (Codice dell'Amministrazione Digitale)
- ☑ GDPR (Regolamento 2016/679)
- ☑ PNRR (Componente data sharing)
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

### 📚 Conformità Piano Triennale AgID 2024-2026

#### Capitolo 3: Servizi (PDND & Data Sharing)

| Requisito | Implementazione MS16 | Status |
|---|---|---|
| **PDND Integration** | API conformi PDND standard | ✅ |
| **Data sharing** | Managed dataset catalog | ✅ |
| **Anagrafe** | Registry per comuni/enti PA | ✅ |
| **Interoperabilità** | OpenAPI 3.0 standard | ✅ |
| **Dataset discovery** | DCAT-AP metadata | ✅ |

#### Capitolo 4: Piattaforme Digitali (Anagrafi & Registries)

| Piattaforma | Implementazione MS16 | Details |
|---|---|---|
| **Anagrafe Nazionale** | Registry per gestione anagrafi PA | ✅ |
| **PDND** | Data sharing platform integration | ✅ |
| **API Portal** | Registry per endpoint pubblici | ✅ |

### 🛡️ Conformità CAD (D.Lgs 82/2005)

| Articolo | Requisito | Implementazione MS16 |
|---|---|---|
| **Art. 2** | Interoperabilità | API standard PDND-compatible |
| **Art. 60** | Dati delle PA | Anagrafe registry per PA |
| **Art. 62** | Standard metadati | DCAT-AP per dataset |

### 🔐 Conformità GDPR (Data Protection)

| Principio | Implementazione MS16 | Meccanismo |
|---|---|---|
| **Transparency** | Dataset catalog public | DCAT-AP metadata |
| **Data minimization** | Only necessary fields in registry | Schema design |
| **Purpose limitation** | Role-based access to registry | RBAC per endpoint |
| **Integrity** | Hash validation per record | Checksum verification |
| **Confidentiality** | TLS 1.3 per API calls | Encryption in transit |
| **Accountability** | Audit trail per data access | Logging all queries |

---

## ✅ Checklist Conformità Pre-Deployment

### Piano Triennale Cap 3 - PDND & Data Sharing

- [ ] PDND API endpoint implementato (data exchange)
- [ ] PDND schema compliance verificato
- [ ] Dataset catalog operational (discovery)
- [ ] Anagrafe registry for PA configurato
- [ ] Data sharing agreements documented
- [ ] Metadata DCAT-AP compliant
- [ ] API versioning per PDND compatibility
- [ ] Service registration workflow tested

### Piano Triennale Cap 4 - Anagrafi & Registries

- [ ] Anagrafe Nazionale registry setup
- [ ] Commons/entities managed
- [ ] API endpoint discovery
- [ ] Registry health checks operational
- [ ] Service catalog up-to-date
- [ ] Metadata completeness verified

### CAD - Interoperability & Data Management

- [ ] PDND API standard compliance verified
- [ ] PA data registry operational
- [ ] DCAT-AP metadata standard implemented
- [ ] API documentation OpenAPI 3.0
- [ ] Data integrity validation active
- [ ] Access control logging enabled

### GDPR - Data Protection & Transparency

- [ ] Dataset catalog transparency (public metadata)
- [ ] Data minimization in registry fields
- [ ] Role-based access control per API consumer
- [ ] Hash validation per record integrity
- [ ] TLS 1.3 for all API communication
- [ ] Audit trail per data access
- [ ] Data retention policy implemented
- [ ] Privacy assessment completed

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] PDND integration compliance audit
- [ ] Dataset catalog completeness verified
- [ ] Anagrafe data accuracy check
- [ ] API endpoint availability validated
- [ ] DCAT-AP metadata standard review
- [ ] Service registration effectiveness
- [ ] GDPR data access audit
- [ ] Registry performance benchmarked
- [ ] Security certificate renewal verified
- [ ] Compliance report generated

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
