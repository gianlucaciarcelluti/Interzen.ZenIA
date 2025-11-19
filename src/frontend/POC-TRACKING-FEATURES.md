# 🎯 POC Streamlit - Workflow Tracking & HITL Checkpoint

## ✨ Nuove Funzionalità Implementate

### 1. **Progress Bar in Tempo Reale** 📊

Dopo l'invio di un file `.eml`, il POC ora mostra l'avanzamento del workflow in tempo reale interrogando il database `nifi_audit`.

#### Fasi Tracciate

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Ingress   │ → │  SP01_Parse │ → │SP01_Classify│ → │ HITL_Review │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
      ✅              ⏳               ⏸️               ⏸️
```

**Stati possibili:**
- ✅ **Success** - Fase completata con successo
- ❌ **Failed** - Fase fallita (con dettagli errore)
- ⏳ **Running** - Fase in esecuzione
- ⏸️ **Pending** - Fase in attesa

---

### 2. **Tracking Database Audit** 🔍

Il sistema interroga la tabella `workflow_executions` nel database `nifi_audit` per recuperare:

- **Execution ID univoco** - Per tracciare l'intera catena di esecuzione
- **Stato di ogni step** - SUCCESS, FAILED, RUNNING
- **Durata di ogni fase** - In millisecondi
- **Output data** - Risultati della classificazione AI
- **Error messages** - In caso di fallimenti

#### Query SQL Utilizzata

```sql
SELECT 
    workflow_name,
    step_name,
    status,
    duration_ms,
    output_data,
    error_message,
    completed_at
FROM workflow_executions
WHERE execution_id = %s
ORDER BY started_at DESC
```

---

### 3. **Visualizzazione Risultato Classificazione** 📋

Quando SP01 completa la classificazione, il POC mostra:

#### Informazioni Principali
- **Tipologia Provvedimento** (es: "Autorizzazione Scarico Acque")
- **Confidence Score** (es: 92%)
- **Allegati Estratti** (numero e dimensione)

#### Dettagli Completi (Espandibile)
```json
{
  "tipologia_provvedimento": "Autorizzazione Scarico",
  "classification_confidence": 0.92,
  "attachments_extracted": 1,
  "groq_model": "llama-3.3-70b-versatile",
  "processing_time_ms": 3200
}
```

---

### 4. **Checkpoint HITL - Conferma Risultato** 🛡️

Il POC implementa un checkpoint Human-In-The-Loop per validare i risultati:

#### Opzioni Disponibili

**✅ Approva**
- Conferma il risultato della classificazione
- Il workflow continua automaticamente
- Mostra animazione celebrativa 🎈

**❌ Rigetta**
- Segnala un risultato errato
- Richiede revisione manuale
- Il caso viene marcato per intervento umano

---

## 🚀 Come Usare le Nuove Funzionalità

### Passo 1: Avvia Streamlit

```bash
cd src/frontend
source ../../.venv/bin/activate
python3 -m streamlit run poc_eml_to_hitl.py --server.port 8501
```

### Passo 2: Invia un File .eml

1. Apri http://localhost:8501
2. Seleziona un file `.eml` di esempio (o caricane uno tuo)
3. Clicca **"🚀 Invia"**

### Passo 3: Osserva il Workflow

Vedrai automaticamente:

```
📤 Invio email in corso...
✅ Email inviata con successo!
🔍 Execution ID: `550e8400-e29b-41d4-a716-446655440000`

───────────────────────────────────────────
📊 Avanzamento Workflow

Progress: ████████████████████░░░░ 80%

✅ Ingress       ⏳ SP01_Parse    ⏸️ SP01_Classify  ⏸️ HITL_Review
   250ms            2800ms

⏳ Elaborazione in corso...
```

### Passo 4: Revisiona il Risultato

Una volta completato:

```
✅ Workflow completato in 8.3s

───────────────────────────────────────────
📊 Risultato Classificazione

✅ Tipologia: Autorizzazione Scarico Acque Reflue

Confidence: 92%

📎 Allegati estratti: 1

🔍 Dettagli Completi ▼
  {
    "tipologia_provvedimento": "Autorizzazione Scarico",
    "classification_confidence": 0.92,
    ...
  }

───────────────────────────────────────────
🛡️ Checkpoint HITL - Conferma Risultato

[✅ Approva]  [❌ Rigetta]
```

### Passo 5: Approva o Rigetta

- **Se corretto** → Clicca "✅ Approva"
- **Se errato** → Clicca "❌ Rigetta" e intervieni manualmente

---

## 🔧 Architettura Tecnica

### Flusso Dati

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │ 1. POST /contentListener/fascicolo
         │    Header: X-Execution-ID
         ↓
┌─────────────────┐
│ NiFi Ingress PG │
└────────┬────────┘
         │ 2. Process & Route
         ↓
┌─────────────────┐       ┌──────────────┐
│   SP01 Parser   │ ───→  │ PostgreSQL   │
└────────┬────────┘       │ nifi_audit   │
         │                └──────────────┘
         │ 3. Classification           ↑
         ↓                              │
┌─────────────────┐                    │
│  HITL Manager   │                    │
└─────────────────┘                    │
                                       │
         ┌─────────────────────────────┘
         │ 4. Poll status ogni 1 secondo
         ↓
┌─────────────────┐
│  Streamlit UI   │ ← Mostra progress bar
└─────────────────┘
```

### Polling Strategy

```python
def track_workflow_execution(execution_id, max_wait=30):
    start_time = time.time()
    
    while (time.time() - start_time) < max_wait:
        # Query database
        executions = query_audit_db(execution_id)
        
        # Update status
        workflow_steps = update_steps(executions)
        
        # Check completion
        if all_steps_completed(workflow_steps):
            return workflow_steps
        
        time.sleep(1)  # Poll ogni secondo
```

---

## 📊 Vantaggi delle Nuove Funzionalità

### ✅ Trasparenza
- L'utente vede esattamente cosa sta succedendo
- Nessuna "black box", tutto tracciato

### ✅ Auditabilità
- Ogni esecuzione ha un ID univoco
- Query SQL per recuperare dettagli completi
- Storico permanente nel database

### ✅ Debugging Facilitato
- Individuazione immediata di fallimenti
- Error messages visibili direttamente nell'UI
- Tempi di esecuzione per identificare colli di bottiglia

### ✅ Controllo Qualità (HITL)
- Validazione umana dei risultati AI
- Riduzione falsi positivi
- Feedback loop per migliorare il modello

---

## 🧪 Test Rapido

### 1. Invia Email di Test

Usa il POC Streamlit oppure:

```bash
curl -X POST http://localhost:9099/contentListener/fascicolo \
  -H "Content-Type: message/rfc822" \
  -H "X-Execution-ID: $(uuidgen)" \
  -d @examples/eml-samples/email_test.eml
```

### 2. Verifica Database Audit

```bash
docker exec postgres-db psql -U nifi -d nifi_audit -c "
SELECT 
    workflow_name,
    step_name,
    status,
    duration_ms,
    output_data->>'tipologia_provvedimento' as tipologia
FROM workflow_executions
WHERE execution_id = 'YOUR-UUID'
ORDER BY started_at;
"
```

### 3. Controlla Logs

```bash
docker-compose logs -f sp01-eml-parser | grep "classification"
```

---

## 🎯 Prossimi Miglioramenti Possibili

### 1. **Real-time Updates con WebSockets**
Sostituire polling con push notifications

### 2. **Dashboard Storico Esecuzioni**
Visualizzare tutte le esecuzioni passate con filtri

### 3. **Grafici Performance**
- Success rate per tipologia
- Tempi medi per fase
- Trend nel tempo

### 4. **Export Report**
- PDF con risultati classificazione
- Excel con storico esecuzioni
- JSON per integrazioni

### 5. **Notifiche Email**
Avvisare l'utente quando il workflow è completato

---

## 📚 File Modificati

- ✅ `src/frontend/poc_eml_to_hitl.py` - Implementazione tracking e HITL
- ✅ `src/requirements.txt` - Aggiunto `psycopg2-binary`
- ✅ `infrastructure/nifi-workflows/init-nifi-audit.sql` - Schema database
- ✅ `infrastructure/nifi-workflows/WORKFLOW-TRACKING-GUIDE.md` - Documentazione

---

## ✨ Conclusione

Il POC ora offre:

1. ✅ **Visibilità completa** del workflow
2. ✅ **Tracking real-time** con progress bar
3. ✅ **Risultati classificazione** visualizzati
4. ✅ **Checkpoint HITL** per validazione umana
5. ✅ **Database audit** per storico e debugging

Tutto è **tracciabile**, **auditabile** e **interattivo**! 🎉

---

**Prova subito:** http://localhost:8501
