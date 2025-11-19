# Troubleshooting - MS05-TRANSFORMER

## Panoramica Troubleshooting

Questa guida fornisce flussi diagnostici e soluzioni per i problemi più comuni nel microservizio MS05-TRANSFORMER.

## Flussi Diagnostici

### Flusso: Trasformazione Fallita

```mermaid
flowchart TD
    A[Ricevuta segnalazione<br/>trasformazione fallita] --> B{Controlla stato job<br/>in database}
    B --> C{Job esiste?}
    C -->|No| D[Errore: Job ID non trovato<br/>Verifica ID fornito]
    C -->|Sì| E{Stato job}
    E -->|FAILED| F[Controlla job_logs<br/>per dettagli errore]
    E -->|PENDING| G[Controlla queue Redis<br/>e worker attivi]
    E -->|PROCESSING| H[Tempo > timeout?<br/>300 secondi]
    H -->|Sì| I[Kill job, marca FAILED<br/>Controlla risorse worker]
    H -->|No| J[Attendi completamento<br/>o aumenta timeout]

    F --> K{Analizza errore<br/>in log}
    K -->|Formato non supportato| L[Verifica formati supportati<br/>in /api/v1/formats]
    K -->|File corrotto| M[Controlla checksum<br/>documento originale]
    K -->|Timeout| N[Aumenta timeout<br/>o ottimizza documento]
    K -->|Memoria insufficiente| O[Aumenta risorse worker<br/>o limita concorrenza]

    G --> P{Worker attivi?}
    P -->|No| Q[Riavvia worker<br/>controlla configurazione]
    P -->|Sì| R{Queue depth<br/>normale?}
    R -->|No| S[Scala orizzontalmente<br/>aggiungi worker]
    R -->|Sì| T[Controlla configurazione<br/>queue e priorità]
```

### Flusso: Performance Degradate

```mermaid
flowchart TD
    A[Segnalazione performance<br/>degradate] --> B[Raccogli metriche<br/>sistema e applicazione]
    B --> C{Analizza throughput<br/>trasformazioni/minuto}
    C -->|< 50/min| D[Identifica bottleneck<br/>CPU/Memoria/IO]
    C -->|50-100/min| E[Controlla configurazione<br/>worker e concorrenza]
    C -->|> 100/min| F[Performance normale<br/>verifica aspettative]

    D --> G{CPU > 80%?}
    G -->|Sì| H[Riduci concorrenza<br/>ottimizza algoritmi]
    G -->|No| I{Memoria > 85%?}
    I -->|Sì| J[Aumenta RAM<br/>ottimizza memory usage]
    I -->|No| K{IO > 90%?}
    K -->|Sì| L[Migra storage<br/>ottimizza caching]

    E --> M{Concorrenza<br/>ottimale?}
    M -->|No| N[Regola GUNICORN_WORKERS<br/>e THREADS]
    M -->|Sì| O[Controlla configurazione<br/>Redis pool]

    F --> P[Documenta baseline<br/>aggiorna monitoring]
```

### Flusso: Errori Connessione Database

```mermaid
flowchart TD
    A[Errore connessione<br/>PostgreSQL] --> B[Test connessione<br/>manuale al DB]
    B --> C{Connessione OK?}
    C -->|No| D[Controlla network<br/>e firewall]
    C -->|Sì| E{Database esiste?}
    E -->|No| F[Crea database<br/>esegui init script]
    E -->|Sì| G{Utente ha permessi?}
    G -->|No| H[Verifica GRANT<br/>in PostgreSQL]
    G -->|Sì| I{Connection pool<br/>esaurito?}
    I -->|Sì| J[Aumenta pool size<br/>ottimizza query]
    I -->|No| K[Controlla configurazione<br/>DATABASE_URL]

    D --> L{Port 5432<br/>accessibile?}
    L -->|No| M[Apri firewall<br/>verifica security groups]
    L -->|Sì| N[Controlla DNS<br/>e risoluzione hostname]

    K --> O[Verifica variabili<br/>ambiente in container]
    O --> P[Confronta con<br/>docker-compose.yml]
```

## Problemi Comuni e Soluzioni

### 1. Trasformazioni PDF Fallite

**Sintomi**:
- Errori "PDF parsing failed"
- Trasformazioni che rimangono in stato PROCESSING
- Log mostrano "Invalid PDF structure"

**Soluzioni**:
```bash
# Verifica integrità PDF
pdfinfo documento.pdf

# Controlla se PDF è protetto
qpdf --check documento.pdf

# Prova riparazione PDF
qpdf documento.pdf repaired.pdf
```

**Configurazione**:
```yaml
# In docker-compose.yml
environment:
  - PDF_PARSER_STRICT=false
  - PDF_REPAIR_ENABLED=true
  - MAX_PDF_SIZE=10485760
```

### 2. Timeout Trasformazioni

**Sintomi**:
- Job marcati come FAILED dopo 300 secondi
- Log mostrano "Processing timeout"
- Documenti di grandi dimensioni falliscono

**Soluzioni**:
```yaml
# Aumenta timeout per documenti grandi
environment:
  - TRANSFORMATION_TIMEOUT_DEFAULT=600
  - MAX_DOCUMENT_SIZE=20971520
  - GUNICORN_TIMEOUT=600
```

**Ottimizzazioni**:
- Comprimere documenti prima dell'upload
- Suddividere documenti molto grandi
- Utilizzare trasformazione asincrona per documenti >5MB

### 3. Memoria Insufficiente

**Sintomi**:
- Worker crashano con "Out of memory"
- Performance degradano gradualmente
- Log mostrano "Memory allocation failed"

**Soluzioni**:
```yaml
# Aumenta risorse container
services:
  ms05-transformer:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

# Riduci concorrenza
environment:
  - GUNICORN_WORKERS=2
  - MAX_CONCURRENT_JOBS=25
```

### 4. Code Redis Piena

**Sintomi**:
- Nuovi job rimangono in PENDING
- Latenza alta per accettazione job
- Metriche mostrano queue_depth > 100

**Soluzioni**:
```yaml
# Scala orizzontalmente
services:
  ms05-transformer:
    scale: 3

# Aumenta risorse Redis
redis-transformer:
  deploy:
    resources:
      limits:
        memory: 512M
```

### 5. Errori Conversione Formato

**Sintomi**:
- Trasformazioni DOCX→PDF falliscono
- Caratteri speciali corrotti
- Layout non preservato

**Soluzioni**:
```yaml
# Aggiorna librerie conversione
environment:
  - LIBREOFFICE_ENABLED=true
  - FONT_EMBEDDING=true
  - IMAGE_QUALITY=0.95
```

## Monitoraggio e Alert

### Metriche Chiave da Monitorare

```yaml
# Prometheus metrics
transformation_success_rate{job="ms05-transformer"} < 0.95
transformation_processing_time{job="ms05-transformer"} > 60
queue_depth{job="ms05-transformer"} > 50
memory_usage{job="ms05-transformer"} > 0.85
cpu_usage{job="ms05-transformer"} > 0.80
```

### Log Pattern da Cercare

```bash
# Errori critici
grep "CRITICAL\|ERROR" /app/logs/transformer.log

# Timeout
grep "timeout\|Timeout" /app/logs/transformer.log

# Memory issues
grep "MemoryError\|OutOfMemory" /app/logs/transformer.log

# Database connection issues
grep "connection\|Connection" /app/logs/transformer.log
```

## Comandi Diagnostici

### Verifica Stato Servizio

```bash
# Health check
curl -f http://ms05-transformer:8005/api/v1/health

# Metrics
curl http://ms05-transformer:8005/api/v1/metrics

# Database connection
docker exec ms05-transformer pg_isready -h postgres-transformer -U transformer_user
```

### Analisi Performance

```bash
# CPU e memoria
docker stats ms05-transformer

# Redis queue status
docker exec redis-transformer redis-cli LLEN transformer:queue

# Database connections
docker exec postgres-transformer psql -U transformer_user -d transformer_db -c "SELECT count(*) FROM pg_stat_activity;"
```

### Log Analysis

```bash
# Ultimi errori
docker logs ms05-transformer --tail 100 | grep ERROR

# Job specifici
docker logs ms05-transformer | grep "job_id=550e8400-e29b-41d4-a716-446655440000"

# Performance summary
docker logs ms05-transformer | grep "processing_time" | awk '{sum+=$2} END {print "Avg:", sum/NR}'
```

## Recovery Procedures

### Recovery da Crash Worker

```bash
# 1. Verifica stato
docker ps | grep ms05-transformer

# 2. Riavvia container
docker restart ms05-transformer

# 3. Controlla recovery job
curl http://ms05-transformer:8005/api/v1/status/{job_id}

# 4. Se necessario, retry manuale
curl -X POST http://ms05-transformer:8005/api/v1/admin/retry/{job_id}
```

### Recovery da Perdita Database

```bash
# 1. Stop servizio
docker stop ms05-transformer

# 2. Restore da backup
docker exec postgres-transformer pg_restore -U transformer_user -d transformer_db /backup/latest.dump

# 3. Verifica integrità
docker exec postgres-transformer psql -U transformer_user -d transformer_db -c "SELECT count(*) FROM transformation_jobs;"

# 4. Riavvia servizio
docker start ms05-transformer
```

### Emergency Procedures

#### Arresto di Emergenza
```bash
# Stop immediato tutti i servizi
docker-compose down --timeout 10

# Kill forzato se necessario
docker kill $(docker ps -q --filter name=ms05)
```

#### Modalità Maintenance
```yaml
# Configurazione maintenance
environment:
  - MAINTENANCE_MODE=true
  - ALLOWED_CLIENTS=admin_only
```

## Prevenzione Problemi

### Best Practices

1. **Monitoring Proattivo**
   - Alert su metriche chiave
   - Dashboard real-time
   - Log aggregation centralizzato

2. **Capacity Planning**
   - Monitoraggio trend utilizzo
   - Scaling automatico basato su metriche
   - Backup e disaster recovery testati

3. **Code Quality**
   - Test automatizzati per nuove funzionalità
   - Code review obbligatorie
   - Dependency scanning regolare

### Checklist Manutenzione Settimanale

- [ ] Verifica spazio disco (>20% libero)
- [ ] Controllo backup database
- [ ] Aggiornamento dipendenze sicurezza
- [ ] Analisi log per pattern anomali
- [ ] Test performance baseline
- [ ] Verifica configurazione monitoring

## Contatti Supporto

- **Team Sviluppo**: dev@zen-ia.it
- **Supporto Operativo**: ops@zen-ia.it
- **Security**: security@zen-ia.it
- **Documentazione**: docs@zen-ia.it