# Developer Workflow - Guida Operativa

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | [DEVELOPMENT-GUIDE.md](../DEVELOPMENT-GUIDE.md) →

---

## 🎯 Il Tuo Workflow in 70 Minuti

```
DAY 1 - LEARNING PHASE (30 minuti)
├─ 5 min:  Leggi UC Overview                    [docs/use_cases/UC5/00_OVERVIEW.md]
├─ 5 min:  Capire quale MS implementare         [MS-ARCHITECTURE-MASTER.md]
├─ 10 min: Leggi MS README.md                   [MS02-ANALYZER/README.md]
├─ 5 min:  Esamina API reference                [MS02-ANALYZER/API.md]
└─ 5 min:  Guarda examples payload              [MS02-ANALYZER/examples/]

DAY 1 - SETUP PHASE (15 minuti)
├─ 10 min: Setup locale con docker-compose       [docker-compose up -d]
├─ 3 min:  Verifica salute servizio             [curl /health]
└─ 2 min:  Test API con example payload         [curl -X POST /api/v1/...]

DAY 2-3 - IMPLEMENTATION PHASE (20 minuti)
├─ 5 min:  Leggi SPECIFICATION.md               [MS02-ANALYZER/SPECIFICATION.md]
├─ 10 min: Implementa feature usando API        [Segui template API.md]
├─ 3 min:  Scrivi unit test                     [Pytest test/]
└─ 2 min:  Verifica su localhost                [curl http://localhost:8002/...]

DAY 3 - DEPLOYMENT PHASE (5 minuti)
├─ 2 min:  Build Docker image                   [docker build -t ...]
├─ 2 min:  Push to registry                     [docker push ...]
└─ 1 min:  Deploy con kubectl                   [kubectl apply -f kubernetes/]

TOTAL TIME: ~70 minuti
```

---

## 📍 Bookmark dei File Essenziali

### Fase 1: Learning (quando inizi)
```
📌 MS-ARCHITECTURE-MASTER.md
   └─ Trova il tuo MS nella matrice (2 min)

📌 [MSxx]/README.md (es: MS02-ANALYZER/README.md)
   └─ Capire cosa fa il servizio (5 min)

📌 [MSxx]/API.md (es: MS02-ANALYZER/API.md)
   └─ Quale endpoint devo usare? (5 min)

📌 [MSxx]/examples/request.json + response.json
   └─ Copiare payload di esempio (2 min)
```

### Fase 2: Setup Locale (quando configuri)
```
📌 [MSxx]/docker-compose.yml
   └─ docker-compose up -d

📌 [MSxx]/TROUBLESHOOTING.md
   └─ Se qualcosa non funziona

📌 http://localhost:800X/health
   └─ Verifica che è up
```

### Fase 3: Implementation (quando codi)
```
📌 [MSxx]/SPECIFICATION.md
   └─ Come funziona internamente (architettura)

📌 [MSxx]/DATABASE-SCHEMA.md
   └─ Quale database usare? Tabelle? Indici?

📌 [MSxx]/API.md
   └─ Che tipo di payload mi aspetta?
```

### Fase 4: Testing (quando verifichi)
```
📌 [MSxx]/examples/request.json
   └─ curl -X POST http://localhost:800X/api/v1/... -d @request.json

📌 [MSxx]/examples/response.json
   └─ Confronta la risposta attesa
```

### Fase 5: Deployment (quando pushh)
```
📌 [MSxx]/kubernetes/deployment.yaml
   └─ kubectl apply -f kubernetes/

📌 Kubernetes monitoring
   └─ kubectl logs -f deployment/msxx-*
```

---

## 🔄 Workflow Visuale: Da Requirement a Production

```
┌─────────────────────────────────────────────────────────────────┐
│ START: Ho un feature da implementare in MS02-ANALYZER           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ STEP 1: DISCOVER │
                    │    (5 minuti)    │
                    └──────────────────┘
                    ↓ Leggi MS-ARCHITECTURE-MASTER.md
                    ↓ Trova MS02 nella matrice
                    ↓ Clicca link [📂 Vedi MS02]
                    ▼
                    ┌──────────────────────────────┐
                    │ STEP 2: LEARN                │
                    │ (10 minuti)                  │
                    ├──────────────────────────────┤
                    │ • MS02-ANALYZER/README.md    │
                    │ • MS02-ANALYZER/API.md       │
                    │ • examples/request.json      │
                    └──────────────────────────────┘
                              ▼
                    ┌──────────────────────────────┐
                    │ STEP 3: SETUP LOCAL          │
                    │ (15 minuti)                  │
                    ├──────────────────────────────┤
                    │ • docker-compose up -d       │
                    │ • curl localhost:8002/health │
                    │ • Test first API call        │
                    └──────────────────────────────┘
                              ▼
                    ┌──────────────────────────────┐
                    │ STEP 4: IMPLEMENT            │
                    │ (20 minuti)                  │
                    ├──────────────────────────────┤
                    │ • Leggi SPECIFICATION.md     │
                    │ • Scrivi codice              │
                    │ • Test locally               │
                    └──────────────────────────────┘
                              ▼
                    ┌──────────────────────────────┐
                    │ STEP 5: DEPLOY               │
                    │ (5 minuti)                   │
                    ├──────────────────────────────┤
                    │ • docker build / push        │
                    │ • kubectl apply -f k8s/      │
                    └──────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ DONE! Feature è in production (70 minuti totali)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ Mappa File per Ruolo

### Se sei Frontend Developer
```
Ignora database schema e deployment
Focus su: API.md → examples/ → Request/Response payloads
Tempo: ~5 minuti per capire come chiamare l'API
```

### Se sei Backend Developer
```
Read: README.md → SPECIFICATION.md → DATABASE-SCHEMA.md → API.md
Implement: docker-compose.yml → local testing → feature code
Time: ~50 minuti setup + coding
```

### Se sei DevOps
```
Focus su: kubernetes/ → docker-compose.yml → TROUBLESHOOTING.md
Ignora: API details, database schema details
```

### Se sei Architect/PM
```
Read: MS-ARCHITECTURE-MASTER.md → README.md
Ignore: Implementation details
Time: ~5 minuti per capire il servizio
```

---

## ✅ Checklist per Feature Completa

**Learning Phase**
- [ ] Ho trovato il MS giusto nella matrice
- [ ] Ho letto il README.md del MS
- [ ] Ho capito come funziona (cosa fa)

**Setup Phase**
- [ ] docker-compose è up
- [ ] Servizio risponde a /health
- [ ] Ho testato almeno 1 API con example payload

**Implementation Phase**
- [ ] Ho letto SPECIFICATION.md
- [ ] Ho capito la sequenza di esecuzione (flow)
- [ ] Ho scritto il codice seguendo l'API.md
- [ ] Unit test sono > 70% coverage

**Testing Phase**
- [ ] Ho testato locally prima di push
- [ ] Payload request/response matchano con examples
- [ ] Ho verificato sul localhost

**Deployment Phase**
- [ ] Image Docker build successivamente
- [ ] Image push al registry
- [ ] kubectl apply ha successo
- [ ] Pod è in running state
- [ ] Health check ritorna 200 OK

---

## 🚀 QuickStart: Copy-Paste Ready

### 1. Setup (esegui una volta)
```bash
cd docs/microservices/MS02-ANALYZER
docker-compose up -d
sleep 5
curl http://localhost:8002/health
```

### 2. Test API (verifica che funziona)
```bash
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d @examples/request.json | jq .
```

### 3. Develop (il tuo codice qui)
```bash
# Usa SPECIFICATION.md come blueprint
# Usa API.md come reference
# Copia payload structure da examples/
```

### 4. Deploy (quando finisci)
```bash
cd ../..
docker build -t zendata/ms02-analyzer:v1 MS02-ANALYZER/
docker push zendata/ms02-analyzer:v1
kubectl apply -f MS02-ANALYZER/kubernetes/
kubectl rollout status deployment/ms02-analyzer
```

---

## 🔗 Link Rapidi per Fase

| Fase | Documento | Link |
|------|-----------|------|
| Discover | Matrice MS | [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) |
| Learn | README | [MS01-CLASSIFIER/README.md](MS01-CLASSIFIER/README.md) |
| Learn | API | [MS01-CLASSIFIER/API.md](MS01-CLASSIFIER/API.md) |
| Learn | Examples | [MS01-CLASSIFIER/examples/](MS01-CLASSIFIER/examples/) |
| Setup | docker-compose | [MS01-CLASSIFIER/docker-compose.yml](MS01-CLASSIFIER/docker-compose.yml) |
| Implement | SPEC | [MS01-CLASSIFIER/SPECIFICATION.md](MS01-CLASSIFIER/SPECIFICATION.md) |
| Implement | Database | [MS01-CLASSIFIER/DATABASE-SCHEMA.md](MS01-CLASSIFIER/DATABASE-SCHEMA.md) |
| Test | Examples | [MS01-CLASSIFIER/examples/](MS01-CLASSIFIER/examples/) |
| Deploy | Kubernetes | [MS01-CLASSIFIER/kubernetes/](MS01-CLASSIFIER/kubernetes/) |

---

**Pro Tips:**
- Stampa questa pagina come bookmark
- Tieni aperto MS-ARCHITECTURE-MASTER.md nella prima tab
- Usa Ctrl+F per cercare il tuo MS
- Se sei bloccato → Consulta TROUBLESHOOTING.md del tuo MS

Navigazione: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | [DEVELOPMENT-GUIDE.md](../DEVELOPMENT-GUIDE.md) →
