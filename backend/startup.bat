@echo off
REM startup.bat

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Initialize database
python init_db.py

REM Start the server
uvicorn main:app --reload