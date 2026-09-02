@echo off
echo ==========================================
echo Starting NutriBudget AI...
echo ==========================================

echo [1/2] Starting Backend Server (FastAPI on port 8000)...
start "NutriBudget Backend" cmd /k "cd backend && .\venv\Scripts\python app.py"

echo [2/2] Starting Frontend Server (Vite on port 5173)...
start "NutriBudget Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are launching in new windows!
echo Please wait a few seconds for them to load, then open your browser to:
echo http://localhost:5173
echo.
echo (To stop the servers later, simply close the two command prompt windows that just opened)
echo.
pause
