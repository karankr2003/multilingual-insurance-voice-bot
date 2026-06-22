# Complete Deployment Guide

## 🚀 Quick Deploy (5 Minutes)

### Prerequisites Checklist:
- ✅ Python 3.11+ installed
- ✅ pip package manager
- ✅ Twilio account (credentials provided)
- ✅ ngrok installed (for local testing)

---

## Method 1: Local Development (Recommended for Testing)

### Step 1: Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

The `.env` file should contain your Twilio credentials:
```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_phone_number_here
```

### Step 3: Start Application

```bash
python app.py
```

Expected output:
```
Starting voice bot on 0.0.0.0:5000
Twilio phone number: Your configured number
 * Running on http://0.0.0.0:5000
```

### Step 4: Expose with ngrok

```bash
# In a new terminal
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Step 5: Configure Twilio Webhook

1. Visit: https://console.twilio.com/
2. Navigate: Phone Numbers → Manage → Active Numbers
3. Click on: **Your phone number**
4. Under "Voice Configuration":
   - **A CALL COMES IN**: Webhook
   - **URL**: `https://your-ngrok-url.ngrok.io/voice`
   - **HTTP Method**: POST
5. Save configuration

### Step 6: Test

Call **+1 (860) 467-1351** and interact with the bot!

---

## Method 2: Docker Deployment

### Quick Start:

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f voicebot

# Stop
docker-compose down
```

### Manual Docker:

```bash
# Build image
docker build -t insurance-voicebot:latest .

# Run container
docker run -d \
  --name voicebot \
  -p 5000:5000 \
  -v $(pwd)/sessions:/app/sessions \
  -e TWILIO_ACCOUNT_SID=your_account_sid \
  -e TWILIO_AUTH_TOKEN=your_auth_token \
  -e TWILIO_PHONE_NUMBER=your_phone_number \
  insurance-voicebot:latest

# View logs
docker logs -f voicebot

# Stop
docker stop voicebot
docker rm voicebot
```

---

## Method 3: Cloud Deployment

### AWS EC2 Deployment

#### 1. Launch EC2 Instance:
```bash
# Instance type: t2.small or larger
# OS: Ubuntu 22.04 LTS
# Security Group: Allow inbound on port 5000 (or 80/443)
```

#### 2. Connect and Setup:
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Clone repository
git clone https://github.com/yourusername/insurance-voicebot.git
cd insurance-voicebot
```

#### 3. Deploy:
```bash
# Create .env file
nano .env
# Paste your environment variables

# Start application
sudo docker-compose up -d

# Check status
sudo docker-compose ps
```

#### 4. Configure Twilio:
- Webhook URL: `http://your-ec2-public-ip:5000/voice`

### Heroku Deployment

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-insurance-bot

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_account_sid
heroku config:set TWILIO_AUTH_TOKEN=your_auth_token
heroku config:set TWILIO_PHONE_NUMBER=your_phone_number

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Configure Twilio
# Webhook URL: https://your-insurance-bot.herokuapp.com/voice
```

### Google Cloud Run

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project your-project-id

# Deploy
gcloud run deploy insurance-voicebot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TWILIO_ACCOUNT_SID=your_account_sid \
  --set-env-vars TWILIO_AUTH_TOKEN=your_auth_token \
  --set-env-vars TWILIO_PHONE_NUMBER=your_phone_number

# Get URL
gcloud run services describe insurance-voicebot \
  --region us-central1 \
  --format 'value(status.url)'

# Configure Twilio with Cloud Run URL
```

### Azure App Service

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name insurance-bot-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name insurance-bot-plan \
  --resource-group insurance-bot-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group insurance-bot-rg \
  --plan insurance-bot-plan \
  --name your-insurance-bot \
  --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set \
  --resource-group insurance-bot-rg \
  --name your-insurance-bot \
  --settings \
    TWILIO_ACCOUNT_SID=your_account_sid \
    TWILIO_AUTH_TOKEN=your_auth_token \
    TWILIO_PHONE_NUMBER=your_phone_number

# Deploy
az webapp up \
  --resource-group insurance-bot-rg \
  --name your-insurance-bot \
  --runtime PYTHON:3.11

# Get URL
# https://your-insurance-bot.azurewebsites.net/voice
```

---

## Testing Guide

### Automated Component Testing:

```bash
python test_bot.py
```

Expected output:
```
================================================================================
MULTILINGUAL INSURANCE VOICE BOT - COMPONENT TESTS
================================================================================

================================================================================
TESTING POLICY ENGINE
================================================================================

Test Case 1 - Young Professional:
  Recommended: HealthGuard Basic
  Coverage: ₹3 Lakhs
  Premium: ₹5500/year
  ...

✅ Policy Engine tests completed successfully!
✅ Language Detector tests completed!
✅ Session Manager tests completed!

================================================================================
ALL TESTS PASSED ✅
================================================================================
```

### Manual Testing Script:

**Call**: +1 (860) 467-1351

**Test 1: English Flow**
```
Bot: "Hello! What is your name?"
You: "My name is John"

Bot: "Thank you John. How old are you?"
You: "35"

Bot: "Which city do you live in?"
You: "Mumbai"

... continue through all questions ...
```

**Test 2: Hindi Flow**
```
Bot: "Hello! What is your name?"
You: "मेरा नाम राहुल है" (My name is Rahul)

Bot: (switches to Hindi) "धन्यवाद राहुल। आपकी उम्र क्या है?"
You: "मैं 35 साल का हूं"

... bot continues in Hindi ...
```

**Test 3: Language Switching**
```
Bot: "Hello! What is your name?"
You: "My name is Priya"

Bot: "Thank you Priya. How old are you?"
You: "मैं 28 साल की हूं" (I am 28 years old - in Hindi)

Bot: (detects Hindi, switches) "समझ गया। आप किस शहर में रहती हैं?"
... continues in Hindi ...
```

### Verification Checklist:

After testing, verify:
- [ ] Call connects successfully
- [ ] Bot greeting is clear
- [ ] Speech recognition works
- [ ] Language detection is automatic
- [ ] Language switching is seamless
- [ ] All 8 questions are asked
- [ ] Policy recommendation is given
- [ ] Explanation is provided
- [ ] Transcript is saved in sessions/
- [ ] Console shows session summary

---

## Monitoring & Logs

### View Application Logs:

**Local**:
```bash
# Logs are printed to console
# Check sessions/ directory for transcripts
```

**Docker**:
```bash
docker logs -f voicebot
```

**Cloud**:
```bash
# Heroku
heroku logs --tail

# AWS CloudWatch
aws logs tail /aws/elasticbeanstalk/your-app

# Google Cloud
gcloud logging read "resource.type=cloud_run_revision"

# Azure
az webapp log tail --name your-insurance-bot --resource-group insurance-bot-rg
```

### Health Check:

```bash
# Check if service is running
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","service":"multilingual-insurance-voicebot"}
```

### Session Transcripts:

```bash
# View latest session
ls -ltr sessions/ | tail -1

# Read session content
cat sessions/session_20240622_143052_abc123.json

# Count total sessions
ls sessions/ | wc -l
```

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Environment variable missing"

**Solution**:
```bash
# Verify .env file exists
cat .env

# Check variables are loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('TWILIO_ACCOUNT_SID'))"
```

### Issue: Twilio webhook not working

**Solution**:
1. Check Flask is running: `curl http://localhost:5000/health`
2. Check ngrok is running: `curl http://127.0.0.1:4040/api/tunnels`
3. Verify Twilio webhook URL matches ngrok URL
4. Check Flask logs for incoming requests

### Issue: Language not detecting

**Solution**:
- Speak clearly for first 5-10 words
- Use common keywords in your language
- Check langdetect is installed: `pip show langdetect`

### Issue: Poor audio quality

**Solution**:
- Check internet connection
- Use a good quality phone/microphone
- Speak in a quiet environment
- Verify Twilio account has sufficient balance

---

## Performance Tuning

### Optimize Response Time:

```python
# In app.py, reduce timeout
speech_timeout='auto'  # Default
speech_timeout='3'      # Faster (3 seconds)
```

### Scale Horizontally:

```bash
# Run multiple instances with load balancer
# Instance 1
PORT=5001 python app.py

# Instance 2
PORT=5002 python app.py

# Instance 3
PORT=5003 python app.py

# Use nginx/HAProxy for load balancing
```

### Database Integration (Production):

```python
# Replace session_manager.py filesystem storage with:
# - PostgreSQL for relational data
# - MongoDB for JSON documents
# - Redis for real-time sessions
```

---

## Security Hardening

### Production Checklist:

- [ ] Use HTTPS (not HTTP)
- [ ] Enable Twilio signature validation
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Encrypt sensitive data
- [ ] Regular security updates
- [ ] Monitor for abuse
- [ ] Backup session data
- [ ] GDPR compliance
- [ ] PII anonymization

### Enable Twilio Signature Validation:

```python
# In app.py, add:
from twilio.request_validator import RequestValidator

@app.before_request
def validate_twilio_request():
    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    url = request.url
    params = request.form
    signature = request.headers.get('X-Twilio-Signature', '')
    
    if not validator.validate(url, params, signature):
        abort(403)
```

---

## Cost Estimation

### Twilio Costs (Approximate):
- **Incoming calls**: $0.0085/minute
- **Speech Recognition**: $0.02/minute
- **Text-to-Speech**: $0.06/minute
- **Total per minute**: ~$0.09/minute
- **Total per 5-minute call**: ~$0.45

### Cloud Hosting (Monthly):
- **AWS EC2 t2.small**: ~$17/month
- **Heroku Hobby**: $7/month
- **Google Cloud Run**: Pay-per-use (~$5-20/month)
- **Azure App Service B1**: ~$13/month

### Estimated Total for 1000 calls/month:
- Twilio: $450 (1000 calls × 5 min × $0.09)
- Hosting: $20
- **Total**: ~$470/month

---

## Backup & Recovery

### Backup Sessions:

```bash
# Manual backup
tar -czf sessions_backup_$(date +%Y%m%d).tar.gz sessions/

# Automated daily backup (cron)
0 2 * * * tar -czf /backups/sessions_$(date +\%Y\%m\%d).tar.gz /app/sessions/
```

### Restore Sessions:

```bash
tar -xzf sessions_backup_20240622.tar.gz
```

---

## Next Steps After Deployment

1. ✅ **Test thoroughly** with all 5 languages
2. ✅ **Monitor logs** for errors
3. ✅ **Review transcripts** for accuracy
4. ✅ **Optimize prompts** based on user feedback
5. ✅ **Add analytics** dashboard
6. ✅ **Scale infrastructure** as needed
7. ✅ **Document learnings** for improvements

---

**Your bot is ready for production! 🎉**

For support, refer to:
- README.md - General documentation
- QUICKSTART.md - 5-minute setup guide
- ARCHITECTURE.md - System design details
- This file - Deployment guide
