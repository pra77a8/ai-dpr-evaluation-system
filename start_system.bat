@echo off
REM Start AI DPR Evaluation System

echo Starting AI DPR Evaluation System...

REM Open a new command prompt for the backend
start "Backend Server" cmd /k "cd /d "%~dp0backend" && python -m uvicorn main:app --reload"

REM Wait a few seconds for the backend to start
timeout /t 5 /nobreak >nul

REM Open a new command prompt for the frontend
start "Frontend Server" cmd /k "cd /d "%~dp0" && npm run dev"

echo.
echo The AI DPR Evaluation System is starting...
echo.
echo Backend server will be available at: http://localhost:8000
echo Frontend server will be available at: http://localhost:3001
echo.
echo Please wait for both servers to finish starting up.
echo Once both are running, open your browser and navigate to http://localhost:3001
echo.
pause