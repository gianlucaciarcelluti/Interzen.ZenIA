# Matrice Dipendenze - UC2 Protocollo Informatico

## Matrice di Dipendenza Componenti

| Componente | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Descrizione |
|------------|------|------|------|------|------|------|------|-------------|
| **SP16 Classifier** | - | → | → | → | - | - | → | Classificazione iniziale corrispondenza |
| **SP17 Suggester** | ← | - | - | → | - | - | → | Suggerimenti protocollo/titolario |
| **SP18 Anomaly Detector** | ← | ← | - | → | - | - | → | Rilevamento anomalie |
| **SP19 Orchestrator** | ← | ← | ← | - | → | → | → | Orchestrazione workflow |
| **SP02 Document Processor** | - | - | - | ← | - | - | - | Elaborazione documenti |
| **SP07 Metadata Extractor** | - | - | - | ← | - | - | - | Estrazione metadata avanzati |
| **SP10 Dashboard** | ← | ← | ← | ← | - | - | - | Interfaccia utente |

**Legenda:**
- → : Dipendenza diretta (richiede output)
- ← : Dipendenza inversa (fornisce input)
- - : Nessuna dipendenza diretta

## Matrice Tecnologica

| Tecnologia | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Versione |
|------------|------|------|------|------|------|------|------|----------|
| **Python** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 3.11 |
| **FastAPI** | - | - | - | ✓ | ✓ | ✓ | ✓ | 0.104 |
| **PostgreSQL** | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | 15 |
| **Redis** | ✓ | ✓ | - | ✓ | - | - | ✓ | 7.2 |
| **Kafka** | - | - | ✓ | ✓ | - | - | - | 3.6 |
| **Elasticsearch** | ✓ | - | - | - | ✓ | ✓ | - | 8.11 |
| **Docker** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 24.0 |
| **Kubernetes** | - | - | - | ✓ | - | - | ✓ | 1.28 |

**Legenda:**
- ✓ : Utilizzata direttamente
- - : Non utilizzata

## Matrice di Sicurezza

| Aspetto Sicurezza | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Implementazione |
|-------------------|------|------|------|------|------|------|------|----------------|
| **Autenticazione** | JWT | JWT | JWT | JWT | JWT | JWT | OAuth2 | Token-based |
| **Autorizzazione** | RBAC | RBAC | RBAC | RBAC | RBAC | RBAC | RBAC | Role-based |
| **Crittografia** | TLS 1.3 | TLS 1.3 | TLS 1.3 | TLS 1.3 | TLS 1.3 | TLS 1.3 | TLS 1.3 | End-to-end |
| **Audit Logging** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ELK Stack |
| **Data Masking** | - | - | ✓ | - | ✓ | ✓ | ✓ | Pattern-based |
| **Rate Limiting** | - | - | ✓ | ✓ | - | - | ✓ | Token bucket |

## Matrice di Scalabilità

| Metrica | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Target |
|---------|------|------|------|------|------|------|------|--------|
| **Throughput** | 100 req/s | 200 req/s | 50 req/s | 500 req/s | 100 req/s | 100 req/s | 1000 req/s | Massimo |
| **Latency** | <500ms | <300ms | <1s | <2s | <1s | <2s | <100ms | Medio |
| **Availability** | 99.9% | 99.9% | 99.5% | 99.9% | 99.9% | 99.9% | 99.9% | SLA |
| **Scalability** | Horizontal | Horizontal | Horizontal | Horizontal | Horizontal | Horizontal | Horizontal | Tipo |

## Matrice di Monitoraggio

| Metriche | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Tool |
|-----------|------|------|------|------|------|------|------|------|
| **Performance** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Prometheus |
| **Errors** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Prometheus |
| **Business KPIs** | ✓ | ✓ | ✓ | ✓ | - | - | ✓ | Custom |
| **Health Checks** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Kubernetes |
| **Logs** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ELK Stack |
| **Traces** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Jaeger |

## Matrice di Deployment

| Ambiente | SP16 | SP17 | SP18 | SP19 | SP02 | SP07 | SP10 | Config |
|----------|------|------|------|------|------|------|------|--------|
| **Development** | Docker | Docker | Docker | Docker | Docker | Docker | Docker | docker-compose |
| **Staging** | K8s | K8s | K8s | K8s | K8s | K8s | K8s | Helm |
| **Production** | K8s | K8s | K8s | K8s | K8s | K8s | K8s | Helm + Istio |
| **CI/CD** | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | GitHub Actions | Pipeline |

## Rischi e Mitigazioni

### Dipendenze Critiche
- **SP19 Orchestrator**: Punto singolo di fallimento
  - **Mitigazione**: High availability, circuit breaker

### Bottlenecks Potenziali
- **Database PostgreSQL**: Contention su titolario
  - **Mitigazione**: Read replicas, caching avanzato

### Failure Scenarios
- **SP18 Anomaly Detector down**: Perdita rilevamento frodi
  - **Mitigazione**: Fallback rule-based, alert monitoring

### Performance Issues
- **SP16 Classification**: Alta latenza ML inference
  - **Mitigazione**: GPU acceleration, model optimization</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/02 Matrice Dipendenze.md