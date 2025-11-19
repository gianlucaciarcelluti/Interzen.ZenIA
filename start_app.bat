@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python src\frontend\start_app.py
pause