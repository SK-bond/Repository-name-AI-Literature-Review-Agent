@echo off
cd /d "%~dp0"

echo Starting AI Literature Review Agent...
echo.

start "FastAPI Backend" cmd /k ".\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload"

timeout /t 5 /nobreak >nul

start "Streamlit Website" cmd /k ".\.venv\Scripts\python.exe -m streamlit run frontend\app.py"

exit