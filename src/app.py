from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from session_manager import SessionManager
from policy_engine import PolicyEngine
from language_detector import LanguageDetector

load_dotenv()

app = Flask(__name__)

# Initialize components
session_manager = SessionManager()
policy_engine = PolicyEngine()
language_detector = LanguageDetector()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Multilingual prompts
@app.route('/', methods=['GET'])
def home():
    """Homepage with bot information"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multilingual Insurance Voice Bot</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2c3e50; }
            .info { background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #3498db; color: white; padding: 10px; border-radius: 3px; margin: 5px 0; }
            .status { color: #27ae60; font-weight: bold; }
            ul { line-height: 1.8; }
        </style>
    </head>
    <body>
        <h1>🤖 Multilingual Insurance Voice Bot</h1>
        <p class="status">✅ Server is running!</p>
        
        <div class="info">
            <h2>📞 How to Test</h2>
            <p>Call this number to interact with the bot:</p>
            <h3>+1 (860) 467-1351</h3>
        </div>
        
        <div class="info">
            <h2>🌍 Supported Languages</h2>
            <ul>
                <li>🇬🇧 English</li>
                <li>🇮🇳 Hindi (हिंदी)</li>
                <li>🇮🇳 Marathi (मराठी)</li>
                <li>🇮🇳 Tamil (தமிழ்)</li>
                <li>🇮🇳 Kannada (ಕನ್ನಡ)</li>
            </ul>
        </div>
        
        <div class="info">
            <h2>🏥 Insurance Type</h2>
            <p><strong>Health Insurance</strong> - Complete conversation flow with policy recommendations</p>
        </div>
        
        <div class="info">
            <h2>🔧 API Endpoints</h2>
            <div class="endpoint">GET / - This homepage</div>
            <div class="endpoint">GET /health - Health check endpoint</div>
            <div class="endpoint">POST /voice - Twilio voice webhook (entry point)</div>
            <div class="endpoint">POST /process_input - Conversation processing</div>
        </div>
        
        <div class="info">
            <h2>📋 Setup Instructions</h2>
            <ol>
                <li>Expose this server using ngrok: <code>ngrok http 5000</code></li>
                <li>Copy your ngrok HTTPS URL</li>
                <li>Go to <a href="https://console.twilio.com" target="_blank">Twilio Console</a></li>
                <li>Configure webhook: <code>https://your-ngrok-url.ngrok.io/voice</code></li>
                <li>Call +1 (860) 467-1351 to test!</li>
            </ol>
        </div>
        
        <div class="info">
            <h2>📊 Features</h2>
            <ul>
                <li>✅ Automatic language detection</li>
                <li>✅ Dynamic language switching</li>
                <li>✅ AI-powered policy recommendations</li>
                <li>✅ Session transcripts with timestamps</li>
                <li>✅ Cohere AI integration (optional)</li>
            </ul>
        </div>
        
        <p style="text-align: center; color: #7f8c8d; margin-top: 40px;">
            Built with Flask + Twilio + Cohere AI
        </p>
    </body>
    </html>
    """

PROMPTS = {
    'en': {
        'greeting': 'Hello! Welcome to our health insurance service. What is your name?',
        'ask_age': 'Thank you {name}. How old are you?',
        'ask_city': 'Got it. Which city do you live in?',
        'ask_occupation': 'Thank you. What is your occupation?',
        'ask_medical_conditions': 'Do you have any pre-existing medical conditions?',
        'ask_family_history': 'Does your family have any history of chronic diseases?',
        'ask_coverage': 'What coverage amount are you looking for? Basic, comprehensive, or premium?',
        'ask_hospital': 'Do you prefer government hospitals, private hospitals, or both?',
        'ask_dependents': 'Do you want to include dependents in your coverage?',
        'recommendation': 'Based on your profile, I recommend {policy}. This policy offers {coverage} coverage with an estimated premium of {premium} rupees per year. This suits you because {reason1} and {reason2}.',
        'closing': 'Thank you for using our service. You will receive detailed information via email. Goodbye!'
    },
    'hi': {
        'greeting': 'नमस्ते! हमारी स्वास्थ्य बीमा सेवा में आपका स्वागत है। आपका नाम क्या है?',
        'ask_age': 'धन्यवाद {name}। आपकी उम्र क्या है?',
        'ask_city': 'समझ गया। आप किस शहर में रहते हैं?',
        'ask_occupation': 'धन्यवाद। आपका पेशा क्या है?',
        'ask_medical_conditions': 'क्या आपको कोई पुरानी बीमारी है?',
        'ask_family_history': 'क्या आपके परिवार में कोई पुरानी बीमारी का इतिहास है?',
        'ask_coverage': 'आप कितनी कवरेज चाहते हैं? बेसिक, व्यापक, या प्रीमियम?',
        'ask_hospital': 'आप सरकारी अस्पताल, निजी अस्पताल, या दोनों पसंद करते हैं?',
        'ask_dependents': 'क्या आप अपने कवरेज में आश्रितों को शामिल करना चाहते हैं?',
        'recommendation': 'आपकी प्रोफाइल के आधार पर, मैं {policy} की सिफारिश करता हूं। यह पॉलिसी {coverage} कवरेज प्रदान करती है और अनुमानित प्रीमियम {premium} रुपये प्रति वर्ष है। यह आपके लिए उपयुक्त है क्योंकि {reason1} और {reason2}।',
        'closing': 'हमारी सेवा का उपयोग करने के लिए धन्यवाद। आपको ईमेल के माध्यम से विस्तृत जानकारी प्राप्त होगी। अलविदा!'
    },
    'mr': {
        'greeting': 'नमस्कार! आमच्या आरोग्य विमा सेवेत आपले स्वागत आहे। तुमचे नाव काय आहे?',
        'ask_age': 'धन्यवाद {name}। तुमचे वय किती आहे?',
        'ask_city': 'समजले। तुम्ही कोणत्या शहरात राहता?',
        'ask_occupation': 'धन्यवाद। तुमचा व्यवसाय काय आहे?',
        'ask_medical_conditions': 'तुम्हाला कोणत्याही जुन्या आजारांचा त्रास आहे का?',
        'ask_family_history': 'तुमच्या कुटुंबात कोणत्याही जुन्या आजारांचा इतिहास आहे का?',
        'ask_coverage': 'तुम्हाला किती कव्हरेज हवे आहे? बेसिक, सर्वसमावेशक किंवा प्रीमियम?',
        'ask_hospital': 'तुम्ही सरकारी रुग्णालय, खाजगी रुग्णालय किंवा दोन्ही पसंत करता?',
        'ask_dependents': 'तुम्ही तुमच्या कव्हरेजमध्ये आश्रितांना समाविष्ट करू इच्छिता?',
        'recommendation': 'तुमच्या प्रोफाइलच्या आधारे, मी {policy} ची शिफारस करतो। ही पॉलिसी {coverage} कव्हरेज देते आणि अंदाजे प्रीमियम {premium} रुपये प्रति वर्ष आहे। हे तुमच्यासाठी योग्य आहे कारण {reason1} आणि {reason2}।',
        'closing': 'आमची सेवा वापरल्याबद्दल धन्यवाद। तुम्हाला ईमेलद्वारे तपशीलवार माहिती मिळेल। निरोप!'
    },
    'ta': {
        'greeting': 'வணக்கம்! எங்கள் சுகாதார காப்பீட்டு சேவைக்கு உங்களை வரவேற்கிறோம். உங்கள் பெயர் என்ன?',
        'ask_age': 'நன்றி {name}। உங்கள் வயது என்ன?',
        'ask_city': 'புரிந்தது। நீங்கள் எந்த நகரத்தில் வசிக்கிறீர்கள்?',
        'ask_occupation': 'நன்றி। உங்கள் தொழில் என்ன?',
        'ask_medical_conditions': 'உங்களுக்கு ஏதேனும் முந்தைய மருத்துவ நிலைமைகள் உள்ளதா?',
        'ask_family_history': 'உங்கள் குடும்பத்தில் நாட்பட்ட நோய்களின் வரலாறு உள்ளதா?',
        'ask_coverage': 'நீங்கள் எந்த அளவு காப்பீடு தேடுகிறீர்கள்? அடிப்படை, விரிவான, அல்லது பிரீமியம்?',
        'ask_hospital': 'நீங்கள் அரசு மருத்துவமனைகள், தனியார் மருத்துவமனைகள், அல்லது இரண்டையும் விரும்புகிறீர்களா?',
        'ask_dependents': 'உங்கள் காப்பீட்டில் சார்ந்திருப்பவர்களை சேர்க்க விரும்புகிறீர்களா?',
        'recommendation': 'உங்கள் சுயவிவரத்தின் அடிப்படையில், நான் {policy} பரிந்துரைக்கிறேன். இந்த பாலிசி {coverage} காப்பீட்டை வழங்குகிறது மற்றும் மதிப்பிடப்பட்ட பிரீமியம் வருடத்திற்கு {premium} ரூபாய். இது உங்களுக்கு ஏற்றது ஏனெனில் {reason1} மற்றும் {reason2}.',
        'closing': 'எங்கள் சேவையைப் பயன்படுத்தியதற்கு நன்றி। விரிவான தகவல் மின்னஞ்சல் மூலம் வரும். பிரியாவிடை!'
    },
    'kn': {
        'greeting': 'ನಮಸ್ಕಾರ! ನಮ್ಮ ಆರೋಗ್ಯ ವಿಮಾ ಸೇವೆಗೆ ನಿಮ್ಮನ್ನು ಸ್ವಾಗತಿಸುತ್ತೇವೆ. ನಿಮ್ಮ ಹೆಸರೇನು?',
        'ask_age': 'ಧನ್ಯವಾದಗಳು {name}. ನಿಮ್ಮ ವಯಸ್ಸು ಎಷ್ಟು?',
        'ask_city': 'ಅರ್ಥವಾಯಿತು. ನೀವು ಯಾವ ನಗರದಲ್ಲಿ ವಾಸಿಸುತ್ತೀರಿ?',
        'ask_occupation': 'ಧನ್ಯವಾದಗಳು. ನಿಮ್ಮ ಉದ್ಯೋಗವೇನು?',
        'ask_medical_conditions': 'ನಿಮಗೆ ಯಾವುದೇ ಹಿಂದಿನ ವೈದ್ಯಕೀಯ ಸ್ಥಿತಿಗಳಿವೆಯೇ?',
        'ask_family_history': 'ನಿಮ್ಮ ಕುಟುಂಬದಲ್ಲಿ ದೀರ್ಘಕಾಲದ ರೋಗಗಳ ಇತಿಹಾಸವಿದೆಯೇ?',
        'ask_coverage': 'ನೀವು ಯಾವ ಕವರೇಜ್ ಮೊತ್ತವನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಿ? ಮೂಲ, ಸಮಗ್ರ, ಅಥವಾ ಪ್ರೀಮಿಯಂ?',
        'ask_hospital': 'ನೀವು ಸರ್ಕಾರಿ ಆಸ್ಪತ್ರೆಗಳು, ಖಾಸಗಿ ಆಸ್ಪತ್ರೆಗಳು, ಅಥವಾ ಎರಡನ್ನೂ ಆದ್ಯತೆ ನೀಡುತ್ತೀರಾ?',
        'ask_dependents': 'ನಿಮ್ಮ ಕವರೇಜ್‌ನಲ್ಲಿ ಅವಲಂಬಿತರನ್ನು ಸೇರಿಸಲು ಬಯಸುವಿರಾ?',
        'recommendation': 'ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಆಧಾರದ ಮೇಲೆ, ನಾನು {policy} ಶಿಫಾರಸು ಮಾಡುತ್ತೇನೆ. ಈ ಪಾಲಿಸಿ {coverage} ಕವರೇಜ್ ನೀಡುತ್ತದೆ ಮತ್ತು ಅಂದಾಜು ಪ್ರೀಮಿಯಂ ವರ್ಷಕ್ಕೆ {premium} ರೂಪಾಯಿಗಳು. ಇದು ನಿಮಗೆ ಸೂಕ್ತವಾಗಿದೆ ಏಕೆಂದರೆ {reason1} ಮತ್ತು {reason2}.',
        'closing': 'ನಮ್ಮ ಸೇವೆಯನ್ನು ಬಳಸಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ನಿಮಗೆ ಇಮೇಲ್ ಮೂಲಕ ವಿವರವಾದ ಮಾಹಿತಿ ಬರುತ್ತದೆ. ವಿದಾಯ!'
    }
}

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    """Handle incoming calls"""
    response = VoiceResponse()
    
    # Get CallSid from either GET params or POST form
    call_sid = request.values.get('CallSid')
    
    # Create new session if we have a CallSid
    if call_sid:
        session_manager.create_session(call_sid)
    
    # Default language is English
    gather = Gather(
        input='speech',
        action='/process_input?step=name&lang=en',
        language='en-US',
        speech_timeout='auto',
        timeout=10
    )
    gather.say(PROMPTS['en']['greeting'])
    response.append(gather)
    
    # Add fallback if no input received
    response.say("I didn't hear your response. Let me ask again.")
    response.redirect('/voice')
    
    return Response(str(response), mimetype='text/xml')

@app.route('/process_input', methods=['GET', 'POST'])
def process_input():
    """Process user input and continue conversation"""
    response = VoiceResponse()
    
    # Get parameters
    step = request.args.get('step')
    current_lang = request.args.get('lang', 'en')
    call_sid = request.values.get('CallSid')
    speech_result = request.values.get('SpeechResult', '')
    
    # Debug logging
    print(f"\n[DEBUG] /process_input called")
    print(f"  Step: {step}")
    print(f"  CallSid: {call_sid}")
    print(f"  Speech: {speech_result}")
    print(f"  Current Lang from URL: {current_lang}")
    print(f"  Available sessions: {list(session_manager.sessions.keys())}")
    
    # Get session
    session = session_manager.get_session(call_sid)
    if session is None:
        print(f"[ERROR] Session not found for CallSid: {call_sid}")
        response.say("Session error. Please call again.")
        response.hangup()
        return Response(str(response), mimetype='text/xml')
    
    # Get session info to check stored language
    session_info = session_manager.sessions.get(call_sid, {})
    stored_lang = session_info.get('language', 'en')
    
    # Use stored language from session if available (overrides URL param)
    if stored_lang != 'en' and stored_lang != current_lang:
        current_lang = stored_lang
        print(f"[LANGUAGE] Using stored session language: {stored_lang}")
    
    # Detect language from speech - but only on early questions
    # Once language is set, stick with it unless user explicitly switches
    session_info = session_manager.sessions.get(call_sid, {})
    stored_lang = session_info.get('language', 'en')
    
    # Only detect language on first 2 questions (name, age)
    # After that, use the stored session language
    if step in ['name', 'age']:
        detected_lang = language_detector.detect(speech_result)
        print(f"[LANGUAGE DETECTION] Input: '{speech_result}' -> Detected: {detected_lang}")
        if detected_lang and detected_lang != current_lang and len(speech_result.strip()) > 3:
            current_lang = detected_lang
            session_manager.update_language(call_sid, current_lang)
            print(f"[LANGUAGE SWITCH] Detected {detected_lang} in: {speech_result}")
        else:
            print(f"[LANGUAGE] Keeping {current_lang} (detected: {detected_lang}, length: {len(speech_result.strip())})")
    else:
        # Use stored session language for all subsequent questions
        if stored_lang != current_lang:
            current_lang = stored_lang
            print(f"[LANGUAGE LOCKED] Using session language: {stored_lang}")
    
    # Log the interaction
    session_manager.add_interaction(call_sid, step, speech_result, current_lang)
    
    # Process based on step
    if step == 'name':
        # Extract just the name from responses like "My name is Karan"
        name = speech_result
        if 'name is' in speech_result.lower():
            name = speech_result.lower().split('name is')[-1].strip()
        elif 'i am' in speech_result.lower():
            name = speech_result.lower().split('i am')[-1].strip()
        # Capitalize first letter
        name = name.capitalize()
        
        session['name'] = name
        next_prompt = PROMPTS[current_lang]['ask_age'].format(name=name)
        next_step = 'age'
    
    elif step == 'age':
        # Extract age number from responses like "I am 25 years old"
        age = speech_result
        import re
        age_match = re.search(r'\d+', speech_result)
        if age_match:
            age = age_match.group()
        
        session['age'] = age
        next_prompt = PROMPTS[current_lang]['ask_city']
        next_step = 'city'
    
    elif step == 'city':
        # Extract city name from responses like "I live in Bangalore"
        city = speech_result
        if 'live in' in speech_result.lower():
            city = speech_result.lower().split('live in')[-1].strip()
        elif 'from' in speech_result.lower():
            city = speech_result.lower().split('from')[-1].strip()
        # Capitalize
        city = city.title()
        
        session['city'] = city
        next_prompt = PROMPTS[current_lang]['ask_occupation']
        next_step = 'occupation'
    
    elif step == 'occupation':
        # Extract occupation from responses like "I am a software engineer"
        occupation = speech_result
        if 'i am' in speech_result.lower():
            occupation = speech_result.lower().split('i am')[-1].strip()
            # Remove article "a" or "an"
            occupation = occupation.replace('a ', '').replace('an ', '')
        
        session['occupation'] = occupation
        next_prompt = PROMPTS[current_lang]['ask_medical_conditions']
        next_step = 'medical_conditions'
    
    elif step == 'medical_conditions':
        session['medical_conditions'] = speech_result
        next_prompt = PROMPTS[current_lang]['ask_family_history']
        next_step = 'family_history'
    
    elif step == 'family_history':
        session['family_history'] = speech_result
        next_prompt = PROMPTS[current_lang]['ask_coverage']
        next_step = 'coverage'
    
    elif step == 'coverage':
        session['coverage'] = speech_result
        next_prompt = PROMPTS[current_lang]['ask_hospital']
        next_step = 'hospital'
    
    elif step == 'hospital':
        session['hospital'] = speech_result
        next_prompt = PROMPTS[current_lang]['ask_dependents']
        next_step = 'dependents'
    
    elif step == 'dependents':
        session['dependents'] = speech_result
        
        # Get full session for policy recommendation
        full_session = session_manager.sessions.get(call_sid, {})
        full_session['data'] = session
        
        # Generate recommendation
        recommendation = policy_engine.recommend(session)
        
        # Translate reasons to current language if not English
        if current_lang != 'en':
            try:
                import cohere
                cohere_key = os.getenv('COHERE_API_KEY')
                if cohere_key and cohere_key != 'your_cohere_api_key_here':
                    co = cohere.Client(cohere_key)
                    lang_names = {'hi': 'Hindi', 'mr': 'Marathi', 'ta': 'Tamil', 'kn': 'Kannada'}
                    target_lang = lang_names.get(current_lang, 'Hindi')
                    
                    response_trans = co.chat(
                        model='command-a-03-2025',
                        message=f"""Translate these 2 reasons to {target_lang}. Keep them brief (8-12 words each). Return only the translations, one per line:

1. {recommendation['reasons'][0]}
2. {recommendation['reasons'][1]}"""
                    )
                    
                    translated = [r.strip() for r in response_trans.text.strip().split('\n') if r.strip() and not r.strip()[0].isdigit()]
                    if len(translated) >= 2:
                        recommendation['reasons'] = translated[:2]
                        print(f"[TRANSLATION] Translated reasons to {target_lang}")
            except Exception as e:
                print(f"[TRANSLATION ERROR] {e}")
        
        # Save recommendation
        session_manager.save_recommendation(call_sid, recommendation)
        
        # Prepare recommendation message
        rec_message = PROMPTS[current_lang]['recommendation'].format(
            policy=recommendation['policy_name'],
            coverage=recommendation['coverage'],
            premium=recommendation['premium'],
            reason1=recommendation['reasons'][0],
            reason2=recommendation['reasons'][1]
        )
        
        response.say(rec_message, language=get_tts_language(current_lang))
        response.pause(length=1)
        response.say(PROMPTS[current_lang]['closing'], language=get_tts_language(current_lang))
        
        # Save transcript
        session_manager.save_transcript(call_sid)
        
        response.hangup()
        return Response(str(response), mimetype='text/xml')
    
    else:
        response.say("Error in conversation flow.")
        response.hangup()
        return Response(str(response), mimetype='text/xml')
    
    # Continue conversation
    gather = Gather(
        input='speech',
        action=f'/process_input?step={next_step}&lang={current_lang}',
        language=get_speech_language(current_lang),
        speech_timeout='auto',
        timeout=10
    )
    gather.say(next_prompt, language=get_tts_language(current_lang))
    response.append(gather)
    
    # Add fallback if no input received
    response.say("I didn't hear your response. Let me ask again.", language=get_tts_language(current_lang))
    response.redirect(f'/process_input?step={next_step}&lang={current_lang}')
    
    return Response(str(response), mimetype='text/xml')

def get_speech_language(lang_code):
    """Get speech recognition language code"""
    lang_map = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'mr': 'mr-IN',
        'ta': 'ta-IN',
        'kn': 'kn-IN'
    }
    return lang_map.get(lang_code, 'en-IN')

def get_tts_language(lang_code):
    """Get text-to-speech language code"""
    lang_map = {
        'en': 'en-IN',
        'hi': 'hi-IN',
        'mr': 'mr-IN',
        'ta': 'ta-IN',
        'kn': 'kn-IN'
    }
    return lang_map.get(lang_code, 'en-IN')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'multilingual-insurance-voicebot'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    # Validate environment variables
    required_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)
    
    print(f"Starting voice bot on {host}:{port}")
    print(f"Twilio phone number: {TWILIO_PHONE_NUMBER}")
    
    app.run(host=host, port=port, debug=True)
