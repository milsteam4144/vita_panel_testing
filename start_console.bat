@echo off
REM VITA Console Demo Startup Script for Windows
REM This script activates the virtual environment and starts the console demo

echo 🚀 Starting VITA Console Demo...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv venv
    echo ✅ Virtual environment created.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo ⚠️  Warning: OPENAI_API_KEY environment variable not set.
    echo    You may need to set it for full functionality.
)

REM Start the console demo
echo 🎓 Starting VITA Console Demo...
if exist "vita_console_demo.py" (
    python vita_console_demo.py
) else if exist "test.py" (
    echo 📊 Running test.py instead...
    panel serve test.py --autoreload
) else (
    echo ❌ Could not find console demo file to run.
    echo Available Python files:
    dir *.py
    pause
    exit /b 1
)

pause