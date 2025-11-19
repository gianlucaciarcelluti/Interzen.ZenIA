# Piattaforma ZenIA - Panoramica dell'Architettura

Benvenuti nella documentazione tecnica completa dell'architettura della piattaforma ZenIA per la gestione intelligente dei documenti e l'analisi dei dati.

---

## 📋 Struttura della Documentazione

### Microservizi (16 servizi core)
Ubicati in `docs/microservices/`:
- **[MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)** - Matrice comparativa microservizi e integrazione
- **Cartelle MS01-MS16** - Documentazione individuale di ogni microservizio con:
  - README.md (quick start 5 minuti)
  - SPECIFICATION.md (approfondimento tecnico 30 minuti)
  - API.md (riferimento API e esempi)
  - DATABASE-SCHEMA.md (diagrammi ER in Mermaid + script SQL separati)
  - TROUBLESHOOTING.md (problemi comuni e soluzioni)
  - docker-compose.yml (setup development locale)
  - kubernetes/ (manifesti deployment Kubernetes)
  - examples/ (esempi JSON request/response)

### Casi d'Uso (11 workflow completi)
Ubicati in `docs/use_cases/`:
- UC1-UC11 copertura di tutti i processi business
- Ogni UC include:
  - Overview processo e diagrammi di flusso
  - Modelli dati e esempi payload
  - Raggruppamenti SP (Sub-Project)
  - Matrici di dipendenza
  - Mapping compliance normativa

### Governance e Configurazione
Ubicati in `docs/`:
- [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) - Design di sistema e livelli
- [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) - Workflow sviluppo e best practice
- [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md) - Fonti normative → mapping MS/SP
- [SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md) - Tutti i 72 mapping SP-to-MS

---

## 🏗️ Architettura di Sistema

### Livelli (da client a data)

```
┌─────────────────────────────────────────┐
│   Applicazioni Client (Web, Mobile)     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   MS11 - API Gateway & Autenticazione   │
│   - Rate limiting, routing, TLS        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────┐
│          Livello Elaborazione (MS01-MS07)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ MS01     │  │ MS02     │  │ MS03     │             │
│  │Classifier│→ │ Analyzer │→ │Orchestrat│             │
│  └──────────┘  └──────────┘  └──────┬───┘             │
│                                      │                 │
│                    ┌──────────────────┼──────────┐     │
│                    │                  │          │     │
│                ┌───▼──┐          ┌───▼──┐   ┌──▼───┐  │
│                │ MS04 │          │ MS05 │   │ MS06 │  │
│                │Validat│         │Transf│   │Aggreg│  │
│                └──────┘          └──────┘   └──────┘  │
│                    │                  │          │     │
│                    └──────────────────┼──────────┘     │
│                                      │                 │
│                            ┌─────────▼──────┐          │
│                            │ MS07 Distribut │          │
│                            └────────────────┘          │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│        Livello Infrastruttura e Cross-Cutting        │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │ MS08   │  │ MS09   │  │ MS10   │  │ MS12   │     │
│  │Monitor │  │Manager │  │ Logger │  │ Cache  │     │
│  └────────┘  └────────┘  └────────┘  └────────┘     │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │
│  │ MS13   │  │ MS14   │  │ MS15   │  │ MS16   │     │
│  │Security│  │ Audit  │  │ Config │  │Registry│     │
│  └────────┘  └────────┘  └────────┘  └────────┘     │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│  Livello Dati (PostgreSQL, Redis, S3, ELK)          │
└──────────────────────────────────────────────────────┘
```

---

## 🎯 Microservizi Chiave

| Servizio | Ruolo | Stack Tecnologico | UC |
|---------|-------|-------------------|-----|
| **MS01-CLASSIFIER** | Rilevamento tipo documento | Python, scikit-learn, PostgreSQL | UC5, UC6, UC7 |
| **MS02-ANALYZER** | Analisi contenuto & NLP | Python, spaCy, PostgreSQL | UC5, UC6, UC7, UC11 |
| **MS03-ORCHESTRATOR** | Gestione workflow | Python, Apache NiFi, FastAPI | UC5, UC6, UC7, UC9 |
| **MS04-VALIDATOR** | Validazione dati | Python, JSON Schema | UC5, UC6, UC7 |
| **MS05-TRANSFORMER** | Trasformazione dati | Python, Pandas | UC5, UC6, UC7 |
| **MS06-AGGREGATOR** | Consolidamento dati | Python, Apache Spark | UC7, UC11 |
| **MS07-DISTRIBUTOR** | Consegna contenuti | Python, RabbitMQ | UC5, UC6, UC7 |
| **MS08-MONITOR** | Monitoraggio | Python, Prometheus, Grafana | Tutti |
| **MS09-MANAGER** | Orchestrazione risorse | Python, Kubernetes | Tutti |
| **MS10-LOGGER** | Logging centralizzato | Python, ELK Stack | Tutti |
| **MS11-GATEWAY** | API gateway | Kong/Nginx | Tutti |
| **MS12-CACHE** | Layer caching | Redis, Memcached | Tutti |
| **MS13-SECURITY** | Sicurezza & crittografia | Python, Vault | Tutti |
| **MS14-AUDIT** | Tracking compliance | Python, Elasticsearch | Tutti |
| **MS15-CONFIG** | Gestione configurazione | Spring Cloud Config | Tutti |
| **MS16-REGISTRY** | Service discovery | Consul/Eureka | Tutti |

---

## 📊 Copertura Casi d'Uso

### Workflow Core (UC1-UC7)
1. **UC1** - Integrazione Email (Intake)
2. **UC2** - Classificazione Documento
3. **UC3** - Estrazione Metadati
4. **UC4** - Integrazione Knowledge Base
5. **UC5** - Produzione Documentale Integrata (Generazione Documenti)
6. **UC6** - Firma Digitale Integrata (Firma Digitale)
7. **UC7** - Conservazione Digitale (Archivio Digitale)

### Funzionalità Avanzate (UC8-UC11)
8. **UC8** - Estrazione Dati Intelligente
9. **UC9** - Workflow Automatizzato
10. **UC10** - Supporto Utente & Gestione Ticket
11. **UC11** - Analisi Dati & Reporting

---

## 🔌 Pattern di Integrazione

### Sincrono (Request-Response)
```
Client → MS11 Gateway → MS01/02/04 → Response
Latenza: < 500ms
Uso: Classificazione real-time, validazione
```

### Asincrono (Queue-Based)
```
Client → MS07 Distributor → RabbitMQ → Worker
Latenza: Eventual consistency
Uso: Elaborazione batch, archive ingestion
```

### Stream Processing
```
Kafka Topic → MS02/05/06 Processor → Sink
Latenza: Real-time (< 1sec)
Uso: Analytics continuo, monitoraggio
```

---

## 📦 Deployment

### Tecnologia Container
- **Immagini Base**: python:3.10-slim, openjdk:17-slim
- **Orchestrazione Container**: Kubernetes (K8s)
- **Registry**: Docker Hub / Registry Privato
- **Networking**: Service mesh (Istio) opzionale

### Setup Kubernetes
```yaml
Namespace: zendata
Replicas: 3+ per servizio (Alta Disponibilità)
Auto-scaling: HPA basato su CPU/Memory
Monitoring: Prometheus + Grafana
Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
```

### Development Locale
```bash
# Avviare tutti i servizi con Docker Compose
docker-compose up -d

# Accesso ai servizi
- Classifier API: http://localhost:8001
- Database: localhost:5432
- Redis Cache: localhost:6379
- pgAdmin: http://localhost:5050
```

---

## 🔐 Sicurezza

### Autenticazione & Autorizzazione
- **Metodo**: JWT (RS256 signing)
- **Issuer**: MS13-SECURITY (Vault integration)
- **RBAC**: Controllo accesso granulare basato su ruoli
- **Scopes**: Permessi a livello di risorsa

### Protezione Dati
- **In Transito**: TLS 1.3 (HTTPS enforced)
- **At Rest**: Crittografia AES-256
- **Secrets**: Kubernetes Secrets + HashiCorp Vault
- **Compliance**: GDPR, eIDAS, PCI-DSS, HIPAA

### Audit & Compliance
- **Logging Centralizzato**: MS10 + MS14 (Elasticsearch)
- **Audit Trail Immutabile**: Write-Once-Read-Many (WORM)
- **Retention**: 5-7 anni (requisito compliance)
- **Monitoring**: Real-time alerting su attività sospette

---

## 📈 Performance SLA

| Metrica | Target | Note |
|--------|--------|-------|
| API Latency (p95) | < 500ms | Gateway + elaborazione |
| Throughput | 1000+ req/sec | Horizontally scalabile |
| Disponibilità | 99.95% | Setup alta disponibilità |
| Cache Hit Rate | > 75% | Layer Redis |
| Database Response | < 50ms | Query optimization |

---

## 🧪 Strategia Testing

### Livelli Test
- **Unit Tests**: 70%+ coverage (pytest)
- **Integration Tests**: Docker Compose + PostgreSQL
- **E2E Tests**: Ambiente sandbox Kubernetes
- **Load Tests**: k6, locust, Apache JMeter

### Pipeline CI/CD
1. **Build**: Creazione immagine Docker
2. **Test**: Tutti i test suite
3. **Push**: Push in registry su main branch
4. **Deploy**: Rolling update in staging
5. **Validate**: Smoke tests in staging
6. **Release**: Deployment in produzione

---

## 📚 Come Iniziare

### Per Sviluppatori
1. **Inizia qui**: Leggi [README.md](microservices/MS01-CLASSIFIER/README.md) per MS01
2. **Setup**: Esegui `docker-compose up` nella cartella MS01
3. **Impara**: Rivedi SPECIFICATION.md per dettagli tecnici
4. **Sviluppa**: Segui DEVELOPMENT-GUIDE.md

### Per Architetti
1. **Panoramica**: Questo file (ARCHITECTURE-OVERVIEW.md)
2. **Riferimento Master**: [MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)
3. **Dipendenze**: Rivedi matrici di dipendenza UC-specifiche
4. **Compliance**: Controlla [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)

### Per Operations
1. **Kubernetes**: Rivedi cartelle kubernetes/ in ogni MS
2. **Monitoring**: Accedi dashboard Prometheus/Grafana
3. **Logs**: ELK Stack (Elasticsearch)
4. **Troubleshooting**: Vedi TROUBLESHOOTING.md in ogni MS

---

## 🔗 File Importanti

- **[MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)** - Matrice microservizi
- **[SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md)** - Tutti i 72 mapping SP-to-MS
- **[COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)** - Fonti normative
- **[DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md)** - Workflow sviluppo

---

## 💡 Concetti Chiave

### Microservizi (MS01-MS16)
- Servizi generici e riusabili
- Deployabili indipendentemente
- Architettura multi-tenant
- Polyglot persistence (PostgreSQL, Redis, Elasticsearch)

### Sub-Progetti (SP01-SP72)
- Componenti business domain-specific
- Raggruppamento SP correlati sotto UC (Casi d'Uso)
- 72 progetti specializzati su 11 casi d'uso
- SP28 intentionally skipped

### Casi d'Uso (UC1-UC11)
- Processi business e workflow
- Coinvolgono multipli SP e MS
- Definiti da requisiti normativi
- Tracciabili a normative italiane/UE

---

## 🚀 Prossimi Passi

1. **Esplora MS01**: Inizia con microservizio Classifier
2. **Setup Locale**: Esegui `docker-compose up` per development
3. **Leggi Specs**: Approfondisci SPECIFICATION.md per dettagli
4. **Deploy**: Segui manifesti kubernetes/ per produzione
5. **Monitora**: Accedi dashboard per insights real-time

---

**Versione**: 1.0
**Ultimo Aggiornamento**: 2024-11-18
**Maintainers**: ZenIA Development Team
