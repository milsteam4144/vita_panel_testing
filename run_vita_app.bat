@echo off
setlocal

:: Check for environment variables
if "%GITHUB_CLIENT_ID%"=="" (
    echo [ERROR] GITHUB_CLIENT_ID is not set.
    goto :exit
)

if "%GITHUB_CLIENT_SECRET%"=="" (
    echo [ERROR] GITHUB_CLIENT_SECRET is not set.
    goto :exit
)

:: Install dependencies from requirements.txt
echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    goto :exit
)

:: Start the Panel app
echo Starting VITA Assistant...
panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
goto :eof

:exit
echo Please set the required environment variables:
echo   set GITHUB_CLIENT_ID=your_client_id
echo   set GITHUB_CLIENT_SECRET=your_client_secret
pause
