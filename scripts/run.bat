@echo off
echo ===========================================
echo Multilingual Insurance Voice Bot
echo ===========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please create .env file from .env.example
    echo Run: copy .env.example .env
    echo Then edit .env with your credentials
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create sessions directory
if not exist sessions mkdir sessions

echo.
echo Setup complete!
echo.
echo Starting voice bot server...
echo Server will be available at: http://localhost:5000
echo.
echo IMPORTANT: You need to expose this server using ngrok or similar
echo    In another terminal, run: ngrok http 5000
echo    Then configure the ngrok URL in Twilio webhook settings
echo.
echo Press Ctrl+C to stop the server
echo ===========================================
echo.

REM Run the application
python app.py
