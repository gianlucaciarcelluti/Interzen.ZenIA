# Guida allo Sviluppo ZenIA

Guida completa per sviluppatori che lavorano sulla piattaforma ZenIA.

---

## 🎯 Prima di Iniziare

### Prerequisiti
- Docker & Docker Compose (per development locale)
- Python 3.10+
- Client PostgreSQL
- Accesso Git & GitHub
- Conoscenza Kubernetes (per deployment produzione)

### File Importanti
- Inizia qui: [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md)
- Matrice microservizi: [MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)
- Requisiti compliance: [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)

---

## 🚀 Setup Development Locale

### 1. Clona e Esplora
```bash
cd /path/to/ZenIA
git clone <repo-url>

# Naviga a un microservizio
cd docs/microservices/MS01-CLASSIFIER
```

### 2. Avvia con Docker Compose
```bash
# Avviare tutti i servizi (Classifier, PostgreSQL, Redis)
docker-compose up -d

# Verifica che i servizi siano running
docker-compose ps

# Vedi i log
docker-compose logs -f classifier
```

### 3. Controlla Salute Servizio
```bash
# Classification API
curl http://localhost:8001/health

# Risposta dovrebbe mostrare:
# {"status": "healthy", "service": "MS01-CLASSIFIER", ...}
```

### 4. Testa Endpoint API
```bash
# Classifica un documento
curl -X POST http://localhost:8001/api/v1/classify \
  -H "Content-Type: application/json" \
  -d @examples/request.json

# Controlla i modelli
curl http://localhost:8001/api/v1/models/status
```

---

## 📖 Gerarchia Documentazione

### Per Qualsiasi Microservizio (MS01-MS16)

1. **README.md** (5 minuti)
   - Cos'è il servizio
   - Comandi quick start
   - Responsabilità principali
   - Stack tecnologico

2. **SPECIFICATION.md** (30 minuti)
   - Architettura dettagliata
   - Descrizione componenti
   - Performance SLA
   - Punti integrazione

3. **API.md** (Riferimento)
   - Documentazione completa endpoint
   - Schemi request/response
   - Codici errore
   - Rate limiting

4. **DATABASE-SCHEMA.md** (Riferimento)
   - Diagrammi ER (Mermaid)
   - Descrizione tabelle
   - Strategia indici
   - Procedure backup/recovery

5. **TROUBLESHOOTING.md** (Quando sorgono problemi)
   - Problemi comuni
   - Procedure diagnostica
   - Soluzioni
   - Strategie prevenzione

6. **docker-compose.yml** (Development Locale)
   - Tutti i servizi in un file
   - Configurazione ambiente
   - Gestione volumi
   - Setup networking

7. **kubernetes/** (Deployment Produzione)
   - deployment.yaml
   - service.yaml
   - configmap.yaml
   - Regole HPA/PDB

8. **examples/** (Testing)
   - request.json
   - response.json
   - Payload di esempio

---

## 🛠️ Task Development Comuni

### Task 1: Comprendere un Microservizio
```bash
1. Leggi: docs/microservices/MS01-CLASSIFIER/README.md
2. Esegui: docker-compose up -d
3. Testa: curl http://localhost:8001/health
4. Approfondisci: Leggi SPECIFICATION.md
```

### Task 2: Aggiungere un Nuovo Endpoint
```bash
# 1. Rivedi API.md per pattern esistenti
# 2. Aggiorna SPECIFICATION.md con dettagli nuovo endpoint
# 3. Aggiungi a docker-compose.yml se necessario
# 4. Aggiorna examples/ con esempi request/response
# 5. Testa con curl o Postman
# 6. Aggiorna API.md con documentazione completa
```

### Task 3: Cambiamenti Schema Database
```bash
# 1. Rivedi DATABASE-SCHEMA.md diagramma ER
# 2. Aggiorna init-schema.sql con nuova tabella/colonne
# 3. Testa con: psql -f init-schema.sql
# 4. Aggiorna DATABASE-SCHEMA.md diagramma ER
# 5. Aggiungi note migrazione al troubleshooting
```

### Task 4: Deploy su Kubernetes
```bash
# 1. Aggiorna versione immagine in kubernetes/deployment.yaml
# 2. Applica manifesti:
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/configmap.yaml

# 3. Monitora rollout:
kubectl rollout status deployment/ms01-classifier

# 4. Verifica salute:
curl http://ms01-classifier.zendata.local/health
```

---

## 🧪 Testing

### Unit Test
```bash
# Esegui pytest in microservizio Python
pytest tests/ --cov=./ --cov-report=html

# Target: 70%+ coverage
```

### Test Integrazione
```bash
# Avvia docker-compose con database di test
docker-compose -f docker-compose.test.yml up -d

# Esegui test integrazione
pytest tests/integration/

# Cleanup
docker-compose -f docker-compose.test.yml down
```

### Test API
```bash
# Usa Postman o curl con examples/
curl -X POST http://localhost:8001/api/v1/classify \
  -H "Content-Type: application/json" \
  -d @examples/request.json

# Valida response corrispondente a examples/response.json
```

---

## 📦 Build & Deployment

### Build Immagine Docker
```bash
# Build locale
docker build -t zendata/ms01-classifier:v1.0.0 .

# Tag e push
docker tag zendata/ms01-classifier:v1.0.0 registry/ms01-classifier:v1.0.0
docker push registry/ms01-classifier:v1.0.0
```

### Pipeline CI/CD
```
Code Push → GitHub → CI/CD Pipeline
  ├─ Build Docker image
  ├─ Esegui unit test (pytest)
  ├─ Esegui integration test
  ├─ Push su registry
  └─ Deploy su staging
```

### Deployment Kubernetes Manuale
```bash
# 1. Aggiorna deployment.yaml con versione immagine nuova
vi kubernetes/deployment.yaml

# 2. Applica cambiamenti
kubectl apply -f kubernetes/deployment.yaml

# 3. Monitora rollout
kubectl rollout status deployment/ms01-classifier -n zendata

# 4. Verifica salute
kubectl exec -it pod/ms01-classifier-xxx -- curl localhost:8001/health
```

---

## 🔍 Debugging

### Vedi Log
```bash
# Docker Compose
docker-compose logs -f classifier

# Kubernetes
kubectl logs -f deployment/ms01-classifier -n zendata
kubectl logs -f pod/ms01-classifier-xxx -n zendata --previous  # Pod crashato
```

### Accesso Database
```bash
# Docker Compose
docker-compose exec postgres psql -U classifier_service -d zenia_classifier

# Kubernetes
kubectl exec -it postgres-0 -- psql -U classifier_service -d zenia_classifier
```

### Controlla Ambiente
```bash
# Docker Compose
docker-compose exec classifier env | grep -i classifier

# Kubernetes
kubectl exec -it deployment/ms01-classifier -- env | grep -i classifier
```

---

## 📊 Ottimizzazione Performance

### Identifica Bottleneck
```bash
# Performance query database
kubectl exec -it postgres-0 -- psql -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Cache hit rate Redis
kubectl exec -it redis-0 -- redis-cli INFO stats | grep hit_rate

# Metriche applicazione
curl http://ms01-classifier:9090/metrics | grep -i latency
```

### Checklist Ottimizzazione
- [ ] Indici database ottimizzati (vedi DATABASE-SCHEMA.md)
- [ ] Cache hit rate > 75% (controlla TROUBLESHOOTING.md)
- [ ] API latency p95 < 500ms
- [ ] Memory usage < 80% dei limiti
- [ ] CPU usage < 70% sustained

---

## 🔐 Best Practice Sicurezza

### Gestione Secrets
```bash
# Crea Kubernetes secret per credenziali database
kubectl create secret generic classifier-db-secret \
  --from-literal=database-url="postgresql://user:pass@host:5432/db" \
  -n zendata

# Riferimento in deployment.yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: classifier-db-secret
        key: database-url
```

### Code Security
- Nessun secret nel code o file configurazione
- Usa .gitignore per file sensibili (.env, config/*.local.yml)
- Abilita code scanning in GitHub
- Esegui SAST tool (es. bandit per Python)

### Network Security
- TLS 1.3 enforced per tutta comunicazione esterna
- Network policies in Kubernetes
- API rate limiting (vedi API.md)
- CORS properly configured

---

## 📋 Guideline Commit & PR

### Commit Message
```
formato: <type>(<scope>): <subject>

type: feat, fix, docs, test, refactor, perf
scope: ms01-classifier, database, api, etc.
subject: Descrizione concisa (mood imperativo)

Esempio:
feat(ms01-classifier): Aggiungi batch classification endpoint
fix(database): Ottimizza indice document lookup
docs(api): Aggiorna sezione error handling
```

### Checklist Pull Request
- [ ] Code segue style guide
- [ ] Tutti test passano (unit + integration)
- [ ] Documentazione aggiornata
- [ ] CHANGELOG.md aggiornato
- [ ] Nessun secret o dato sensibile
- [ ] Database migration testata (se applicabile)

---

## 🚨 Troubleshooting

### Servizio non parte
1. Controlla log: `docker-compose logs classifier`
2. Verifica dipendenze: `docker-compose ps`
3. Controlla port conflict: `lsof -i :8001`
4. Vedi TROUBLESHOOTING.md per problemi comuni

### Errori connessione database
1. Verifica credenziali in .env o K8s secret
2. Controlla database è running: `docker-compose ps postgres`
3. Testa connessione: `psql -h localhost -U classifier_service`
4. Vedi DATABASE-SCHEMA.md per dettagli connessione

### API Timeout
1. Controlla log servizio per operazioni lente
2. Monitora performance query database
3. Controlla Redis cache hit rate
4. Rivedi metriche latency in Prometheus
5. Vedi TROUBLESHOOTING.md Issue #1 (Classification Timeout)

---

## 📚 Risorse Aggiuntive

### Documentazione Interna
- [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) - Design sistema
- [MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md) - Dettagli microservizi
- [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md) - Requisiti normativi
- [SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md) - Mapping business

### Risorse Esterne
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
- [Docker Documentation](https://docs.docker.com/)

---

## ✅ Checklist Development

Prima di submitare una PR:
- [ ] Code testato localmente con `docker-compose up`
- [ ] Unit test passano con 70%+ coverage
- [ ] Integration test passano
- [ ] Documentazione aggiornata (README, SPECIFICATION, API)
- [ ] Schema database aggiornato se applicabile
- [ ] Cartella examples/ aggiornata con nuovi esempi
- [ ] Nessun secret o valore hardcoded
- [ ] Commit message seguono guideline
- [ ] CHANGELOG.md aggiornato

---

## 🆘 Come Ottenere Aiuto

1. **Controlla Documentazione**: TROUBLESHOOTING.md nella cartella microservizio
2. **Rivedi Esempi**: Vedi cartella examples/ per utilizzo API
3. **Chiedi al Team**: #zendata-dev Slack channel
4. **Controlla Issue**: GitHub issues per problemi noti
5. **Leggi Spec**: SPECIFICATION.md per dettagli tecnici

---

**Versione**: 1.0
**Ultimo Aggiornamento**: 2024-11-18
**Maintainers**: ZenIA Development Team
