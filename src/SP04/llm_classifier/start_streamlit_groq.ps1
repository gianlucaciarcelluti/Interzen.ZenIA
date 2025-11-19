# Script PowerShell per avviare il POC Streamlit Groq Classifier
# Esegui con: .\start_streamlit_groq.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Avvio Classificatore Sinistri Groq" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se il virtual environment e' attivato
$venvActivated = $env:VIRTUAL_ENV

if ([string]::IsNullOrEmpty($venvActivated)) {
    Write-Host "Virtual environment Python non attivato!" -ForegroundColor Yellow
    
    # Cerca il venv nella root del progetto (llm_classifier -> SP04 -> src -> ZenIA)
    $venvPath = Join-Path $PSScriptRoot "..\..\..\.venv\Scripts\Activate.ps1"
    
    if (Test-Path $venvPath) {
        Write-Host "Attivazione automatica del virtual environment..." -ForegroundColor Cyan
        & $venvPath
        Write-Host "Virtual environment attivato!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "Virtual environment non trovato" -ForegroundColor Red
        Write-Host "Percorso cercato: $venvPath" -ForegroundColor Yellow
        Write-Host "Crealo nella root del progetto (ZenIA) con: python -m venv .venv" -ForegroundColor Cyan
        Write-Host "Oppure attivalo manualmente con: .venv\Scripts\Activate.ps1" -ForegroundColor Cyan
        Write-Host "Oppure premi un tasto per continuare comunque..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        Write-Host ""
    }
} else {
    Write-Host "Virtual environment attivato: $venvActivated" -ForegroundColor Green
    Write-Host ""
}

# Controlla se Streamlit e' installato
$streamlitInstalled = Get-Command streamlit -ErrorAction SilentlyContinue

if (-not $streamlitInstalled) {
    Write-Host "Streamlit non trovato!" -ForegroundColor Red
    Write-Host "Installalo con: pip install streamlit" -ForegroundColor Yellow
    exit 1
}

# Controlla se il file esiste
if (-not (Test-Path "streamlit_groq_classifier.py")) {
    Write-Host "File streamlit_groq_classifier.py non trovato!" -ForegroundColor Red
    Write-Host "Assicurati di essere nella directory corretta (src\llm_classifier)" -ForegroundColor Yellow
    exit 1
}

# Controlla variabile ambiente GROQ_API_KEY
$groqApiKey = [System.Environment]::GetEnvironmentVariable("GROQ_API_KEY")

if ([string]::IsNullOrEmpty($groqApiKey)) {
    Write-Host "GROQ_API_KEY non trovata nelle variabili d'ambiente" -ForegroundColor Yellow
    Write-Host "Potrai inserirla nell'interfaccia web" -ForegroundColor Cyan
} else {
    Write-Host "GROQ_API_KEY trovata" -ForegroundColor Green
}

Write-Host ""
Write-Host "Avvio applicazione Streamlit..." -ForegroundColor Green
Write-Host "L'app si aprira' automaticamente nel browser" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Premi Ctrl+C per fermare l'applicazione" -ForegroundColor Yellow
Write-Host ""

# Avvia Streamlit
streamlit run streamlit_groq_classifier.py
