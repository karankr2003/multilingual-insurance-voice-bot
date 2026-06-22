# Quick Start Guide - 5 Minutes to Running Bot

## Step 1: Install Dependencies (1 minute)

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Configure Environment (1 minute)

Create `.env` file with your Twilio credentials:
```bash
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_phone_number_here
COHERE_API_KEY=your_cohere_api_key_here  # Optional
```

## Step 3: Test Components (30 seconds)

```bash
python test_bot.py
```

You should see:
```
✅ Policy Engine tests completed successfully!
✅ Language Detector tests completed!
✅ Session Manager tests completed!
ALL TESTS PASSED ✅
```

## Step 4: Start Server (10 seconds)

```bash
python app.py
```

You should see:
```
Starting voice bot on 0.0.0.0:5000
Twilio phone number: Your configured number
 * Running on http://0.0.0.0:5000
```

## Step 5: Expose with ngrok (2 minutes)

### Install ngrok:
- Download from: https://ngrok.com/download
- Or: `choco install ngrok` (Windows) / `brew install ngrok` (Mac)

### Run ngrok:
```bash
ngrok http 5000
```

You'll see:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:5000
```

## Step 6: Configure Twilio Webhook (1 minute)

1. Go to: https://console.twilio.com/
2. Phone Numbers → Manage → Active Numbers
3. Click on: Your phone number
4. Under "Voice Configuration":
   - A CALL COMES IN: **Webhook**
   - URL: `https://your-ngrok-url.ngrok.io/voice` (paste your ngrok URL)
   - HTTP: **POST**
5. Click **Save**

## Step 7: Test the Bot! 🎉

Call: **+1 (860) 467-1351**

### Test Script:

**Bot**: "Hello! Welcome to our health insurance service. What is your name?"  
**You**: "My name is John"

**Bot**: "Thank you John. How old are you?"  
**You**: "I am 35 years old"

**Bot**: "Got it. Which city do you live in?"  
**You**: "Mumbai"

**Bot**: "Thank you. What is your occupation?"  
**You**: "Software Engineer"

**Bot**: "Do you have any pre-existing medical conditions?"  
**You**: "No"

**Bot**: "Does your family have any history of chronic diseases?"  
**You**: "No"

**Bot**: "What coverage amount are you looking for?"  
**You**: "Comprehensive"

**Bot**: "Do you prefer government hospitals, private hospitals, or both?"  
**You**: "Private"

**Bot**: "Do you want to include dependents in your coverage?"  
**You**: "No"

**Bot**: Gives recommendation and explanation!

### Test Language Switching:

Try answering in Hindi after starting in English:
- "मेरा नाम राहुल है" (My name is Rahul)
- Bot will automatically switch to Hindi!

## Verify Success:

1. **Check console** - You'll see session details printed
2. **Check sessions/ folder** - JSON transcript file created
3. **Check ngrok dashboard** - http://127.0.0.1:4040 (see HTTP requests)

## Docker Alternative (2 minutes)

```bash
# Build and run
docker-compose up --build

# In another terminal, run ngrok
ngrok http 5000
```

## Troubleshooting:

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Environment variable missing" error
- Check .env file exists
- Verify all variables are set

### "Connection refused" in Twilio
- Ensure Flask app is running
- Verify ngrok tunnel is active
- Check webhook URL in Twilio console

### Language not detecting
- Speak clearly for first few words
- Try keyword like "मेरा नाम" for Hindi

## What's Happening:

1. **You call** → Twilio receives call
2. **Twilio** → Sends request to your ngrok URL
3. **ngrok** → Forwards to Flask app (localhost:5000)
4. **Flask app** → Processes voice, detects language, recommends policy
5. **Response** → Goes back through ngrok → Twilio → You hear it!

## Session Output:

After call ends, check console:

```
================================================================================
SESSION COMPLETE: abc-123-def
================================================================================
Caller: John
Age: 35
City: Mumbai
...
Recommendation: HealthGuard Comprehensive
================================================================================
```

And check `sessions/` folder for complete JSON transcript!

## Next Steps:

- ✅ Test with different languages (Hindi, Marathi, Tamil, Kannada)
- ✅ Test language switching mid-conversation
- ✅ Review session transcripts in sessions/ folder
- ✅ Customize policy options in policy_engine.py
- ✅ Deploy to cloud (AWS, Azure, Heroku)

## Support:

- Check README.md for detailed documentation
- Review test_bot.py for component tests
- Check Flask logs for errors
- Visit ngrok dashboard: http://127.0.0.1:4040

---

**Estimated Time: 5-10 minutes from start to working bot! 🚀**
