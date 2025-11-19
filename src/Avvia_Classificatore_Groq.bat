@echo off
REM filepath: c:\GitHub\Interzen\Interzen.POC\ZenIA\src\Avvia_Classificatore_Groq.bat
REM Batch file per avviare il Classificatore Sinistri Groq
REM Doppio click per eseguire

cd /d "%~dp0\SP04\llm_classifier"
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "start_streamlit_groq.ps1"
pause