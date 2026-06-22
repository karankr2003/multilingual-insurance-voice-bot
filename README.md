# Multilingual Insurance Voice Bot

A production-ready voice bot for health insurance that supports 5 languages (English, Hindi, Marathi, Tamil, Kannada) with automatic language detection and dynamic switching.

## Features

✅ **Telephony Integration**: Twilio-based phone call routing  
✅ **Multilingual Support**: English, Hindi, Marathi, Tamil, Kannada  
✅ **Automatic Language Detection**: Detects and switches languages automatically  
✅ **Health Insurance Flow**: Complete conversation from greeting to policy recommendation  
✅ **AI Policy Recommendation**: Rule-based engine with personalized suggestions  
✅ **Session Transcripts**: Complete conversation logs with timestamps  
✅ **Containerized Deployment**: Docker support for easy deployment  

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Caller    │─────>│    Twilio    │─────>│  Flask App  │
│   (Phone)   │<─────│   Gateway    │<─────│  (Voice Bot)│
└─────────────┘      └──────────────┘      └─────────────┘
                                                    │
                                            ┌───────┴───────┐
                                            │               │
                                     ┌──────▼─────┐ ┌──────▼─────┐
                                     │  Policy    │ │  Session   │
                                     │  Engine    │ │  Manager   │
                                     └────────────┘ └────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Twilio account with phone number
- ngrok or similar tunneling service (for local testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/karankr2003/multilingual-insurance-voice-bot.git
cd multilingual-insurance-voice-bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required variables:
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number (format: +1234567890)

5. **Run the application**
```bash
python app.py
```

The bot will start on `http://0.0.0.0:5000`

### Local Testing with ngrok

1. **Start ngrok** (in a separate terminal)
```bash
ngrok http 5000
```

2. **Configure Twilio webhook**
   - Go to Twilio Console → Phone Numbers → Your Number
   - Under "Voice & Fax", set:
     - **A CALL COMES IN**: Webhook
     - **URL**: `https://your-ngrok-url.ngrok.io/voice`
     - **HTTP Method**: POST

3. **Call your Twilio number** and test the bot!

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker directly

```bash
# Build image
docker build -t insurance-voicebot .

# Run container
docker run -p 5000:5000 \
  -e TWILIO_ACCOUNT_SID=your_sid \
  -e TWILIO_AUTH_TOKEN=your_token \
  -e TWILIO_PHONE_NUMBER=your_number \
  -v $(pwd)/sessions:/app/sessions \
  insurance-voicebot
```

## Conversation Flow

1. **Greeting**: Bot greets in English by default
2. **Name Collection**: Asks for caller's name
3. **Language Detection**: Automatically detects language from first response
4. **Information Gathering**:
   - Age
   - City
   - Occupation
   - Medical conditions
   - Family medical history
   - Coverage preference
   - Hospital preference
   - Dependents
5. **Policy Recommendation**: AI-powered recommendation with explanation
6. **Closing**: Thank you message and hangup

## Language Support

| Language | Code | Example Phrase |
|----------|------|----------------|
| English  | en   | "What is your name?" |
| Hindi    | hi   | "आपका नाम क्या है?" |
| Marathi  | mr   | "तुमचे नाव काय आहे?" |
| Tamil    | ta   | "உங்கள் பெயர் என்ன?" |
| Kannada  | kn   | "ನಿಮ್ಮ ಹೆಸರೇನು?" |

### Language Switching

The bot automatically detects language changes during the conversation. No need to ask to switch - just speak in your preferred language!

## Policy Options

1. **HealthGuard Basic**
   - Coverage: ₹3 Lakhs
   - Best for: Young individuals, no pre-existing conditions

2. **HealthGuard Comprehensive**
   - Coverage: ₹10 Lakhs
   - Best for: Middle-aged, families

3. **HealthGuard Premium Plus**
   - Coverage: ₹25 Lakhs
   - Best for: Seniors, extensive coverage needs

4. **HealthGuard Family Shield**
   - Coverage: ₹15 Lakhs
   - Best for: Families with dependents

## Session Output

After each call, the system generates:

### 1. Console Output
```
================================================================================
SESSION COMPLETE: abc-123-def
================================================================================
Caller: John Doe
Age: 35
City: Mumbai
Occupation: Software Engineer

Recommendation:
  Policy: HealthGuard Comprehensive
  Coverage: ₹10 Lakhs
  Premium: ₹13200/year
  Reasons: it balances coverage and affordability...
  
Transcript saved to: sessions/session_20240622_143052_abc123.json
================================================================================
```

### 2. JSON Transcript
Located in `sessions/` directory:

```json
{
  "session_id": "abc-123-def",
  "call_sid": "CA1234567890",
  "start_time": "2024-06-22T14:30:52",
  "end_time": "2024-06-22T14:35:12",
  "languages_used": ["en", "hi"],
  "caller_data": {
    "name": "John Doe",
    "age": "35",
    "city": "Mumbai",
    ...
  },
  "conversation": [...],
  "recommendation": {...}
}
```

## Project Structure

```
.
├── app.py                  # Main Flask application
├── policy_engine.py        # Policy recommendation logic
├── session_manager.py      # Session and transcript management
├── language_detector.py    # Language detection
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker compose configuration
├── .env.example           # Environment variables template
├── .env                   # Your environment variables (not committed)
├── README.md              # This file
└── sessions/              # Session transcripts (auto-created)
```

## Testing

### Manual Testing

1. Call the Twilio phone number: **Your configured number**
2. Follow the conversation flow
3. Test language switching by speaking in different languages
4. Check `sessions/` directory for transcripts

### Expected Behavior

- Bot should respond within 2 seconds
- Language detection should happen within 1 second
- Complete conversation should take 3-5 minutes
- Transcript should be saved automatically

## Troubleshooting

### Issue: "Session error. Please call again."
**Solution**: Check that Flask app is running and ngrok tunnel is active

### Issue: Language not detecting properly
**Solution**: Speak clearly for first 5-10 words in your preferred language

### Issue: Twilio webhook not working
**Solution**: 
- Verify ngrok URL is correct in Twilio console
- Check Flask logs for errors
- Ensure port 5000 is accessible

### Issue: No transcript files
**Solution**: Check `sessions/` directory permissions

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| TWILIO_ACCOUNT_SID | Twilio account identifier | ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| TWILIO_AUTH_TOKEN | Twilio authentication token | your_auth_token_here |
| TWILIO_PHONE_NUMBER | Your Twilio phone number | +1234567890 |
| FLASK_ENV | Flask environment | production |
| PORT | Server port | 5000 |
| HOST | Server host | 0.0.0.0 |

## Production Deployment

### Cloud Deployment Options

1. **AWS EC2 / Azure VM**
   - Deploy Docker container
   - Configure security groups for port 5000
   - Use Elastic IP for stable webhook URL

2. **Heroku**
```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=xxx
heroku config:set TWILIO_AUTH_TOKEN=xxx
heroku config:set TWILIO_PHONE_NUMBER=xxx
git push heroku main
```

3. **Google Cloud Run**
```bash
gcloud run deploy insurance-voicebot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Performance

- **Latency**: < 300ms for audio processing
- **Response Time**: < 2 seconds for bot responses
- **Language Detection**: < 1 second
- **Concurrent Calls**: Supports multiple simultaneous calls

## Security

- Environment variables for sensitive credentials
- No hardcoded API keys
- Session data isolated per call
- Automatic session cleanup

## Future Enhancements

- [ ] Add voice biometrics for caller verification
- [ ] Integrate with CRM systems
- [ ] Add payment processing
- [ ] SMS follow-up with policy details
- [ ] Dashboard for analytics
- [ ] Support for more languages

## License

MIT License

## Support

For issues and questions:
- Create an issue in the repository
- Check logs in `sessions/` directory
- Review Twilio console for call logs

## Credits

Built with:
- Flask - Web framework
- Twilio - Telephony platform
- langdetect - Language detection
- Docker - Containerization

---

**Made with ❤️ for Insurance Companies**
