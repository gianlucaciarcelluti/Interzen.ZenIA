@echo off
echo 🏛️ POC Generatore Determine Amministrative
echo ==========================================

:: Verifica se siamo nella directory corretta
if not exist "requirements.txt" (
    echo ❌ Eseguire lo script dalla directory src del progetto
    pause
    exit /b 1
)

:: Crea file .env se non esiste
if not exist ".env" (
    if exist ".env.example" (
        echo 📝 Creazione file .env...
        copy ".env.example" ".env" >nul
        echo ✅ File .env creato
    )
)

:: Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trovato. Installare Python 3.8+
    pause
    exit /b 1
)

:: Installa le dipendenze
echo 📦 Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Errore nell'installazione delle dipendenze
    pause
    exit /b 1
)

:: Verifica Ollama
echo 🔍 Verifica connessione Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama non risponde su http://localhost:11434
    echo 💡 Assicurati che Ollama sia in esecuzione:
    echo    ollama serve
    echo.
    echo Continuare comunque? (s/n)
    set /p choice=
    if /i not "%choice%"=="s" (
        pause
        exit /b 1
    )
) else (
    echo ✅ Ollama connesso
)

:: Avvia l'applicazione
echo.
echo 🚀 Avvio applicazione Streamlit...
echo 🌐 L'applicazione sarà disponibile su: http://localhost:8501
echo.
echo ⏳ Avvio in corso...
timeout /t 3 >nul

:: Avvia Streamlit
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false --theme.base light

pause
