# Quick Setup Script for Windows
# Run this to download ngrok and setup everything

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Multilingual Voice Bot - Quick Setup" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some packages may have failed to install" -ForegroundColor Red
}

# Check if ngrok exists
Write-Host ""
Write-Host "Checking ngrok..." -ForegroundColor Yellow
$ngrokExists = Test-Path "ngrok.exe"

if (-not $ngrokExists) {
    Write-Host "❌ ngrok.exe not found in current directory" -ForegroundColor Red
    Write-Host ""
    Write-Host "Downloading ngrok..." -ForegroundColor Yellow
    
    try {
        # Download ngrok for Windows
        $ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        $zipPath = "ngrok.zip"
        
        Invoke-WebRequest -Uri $ngrokUrl -OutFile $zipPath
        
        # Extract
        Expand-Archive -Path $zipPath -DestinationPath . -Force
        Remove-Item $zipPath
        
        Write-Host "✅ ngrok downloaded successfully!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Failed to download ngrok automatically" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please download manually:" -ForegroundColor Yellow
        Write-Host "1. Visit: https://ngrok.com/download" -ForegroundColor Cyan
        Write-Host "2. Download Windows version" -ForegroundColor Cyan
        Write-Host "3. Extract ngrok.exe to: $PWD" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "Press Enter after downloading ngrok.exe to continue..."
    }
} else {
    Write-Host "✅ ngrok.exe found" -ForegroundColor Green
}

# Create sessions directory
Write-Host ""
Write-Host "Creating sessions directory..." -ForegroundColor Yellow
if (-not (Test-Path "sessions")) {
    New-Item -ItemType Directory -Path "sessions" | Out-Null
    Write-Host "✅ sessions/ directory created" -ForegroundColor Green
} else {
    Write-Host "✅ sessions/ directory exists" -ForegroundColor Green
}

# Check .env file
Write-Host ""
Write-Host "Checking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "❌ .env file not found! Creating from template..." -ForegroundColor Red
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file (please review and update if needed)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start Flask server:" -ForegroundColor Cyan
Write-Host "   python app.py" -ForegroundColor White
Write-Host ""
Write-Host "2. In another terminal, start ngrok:" -ForegroundColor Cyan
Write-Host "   .\ngrok.exe http 5000" -ForegroundColor White
Write-Host ""
Write-Host "3. Copy ngrok HTTPS URL and configure Twilio webhook:" -ForegroundColor Cyan
Write-Host "   https://console.twilio.com/" -ForegroundColor White
Write-Host ""
Write-Host "4. Call the bot:" -ForegroundColor Cyan
Write-Host "   +1 (860) 467-1351" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: SETUP_AND_TEST.md" -ForegroundColor Yellow
Write-Host ""
