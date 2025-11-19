# 📊 Guida al Tracciamento del Workflow

## 🎯 Cosa succede dopo l'invio di un file .eml

Quando invii un file `.eml` tramite il POC Streamlit, il sistema esegue il seguente flusso:

```
📧 Email (.eml)
 ↓
🌐 POST http://localhost:9099/contentListener/fascicolo
 ↓
📦 Ingress_ContentListener (NiFi Process Group)
 ├─ HandleHttpRequest (porta 9099)
 ├─ Generate_Workflow_ID (UUID univoco)
 ├─ Log_Incoming_Request (attributi FlowFile)
 ├─ Route_To_Workflow (routing per tipo file)
 └─ HandleHttpResponse (HTTP 200 al client)
 ↓
📦 SP01_EML_Parser (NiFi Process Group)
 ├─ Input Port 'From_Ingress'
 ├─ Call_SP01_Microservice (POST http://sp01:5001/parse)
 │   → Groq AI Classification
 │   → Estrazione allegati PDF
 ├─ Route_Success_Failure
 └─ Output Port 'Success'
 ↓
📦 SP11_HITL_Manager (se configurato)
 ├─ Input Port 'From_SP01'
 ├─ Call_SP11_Security_Audit (POST http://hitl:5009/hitl/review)
 └─ Human-In-The-Loop Review
```

---

## 📈 Come Verificare l'Elaborazione

### 1. **Risposta HTTP Immediata**
Dopo l'invio, riceverai **HTTP 200** immediatamente dal server.

Questo indica che:
- ✅ Email ricevuta da NiFi
- ✅ Workflow avviato
- ✅ Elaborazione in corso in background

### 2. **Tracciamento Database Audit**

Tutti i passaggi del workflow vengono tracciati nel database `nifi_audit`.

#### Query Rapide

**Visualizza ultime esecuzioni:**
```sql
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT 
    workflow_name,
    step_name,
    status,
    started_at,
    duration_ms
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 10;
"
```

**Verifica esecuzioni fallite:**
```sql
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT 
    workflow_name,
    step_name,
    error_message,
    started_at
FROM workflow_executions
WHERE status = 'FAILED'
ORDER BY started_at DESC
LIMIT 5;
"
```

**Traccia un'esecuzione specifica (per execution_id):**
```sql
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT 
    workflow_name,
    step_name,
    status,
    duration_ms,
    attributes
FROM workflow_executions
WHERE execution_id = 'YOUR-UUID-HERE'
ORDER BY started_at;
"
```

**Statistiche generali:**
```sql
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT 
    workflow_name,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) as successes,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failures,
    AVG(duration_ms) as avg_duration_ms
FROM workflow_executions
GROUP BY workflow_name
ORDER BY total_executions DESC;
"
```

### 3. **Logs dei Microservizi**

Controlla i logs dei singoli servizi:

```bash
# SP01 EML Parser
docker-compose logs -f sp01-eml-parser | grep -i "parse"

# HITL Manager
docker-compose logs -f hitl-manager | grep -i "review"

# NiFi (completo)
docker-compose logs -f nifi | tail -100
```

### 4. **NiFi UI - Provenance**

1. Apri NiFi UI: http://localhost:8080/nifi
2. Tasto destro su un processor → "View Provenance"
3. Cerca per attributi (es. `filename`, `workflow_id`)
4. Vedi l'intero lineage del FlowFile

---

## 🔍 Dove Finiscono i Dati?

### Tabelle Database Audit

| Tabella | Contenuto |
|---------|-----------|
| `workflow_executions` | **Tracciamento completo** di ogni step del workflow |
| `http_requests` | Log di tutte le chiamate HTTP (ingress + microservizi) |
| `error_log` | Errori e warning durante l'elaborazione |
| `performance_metrics` | Metriche di performance (CPU, memoria, tempo) |
| `data_quality_checks` | Validazioni e controlli qualità dati |

### Esempio Record `workflow_executions`

```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "workflow_name": "SP01_EML_Parser",
  "step_name": "Call_Microservice",
  "status": "SUCCESS",
  "started_at": "2025-11-04T15:30:00",
  "completed_at": "2025-11-04T15:30:03",
  "duration_ms": 3200,
  "input_data": {
    "filename": "email_test.eml",
    "size_bytes": 45320
  },
  "output_data": {
    "tipologia_provvedimento": "Autorizzazione Scarico",
    "attachments_extracted": 1,
    "classification_confidence": 0.92
  },
  "attributes": {
    "workflow_id": "550e8400-e29b-41d4-a716-446655440000",
    "mime.type": "message/rfc822",
    "filename": "email_test.eml"
  }
}
```

---

## 🎨 Dashboard e Visualizzazioni (Opzionali)

### Grafana + PostgreSQL

Puoi collegare Grafana al database `nifi_audit` per visualizzare:

- 📊 Numero esecuzioni per workflow (time series)
- ✅ Success rate per workflow
- ⏱️ Performance metrics (P50, P95, P99)
- 🚨 Alert su failure rate > soglia

### Query Grafana Esempio

```sql
SELECT
  $__timeGroup(started_at, '1h') as time,
  workflow_name,
  COUNT(*) as executions
FROM workflow_executions
WHERE $__timeFilter(started_at)
GROUP BY time, workflow_name
ORDER BY time
```

---

## 🧪 Test Rapido

### 1. Invia Email di Test

```bash
curl -X POST http://localhost:9099/contentListener/fascicolo \
  -H "Content-Type: message/rfc822" \
  -d "From: test@esempio.it
To: office@comune.it
Subject: Test Workflow
Content-Type: text/plain

Test del workflow completo.
"
```

### 2. Verifica Record Audit (dopo 2-3 secondi)

```bash
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT workflow_name, step_name, status, started_at
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 5;
"
```

### 3. Verifica Logs SP01

```bash
docker-compose logs sp01-eml-parser | tail -20
```

---

## 🎯 Risultati Attesi

✅ **HTTP 200** - Email ricevuta
✅ **Record in `workflow_executions`** - Workflow tracciato
✅ **Logs microservizi** - Elaborazione confermata
✅ **NiFi Provenance** - Lineage completo FlowFile

---

## 🚨 Troubleshooting

### ❌ Nessun record in `workflow_executions`

**Causa:** Controller Services non abilitati

**Soluzione:**
```bash
./enable-controller-services.sh
```

### ❌ Errore "FAILED" in workflow_executions

**Controlla:**
```bash
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT error_message, error_details
FROM workflow_executions
WHERE status = 'FAILED'
ORDER BY started_at DESC
LIMIT 1;
"
```

### ❌ SP01 non risponde

**Verifica:**
```bash
curl http://localhost:5001/health
docker-compose logs sp01-eml-parser | tail -50
```

---

## 📚 Documentazione Completa

- **Audit Trail Schema:** `init-nifi-audit.sql`
- **API Endpoints:** `POSTMAN-TEST-GUIDE.md`
- **Integration Flow:** `INTEGRATION-FLOW-GUIDE.md`

---

## ✅ Conclusione

Dopo l'invio di un file `.eml`:

1. **Risposta immediata**: HTTP 200
2. **Tracciamento database**: `nifi_audit.workflow_executions`
3. **Logs microservizi**: `docker-compose logs`
4. **NiFi Provenance**: UI di NiFi

Il sistema è completamente **tracciabile** e **auditabile**! 🎉
