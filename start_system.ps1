# Start AI DPR Evaluation System

Write-Host "Starting AI DPR Evaluation System..." -ForegroundColor Green

# Start the backend server in a new PowerShell window
# Start the backend server in a new PowerShell window
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backendPath = Join-Path $scriptPath "backend"

Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python -m uvicorn main:app --reload --port 8000" -WindowStyle Normal

# Wait a few seconds for the backend to start
Start-Sleep -Seconds 5

# Start the frontend server in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath'; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "The AI DPR Evaluation System is starting..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend server will be available at: http://localhost:3001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please wait for both servers to finish starting up." -ForegroundColor Yellow
Write-Host "Once both are running, open your browser and navigate to http://localhost:3001" -ForegroundColor Yellow
Write-Host ""