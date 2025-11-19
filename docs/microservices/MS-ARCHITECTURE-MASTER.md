# Microservizi ZenIA - Navigazione Rapida

> **Quick Links**: [Trova il tuo MS](#microservizi-disponibili) | [Flow UC5](#flusso-uc5) | [Pattern Dati](#pattern-dati)

## 🚀 Per Developer - Inizia Qui

### Se devi implementare un feature:
1. **Scopri quale MS** → Vedi tabella sotto
2. **Clicca il link** → Vai a [MS01-CLASSIFIER/README.md](MS01-CLASSIFIER/README.md)
3. **Segui 5 passi** → Setup locale (5 min) → API (10 min) → Code (30 min) → Test (10 min) → Deploy (10 min)

**Tempo totale: ~70 minuti da zero a deployment**

👉 **[Workflow Operativo Completo](DEVELOPER-WORKFLOW.md)** ← Apri questo quando inizi!

---

## Microservizi Disponibili

| MS | Nome | Ruolo Primario | Copertura UC | Tecnologie | Documentazione |
|----|------|----------------|--------------|------------|-----------------|
| **MS01** | CLASSIFIER | Classificazione documenti | UC5, UC6, UC7 | Python, scikit-learn, FastAPI, PostgreSQL | [📂 Vedi MS01](MS01-CLASSIFIER/README.md) |
| **MS02** | ANALYZER | Analisi contenuto & NLP | UC5, UC6, UC7, UC11 | Python, spaCy, NLTK, FastAPI | [📂 Vedi MS02](MS02-ANALYZER/README.md) |
| **MS03** | ORCHESTRATOR | Orchestrazione workflow | UC5, UC6, UC7, UC9 | Python, Apache NiFi, FastAPI | [📂 Vedi MS03](MS03-ORCHESTRATOR/README.md) |
| **MS04** | VALIDATOR | Validazione dati | UC5, UC6, UC7 | Python, JSON Schema, FastAPI | [📂 Vedi MS04](MS04-VALIDATOR/README.md) |
| **MS05** | TRANSFORMER | Trasformazione dati | UC5, UC6, UC7 | Python, Pandas, FastAPI | [📂 Vedi MS05](MS05-TRANSFORMER/README.md) |
| **MS06** | AGGREGATOR | Aggregazione dati | UC7, UC11 | Python, Apache Spark, FastAPI | [📂 Vedi MS06](MS06-AGGREGATOR/README.md) |
| **MS07** | DISTRIBUTOR | Distribuzione contenuti | UC5, UC6, UC7 | Python, RabbitMQ, FastAPI | [📂 Vedi MS07](MS07-DISTRIBUTOR/README.md) |
| **MS08** | MONITOR | Monitoraggio & salute | Tutti gli UC | Python, Prometheus, Grafana | [📂 Vedi MS08](MS08-MONITOR/README.md) |
| **MS09** | MANAGER | Gestione risorse | Tutti gli UC | Python, Kubernetes, FastAPI | [📂 Vedi MS09](MS09-MANAGER/README.md) |
| **MS10** | LOGGER | Logging centralizzato | Tutti gli UC | Python, ELK Stack, FastAPI | [📂 Vedi MS10](MS10-LOGGER/README.md) |
| **MS11** | GATEWAY | API gateway | Tutti gli UC | Java/Go, Kong, Nginx | [📂 Vedi MS11](MS11-GATEWAY/README.md) |
| **MS12** | CACHE | Cache distribuito | Tutti gli UC | Redis, Memcached | [📂 Vedi MS12](MS12-CACHE/README.md) |
| **MS13** | SECURITY | Sicurezza & crittografia | Tutti gli UC | Python, Vault, FastAPI | [📂 Vedi MS13](MS13-SECURITY/README.md) |
| **MS14** | AUDIT | Audit & compliance | Tutti gli UC | Python, Elasticsearch, FastAPI | [📂 Vedi MS14](MS14-AUDIT/README.md) |
| **MS15** | CONFIG | Gestione configurazione | Tutti gli UC | Spring Cloud Config, Etcd | [📂 Vedi MS15](MS15-CONFIG/README.md) |
| **MS16** | REGISTRY | Service discovery | Tutti gli UC | Consul, Eureka | [📂 Vedi MS16](MS16-REGISTRY/README.md) |

---

## Flusso UC5

### UC5 - Produzione Documentale Integrata
- **MS Coinvolti**: MS01, MS02, MS03, MS04, MS05, MS07, MS08, MS11, MS13, MS14
- **Flusso**: Email → MS01(classifica) → MS02(analizza) → MS03(orchestra) → Pipeline SP → MS07(distribuisci) → Output

---

## Pattern Dati

### Pattern 1: Sincrono Request-Response
```
Client → MS11(Gateway) → MS01/MS02/MS04 → Response → Client
Latenza: < 500ms
Caso d'uso: Classificazione iniziale UC5, validazione UC6
```

### Pattern 2: Asincrono Basato su Code
```
Client → MS07(Distributor) → RabbitMQ → Worker MS → Completamento
Latenza: Asincrona, consistenza finale
Caso d'uso: Ingestion archivio UC7, reporting batch UC11
```

### Pattern 3: Stream Processing
```
Sorgente → Kafka Topic → MS02/MS05/MS06 → Sink
Latenza: Real-time, < 1 secondo
Caso d'uso: Monitoraggio UC9, flusso dati continuo
```

---

## Struttura Cartelle (per ogni MS)

Ogni microservizio contiene:
- **README.md** → Quick start (5 min)
- **SPECIFICATION.md** → Architettura e design (30 min)
- **API.md** → Endpoint e payload
- **DATABASE-SCHEMA.md** → Schema database
- **docker-compose.yml** → Setup locale
- **kubernetes/** → Deployment manifests
- **examples/** → Request/response examples

---

## Per Approfondire

**Dettagli architettura completa** → [ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
**Guida sviluppatore** → [DEVELOPMENT-GUIDE.md](../DEVELOPMENT-GUIDE.md)
**Documentazione structure** → [DOCUMENTATION-STRUCTURE-GUIDE.md](../DOCUMENTATION-STRUCTURE-GUIDE.md)

---
