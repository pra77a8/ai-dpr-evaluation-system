@echo off
REM Start AI DPR Evaluation System - Fixed Version

echo Starting AI DPR Evaluation System...

REM Get the current directory
set CURRENT_DIR=%~dp0

REM Remove trailing backslash
set CURRENT_DIR=%CURRENT_DIR:~0,-1%

REM Open a new command prompt for the backend
start "Backend Server" cmd /k "cd /d \"%CURRENT_DIR%\backend\" && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a few seconds for the backend to start
timeout /t 5 /nobreak >nul

REM Open a new command prompt for the frontend
start "Frontend Server" cmd /k "cd /d \"%CURRENT_DIR%\" && npm run dev"

echo.
echo The AI DPR Evaluation System is starting...
echo.
echo Backend server will be available at: http://localhost:8000
echo Frontend server will be available at: http://localhost:5173
echo.
echo Please wait for both servers to finish starting up.
echo Once both are running, open your browser and navigate to http://localhost:5173
echo.
pause