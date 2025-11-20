# Microservizi ZenIA - Guida Rapida

**Navigazione**: [← ../README.md](../README.md) | [Microservices README](README.md) | [MS-ARCHITECTURE-MASTER →](MS-ARCHITECTURE-MASTER.md)

---

## 🎯 Se sei un Developer che Deve Implementare un Feature

### 5 Passi (70 minuti totali):

1. **Scopri quale MS** → Apri [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md)
2. **Impara velocemente** → Leggi il README.md del tuo MS (~5 min)
3. **Setup locale** → `docker-compose up -d` (~15 min)
4. **Implementa feature** → Segui API.md e SPECIFICATION.md (~20 min)
5. **Deploy** → `docker build` + `docker push` + `kubectl apply` (~5 min)

👉 **[Workflow Completo con Timing](DEVELOPER-WORKFLOW.md)**

---

## 📚 Documentazione Disponibile

### Per Developer
| File | Uso | Tempo |
|------|-----|-------|
| [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | **INIZIA QUI** - Matrice dei 16 MS | 5 min |
| [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) | Timeline + bookmark guide | 10 min |
| [MSxx/README.md](MS01-CLASSIFIER/README.md) | Quick start del tuo MS | 5 min |
| [MSxx/SPECIFICATION.md](MS01-CLASSIFIER/SPECIFICATION.md) | Architettura tecnica | 30 min |
| [MSxx/API.md](MS01-CLASSIFIER/API.md) | Endpoint reference | Reference |
| [MSxx/DATABASE-SCHEMA.md](MS01-CLASSIFIER/DATABASE-SCHEMA.md) | Schema database | Reference |
| [MSxx/docker-compose.yml](MS01-CLASSIFIER/docker-compose.yml) | Setup locale | - |
| [MSxx/examples/](MS01-CLASSIFIER/examples/) | Request/response examples | Copy-paste |

### Per Navigazione
| File | Uso | Tipo |
|------|-----|------|
| [BREADCRUMB-NAVIGATION.md](BREADCRUMB-NAVIGATION.md) | Come aggiungere breadcrumb | Template |
| [GITHUB-NAVIGATION-GUIDE.md](GITHUB-NAVIGATION-GUIDE.md) | Come scrivere anchor link | Guide |
| [TESTING-WORKFLOW.md](TESTING-WORKFLOW.md) | Come testare il workflow | Checklist |

### Per Architetto
| File | Uso | Tempo |
|------|-----|-------|
| [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md) | Sistema completo | 20 min |
| [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | Matrice dipendenze | 10 min |
| [../COMPLIANCE-MATRIX.md](../COMPLIANCE-MATRIX.md) | Compliance mapping | Reference |

---

## 📍 I 16 Microservizi

Clicca su uno per aprire il README:

| MS | Nome | Ruolo | Docum. |
|----|------|-------|--------|
| **MS01** | CLASSIFIER | Classificazione documenti | [README](MS01-CLASSIFIER/README.md) |
| **MS02** | ANALYZER | Analisi contenuto & NLP | [README](MS02-ANALYZER/README.md) |
| **MS03** | ORCHESTRATOR | Orchestrazione workflow | [README](MS03-ORCHESTRATOR/README.md) |
| **MS04** | VALIDATOR | Validazione dati | [README](MS04-VALIDATOR/README.md) |
| **MS05** | TRANSFORMER | Trasformazione dati | [README](MS05-TRANSFORMER/README.md) |
| **MS06** | AGGREGATOR | Aggregazione dati | [README](MS06-AGGREGATOR/README.md) |
| **MS07** | DISTRIBUTOR | Distribuzione contenuti | [README](MS07-DISTRIBUTOR/README.md) |
| **MS08** | MONITOR | Monitoraggio sistema | [README](MS08-MONITOR/README.md) |
| **MS09** | MANAGER | Gestione risorse | [README](MS09-MANAGER/README.md) |
| **MS10** | LOGGER | Logging centralizzato | [README](MS10-LOGGER/README.md) |
| **MS11** | GATEWAY | API gateway | [README](MS11-GATEWAY/README.md) |
| **MS12** | CACHE | Caching distribuito | [README](MS12-CACHE/README.md) |
| **MS13** | SECURITY | Sicurezza & crittografia | [README](MS13-SECURITY/README.md) |
| **MS14** | AUDIT | Audit & compliance | [README](MS14-AUDIT/README.md) |
| **MS15** | CONFIG | Gestione configurazione | [README](MS15-CONFIG/README.md) |
| **MS16** | REGISTRY | Service discovery | [README](MS16-REGISTRY/README.md) |

---

## 🚀 Quickstart

### Opzione 1: Sono un Developer
```bash
# 1. Apri la matrice dei microservizi
open MS-ARCHITECTURE-MASTER.md

# 2. Trova il tuo MS e clicca il link
# (es: MS02-ANALYZER)

# 3. Segui il workflow di 70 minuti
open DEVELOPER-WORKFLOW.md
```

## [Auto-generated heading level 2]
### Opzione 2: Sono un Architect
```bash
# 1. Capire il sistema
open ../ARCHITECTURE-OVERVIEW.md

# 2. Vedere la matrice
open MS-ARCHITECTURE-MASTER.md

# 3. Compliance check
open ../COMPLIANCE-MATRIX.md
```

## [Auto-generated heading level 2]
### Opzione 3: Sono un DevOps
```bash
# 1. Deployment setup
cd MSxx-NAME
open kubernetes/deployment.yaml

# 2. Local testing
docker-compose up -d
curl http://localhost:800X/health

# 3. Troubleshooting
open TROUBLESHOOTING.md
```

---

## 🗂️ Struttura Cartelle

```
docs/microservices/
│
├── README.md ← Questo file
├── MS-ARCHITECTURE-MASTER.md ⭐ Inizio per developer
├── DEVELOPER-WORKFLOW.md ⭐ Timeline + guide
│
├── BREADCRUMB-NAVIGATION.md (template)
├── GITHUB-NAVIGATION-GUIDE.md (template)
├── TESTING-WORKFLOW.md (checklist)
│
├── MS01-CLASSIFIER/ ⭐ Reference Implementation
│   ├── README.md (5 min quick start)
│   ├── SPECIFICATION.md (30 min deep dive)
│   ├── API.md (endpoint reference)
│   ├── DATABASE-SCHEMA.md (ER diagrams)
│   ├── init-schema.sql (DDL script)
│   ├── TROUBLESHOOTING.md (problem solving)
│   ├── docker-compose.yml (local setup)
│   ├── kubernetes/ (production deploy)
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   └── examples/ (request/response samples)
│       ├── request.json
│       └── response.json
│
├── MS02-ANALYZER/ (same pattern as MS01)
├── MS03-ORCHESTRATOR/ (same pattern)
│
└── ... MS04-MS16/ (template structure ready)
```

---

## 🎯 Key Concepts

### 70-Minute Developer Workflow

```
┌─────────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐     ┌──────────┐
│  Discovery  │ 5   │ Learning│ 10  │  Setup   │ 15  │ Coding │ 20  │  Deploy  │ 5
│  (5 min)    │───→ │(10 min) │───→ │(15 min)  │───→ │(20 min)│───→ │ (5 min)  │
└─────────────┘     └─────────┘     └──────────┘     └────────┘     └──────────┘

TOTAL: ~70 minutes
```

### Microservice Pattern

Ogni microservice ha **9 elementi** documentati:

1. **README.md** - What + How + Link Next
2. **SPECIFICATION.md** - Architecture + Design
3. **API.md** - Endpoints + Payloads
4. **DATABASE-SCHEMA.md** - Data Model
5. **init-schema.sql** - DDL Script (separate)
6. **TROUBLESHOOTING.md** - Problems + Solutions
7. **docker-compose.yml** - Local Setup
8. **kubernetes/** - Production Deploy
9. **examples/** - Request/Response Samples

### 3 Navigation Systems

1. **Breadcrumb** - Move between files (top + bottom)
2. **Anchor Links** - Jump within document (GitHub-compatible)
3. **Index/TOC** - Quick jump to sections

---

## ❓ FAQ

### D: Ho appena 15 minuti, cosa leggo?
**A**: [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) + il README del tuo MS

### D: Cosa faccio prima di codare?
**A**: [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) - segui il workflow di 70 minuti

### D: Dove copio i payload di esempio?
**A**: `MSxx-NAME/examples/request.json` + `response.json`

### D: Come faccio il setup locale?
**A**: `cd MSxx-NAME && docker-compose up -d`

### D: Quale file devo leggere prima di implementare?
**A**: README.md (5 min) → SPECIFICATION.md (30 min) → API.md (reference)

### D: I link non funzionano su GitHub?
**A**: Vedi [GITHUB-NAVIGATION-GUIDE.md](GITHUB-NAVIGATION-GUIDE.md)

### D: Come testo che il mio workflow funziona?
**A**: Usa [TESTING-WORKFLOW.md](TESTING-WORKFLOW.md) checklist

---

## ✅ Checklist per Prima Volta

- [ ] Letto [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md)
- [ ] Trovato il mio MS nella matrice
- [ ] Clicca il link per aprire il README
- [ ] Letto il README del mio MS (5 min)
- [ ] Capito cosa fa il servizio
- [ ] Visto il docker-compose.yml
- [ ] Setup locale con `docker-compose up -d`
- [ ] Testato API con `curl` + example payload
- [ ] Passato alla fase "Learning" di [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md)

---

## 📞 Bisogna Aiuto?

| Problema | Soluzione |
|----------|-----------|
| Non trovo il mio MS | Usa Ctrl+F in [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) |
| Link è rotto | Vedi [BREADCRUMB-NAVIGATION.md](BREADCRUMB-NAVIGATION.md) |
| Anchor link non funziona | Vedi [GITHUB-NAVIGATION-GUIDE.md](GITHUB-NAVIGATION-GUIDE.md) |
| Docker non avvia | Apri [MSxx/TROUBLESHOOTING.md](MS01-CLASSIFIER/TROUBLESHOOTING.md) |
| API ritorna errore | Confronta payload con [MSxx/examples/request.json](MS01-CLASSIFIER/examples/request.json) |
| Non capisco il workflow | Leggi [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) |
| Voglio testare tutto | Usa [TESTING-WORKFLOW.md](TESTING-WORKFLOW.md) |

---

## 🔗 Link Importanti

**Per Developer**:
- [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) ← INIZIO QUI
- [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) ← Timeline
- [MS01-CLASSIFIER/README.md](MS01-CLASSIFIER/README.md) ← Esempio

**Per Architettura**:
- [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
- [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md)
- [../COMPLIANCE-MATRIX.md](../COMPLIANCE-MATRIX.md)

**Per Navigazione**:
- [BREADCRUMB-NAVIGATION.md](BREADCRUMB-NAVIGATION.md)
- [GITHUB-NAVIGATION-GUIDE.md](GITHUB-NAVIGATION-GUIDE.md)
- [TESTING-WORKFLOW.md](TESTING-WORKFLOW.md)

---

## 📈 Statistiche

- **Microservizi**: 16 (MS01-MS16)
- **Documenti per MS**: 9 (README + SPEC + API + DB + init.sql + troubleshooting + compose + k8s + examples)
- **Setup time**: ~15 minuti
- **Learning time**: ~15 minuti
- **Development time**: ~20 minuti
- **Deployment time**: ~5 minuti
- **Total workflow**: ~70 minuti
- **Language**: 100% Italiano

---

**Last Updated**: 2024-11-18
**Language**: Italiano
**Status**: ✅ Ready for developers
**Maintainers**: ZenIA Documentation Team

Navigazione: [← ../README.md](../README.md) | [Microservices README](README.md) | [MS-ARCHITECTURE-MASTER →](MS-ARCHITECTURE-MASTER.md)
