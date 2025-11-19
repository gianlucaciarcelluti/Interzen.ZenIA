# Test Guide - NiFi Workflows via Postman

Questa guida spiega come testare i workflow NiFi usando la collection Postman.

## 📋 Prerequisiti

1. ✅ Tutti i servizi Docker devono essere attivi
2. ✅ I workflow NiFi devono essere deployati (esegui `./setup-nifi-workflows.sh`)
3. ✅ I processor devono essere avviati (esegui `./start-all-processors.sh`)

## 🔌 Porte dei Workflow

| Workflow | Porta ListenHTTP | Base Path | Microservizio |
|----------|------------------|-----------|---------------|
| SP01 - EML Parser | 9091 | /sp01 | http://sp01-eml-parser:5001 |
| SP02 - Document Extractor | 9092 | /sp02 | http://sp02-document-extractor:5002 |
| SP03 - Procedural Classifier | 9093 | /sp03 | http://sp03-procedural-classifier:5003 |
| SP04 - Knowledge Base | 9094 | /sp04 | http://sp04-knowledge-base:5004 |
| SP05 - Template Engine | 9095 | /sp05 | N/A |
| SP06 - Validator | 9096 | /sp06 | N/A |
| SP07 - Content Classifier | 9097 | /sp07 | N/A |
| SP08 - Quality Checker | 9098 | /sp08 | N/A |
| SP11 - Security Audit | 9101 | /sp11 | N/A |

## 🧪 Test Rapidi via cURL

### SP01 - EML Parser
```bash
curl -X POST http://localhost:9091/sp01 \
  -H 'Content-Type: application/json' \
  -d '{
    "eml_content": "From: test@example.com\nTo: recipient@example.com\nSubject: Test\n\nBody"
  }'
```

### SP02 - Document Extractor
```bash
curl -X POST http://localhost:9092/sp02 \
  -H 'Content-Type: application/json' \
  -d '{
    "document": {
      "content": "Test document content"
    }
  }'
```

### SP03 - Procedural Classifier
```bash
curl -X POST http://localhost:9093/sp03 \
  -H 'Content-Type: application/json' \
  -d '{
    "workflow_id": "wf_123",
    "istanza_metadata": {
      "oggetto": "Richiesta autorizzazione",
      "descrizione_istanza": "Test"
    }
  }'
```

### SP04 - Knowledge Base
```bash
curl -X POST http://localhost:9094/sp04 \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "normativa ambientale",
    "context": "autorizzazione scarico acque"
  }'
```

## 📊 Verifica Stato Workflow

### Controlla se i processor sono in esecuzione
```bash
curl -s http://localhost:8080/nifi-api/flow/process-groups/root | \
  jq '.processGroupFlow.flow.processGroups[] | {name: .component.name, running: .runningCount, stopped: .stoppedCount}'
```

### Avvia tutti i processor
```bash
./start-all-processors.sh
```

### Controlla porte ListenHTTP
```bash
lsof -i :9091-9101
```

## 🐛 Troubleshooting

### Problema: "Connection refused" o timeout

**Soluzione**:
1. Verifica che i processor siano in esecuzione:
   ```bash
   ./start-all-processors.sh
   ```

2. Controlla i log NiFi:
   ```bash
   docker logs nifi-orchestrator --tail 100
   ```

3. Verifica che i microservizi siano attivi:
   ```bash
   curl http://localhost:5001/health  # SP01
   curl http://localhost:5002/health  # SP02
   curl http://localhost:5003/health  # SP03
   curl http://localhost:5004/health  # SP04
   ```

### Problema: "Invalid processor configuration"

**Causa**: Il processor InvokeHTTP non ha l'URL del microservizio configurato

**Soluzione**: Gli script Python dovrebbero configurare automaticamente gli URL. Se il problema persiste, configura manualmente via UI:
1. Apri http://localhost:8080/nifi
2. Doppio click sul process group
3. Click destro sul processor InvokeHTTP → Configure
4. Tab Properties → Remote URL: `http://sp0X-service:500X/endpoint`

### Problema: ListenHTTP non risponde

**Verifica**:
```bash
# Controlla se la porta è aperta
lsof -i :9091

# Controlla stato del processor
PG_ID=$(curl -s http://localhost:8080/nifi-api/process-groups/root/process-groups | \
  jq -r '.processGroups[] | select(.component.name == "SP01_EML_Parser") | .id')

curl -s "http://localhost:8080/nifi-api/process-groups/$PG_ID/processors" | \
  jq '.processors[] | {name: .component.name, state: .component.state}'
```

## 📮 Usando Postman

1. Importa la collection: `ZenIA_Postman_Collection.json`
2. Le variabili sono già configurate:
   - `base_url`: localhost
   - `nifi_url`: http://localhost:8080
3. Usa la cartella **"NiFi Flows (via ListenHTTP)"** per testare i workflow
4. Ogni request ha esempi di payload pre-configurati

## ✅ Checklist Pre-Test

- [ ] Docker compose up e tutti i container healthy
- [ ] Setup workflow eseguito (`./setup-nifi-workflows.sh`)
- [ ] Processor avviati (`./start-all-processors.sh`)
- [ ] Microservizi rispondono agli health check
- [ ] Porte 9091-9101 sono aperte (verifica con `lsof`)

## 📝 Note

- I workflow elaborano i dati in modo asincrono
- Le risposte potrebbero richiedere qualche secondo
- I FlowFile vengono processati attraverso le connessioni
- Per debug dettagliato, usa la UI NiFi su http://localhost:8080/nifi
