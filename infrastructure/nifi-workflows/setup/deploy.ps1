# =========================================
# Apache NiFi Workflow Deployment Script (PowerShell)
# =========================================

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Deployment Apache NiFi - Provvedimenti Assistant" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# =========================================
# Step 1: Check Prerequisites
# =========================================

Write-Host "[1/8] Controllo prerequisiti..." -ForegroundColor Yellow

$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
$dockerComposeInstalled = Get-Command docker-compose -ErrorAction SilentlyContinue

if (-not $dockerInstalled) {
    Write-Host "❌ Docker non trovato. Installare Docker Desktop." -ForegroundColor Red
    exit 1
}

if (-not $dockerComposeInstalled) {
    Write-Host "❌ Docker Compose non trovato." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker e Docker Compose trovati" -ForegroundColor Green

# =========================================
# Step 2: Check .env file
# =========================================

Write-Host "[2/8] Verifica configurazione..." -ForegroundColor Yellow

if (-not (Test-Path .env)) {
    Write-Host "⚠️  File .env non trovato. Creo da template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "❌ IMPORTANTE: Modifica il file .env con le tue API keys prima di continuare!" -ForegroundColor Red
    Write-Host "   Esegui: notepad .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ File .env trovato" -ForegroundColor Green

# Load environment variables
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "env:$name" -Value $value
    }
}

# Check critical variables
if ([string]::IsNullOrEmpty($env:GROQ_API_KEY) -or $env:GROQ_API_KEY -eq "your_groq_api_key_here") {
    Write-Host "❌ GROQ_API_KEY non configurata nel file .env" -ForegroundColor Red
    Write-Host "   Ottieni una API key gratuita su: https://console.groq.com/keys" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Variabili d'ambiente configurate" -ForegroundColor Green

# =========================================
# Step 3: Stop existing containers
# =========================================

Write-Host "[3/8] Arresto container esistenti..." -ForegroundColor Yellow

docker-compose down -v 2>$null

Write-Host "✅ Container arrestati" -ForegroundColor Green

# =========================================
# Step 4: Build and Start Services
# =========================================

Write-Host "[4/8] Avvio servizi infrastrutturali..." -ForegroundColor Yellow

docker-compose up -d postgres redis zookeeper neo4j minio

Write-Host "Attendo 30 secondi per inizializzazione database..."
Start-Sleep -Seconds 30

Write-Host "✅ Servizi infrastrutturali avviati" -ForegroundColor Green

# =========================================
# Step 5: Verify Database
# =========================================

Write-Host "[5/8] Verifica database..." -ForegroundColor Yellow

$dbCheck = docker exec postgres-db psql -U postgres -d provvedimenti -c "SELECT COUNT(*) FROM templates;" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database inizializzato correttamente" -ForegroundColor Green
} else {
    Write-Host "❌ Errore inizializzazione database" -ForegroundColor Red
    exit 1
}

# =========================================
# Step 6: Start N8N
# =========================================

Write-Host "[6/8] Avvio N8N..." -ForegroundColor Yellow

docker-compose up -d n8n

Write-Host "Attendo 20 secondi per avvio N8N..."
Start-Sleep -Seconds 20

Write-Host "✅ N8N avviato" -ForegroundColor Green

# =========================================
# Step 7: Import Workflows
# =========================================

Write-Host "[7/8] Importazione workflows..." -ForegroundColor Yellow

$N8N_HOST = "http://localhost:5678"
$N8N_USER = $env:N8N_USER
$N8N_PASSWORD = $env:N8N_PASSWORD

# Create credentials
$pair = "$($N8N_USER):$($N8N_PASSWORD)"
$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($pair))
$basicAuthValue = "Basic $encodedCreds"

# Wait for N8N to be ready
$MAX_RETRIES = 10
$RETRY_COUNT = 0

while ($RETRY_COUNT -lt $MAX_RETRIES) {
    try {
        $response = Invoke-WebRequest -Uri "$N8N_HOST/healthz" -Headers @{Authorization=$basicAuthValue} -UseBasicParsing -ErrorAction SilentlyContinue
        Write-Host "✅ N8N pronto" -ForegroundColor Green
        break
    } catch {
        Write-Host "Attendo N8N... ($($RETRY_COUNT+1)/$MAX_RETRIES)"
        Start-Sleep -Seconds 5
        $RETRY_COUNT++
    }
}

if ($RETRY_COUNT -eq $MAX_RETRIES) {
    Write-Host "❌ Timeout connessione N8N" -ForegroundColor Red
    exit 1
}

# Import workflows
Write-Host "Importazione workflow globale..."
$globalWorkflow = Get-Content "WORKFLOW-GLOBALE-Orchestrator.json" -Raw
Invoke-RestMethod -Uri "$N8N_HOST/rest/workflows" `
                  -Method Post `
                  -Headers @{Authorization=$basicAuthValue; "Content-Type"="application/json"} `
                  -Body $globalWorkflow | Out-Null

Get-ChildItem -Filter "SP*.json" | ForEach-Object {
    Write-Host "Importazione $($_.Name)..."
    $workflowContent = Get-Content $_.FullName -Raw
    Invoke-RestMethod -Uri "$N8N_HOST/rest/workflows" `
                      -Method Post `
                      -Headers @{Authorization=$basicAuthValue; "Content-Type"="application/json"} `
                      -Body $workflowContent | Out-Null
}

Write-Host "✅ Workflows importati" -ForegroundColor Green

# =========================================
# Step 8: Start Application Services
# =========================================

Write-Host "[8/8] Avvio servizi applicativi..." -ForegroundColor Yellow

# Solo SP03 Knowledge Base e FAISS (SP04 è opzionale)
docker-compose up -d sp03-knowledge-base faiss-service

# SP04 Classifier è commentato nel docker-compose.yml (opzionale)
# Se necessario, decommentarlo e aggiungere qui

Write-Host "✅ Servizi applicativi avviati" -ForegroundColor Green
Write-Host "ℹ️  SP01, SP02, SP05, SP08 sono implementati come N8N workflows" -ForegroundColor Blue

# =========================================
# Summary
# =========================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ DEPLOYMENT COMPLETATO" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Servizi attivi:" -ForegroundColor White
Write-Host ""
Write-Host "  🔹 N8N Dashboard:       http://localhost:5678"
Write-Host "     Credentials:        $($env:N8N_USER) / $($env:N8N_PASSWORD)"
Write-Host ""
Write-Host "  🔹 PostgreSQL:          localhost:5432"
Write-Host "     Database:           provvedimenti"
Write-Host "     User:               postgres"
Write-Host ""
Write-Host "  🔹 Redis:               localhost:6379"
Write-Host ""
Write-Host "  🔹 ZooKeeper:           localhost:2181 (NiFi coordination)"
Write-Host ""
Write-Host "  🔹 Neo4j Browser:       http://localhost:7474"
Write-Host "     Credentials:        neo4j / $env:NEO4J_PASSWORD"
Write-Host ""
Write-Host "  🔹 MinIO Console:       http://localhost:9001"
Write-Host "     Credentials:        $env:MINIO_USER / $env:MINIO_PASSWORD"
Write-Host ""
Write-Host "  🔹 SP03 Knowledge Base: http://localhost:5003/docs"
Write-Host "     (RAG orchestration + FAISS vector search)"
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "📝 Architettura Ibrida N8N:" -ForegroundColor Blue
Write-Host ""
Write-Host "  ✅ Microservizi attivi:"
Write-Host "     - SP03: Knowledge Base (Python + FAISS)"
Write-Host "     - FAISS: Vector search service"
Write-Host ""
Write-Host "  🔄 N8N Workflows (importati):"
Write-Host "     - SP01: Template Engine (Groq + JS)"
Write-Host "     - SP02: Validator (Groq + JS rules)"
Write-Host "     - SP05: Quality Checker (LanguageTool API + JS NLP)"
Write-Host "     - SP08: Security Audit (JWT + blockchain)"
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Test del workflow globale:" -ForegroundColor Yellow
Write-Host ""
Write-Host 'Invoke-RestMethod -Uri "http://localhost:5678/webhook/workflow-globale" `' -ForegroundColor Gray
Write-Host '  -Method Post `' -ForegroundColor Gray
Write-Host '  -ContentType "application/json" `' -ForegroundColor Gray
Write-Host '  -Body (@{' -ForegroundColor Gray
Write-Host '    tipo_richiesta = "Autorizzazione Scarico Acque"' -ForegroundColor Gray
Write-Host '    dati_input = @{' -ForegroundColor Gray
Write-Host '      richiedente = "Azienda XYZ"' -ForegroundColor Gray
Write-Host '      indirizzo = "Via Roma 123"' -ForegroundColor Gray
Write-Host '      descrizione = "Scarico acque reflue industriali"' -ForegroundColor Gray
Write-Host '    }' -ForegroundColor Gray
Write-Host '  } | ConvertTo-Json)' -ForegroundColor Gray
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Per vedere i logs:" -ForegroundColor White
Write-Host "   docker-compose logs -f"
Write-Host ""
Write-Host "🛑 Per fermare tutto:" -ForegroundColor White
Write-Host "   docker-compose down"
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
