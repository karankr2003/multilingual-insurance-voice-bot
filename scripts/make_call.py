from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Your ngrok URL (update this with your actual ngrok URL)
NGROK_URL = "https://amply-backrest-untaxed.ngrok-free.dev"

# Your phone number (the number you want to call)
YOUR_PHONE_NUMBER = input("Enter your phone number (with country code, e.g., +919876543210): ")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

print(f"\nMaking outbound call from {TWILIO_PHONE_NUMBER} to {YOUR_PHONE_NUMBER}...")
print(f"Using webhook: {NGROK_URL}/voice\n")

# Make the call
call = client.calls.create(
    to=YOUR_PHONE_NUMBER,
    from_=TWILIO_PHONE_NUMBER,
    url=f"{NGROK_URL}/voice",
    method='POST'
)

print(f"✅ Call initiated successfully!")
print(f"Call SID: {call.sid}")
print(f"Status: {call.status}")
print(f"\nYou should receive a call shortly from {TWILIO_PHONE_NUMBER}")
print("The bot will ask you questions about health insurance in multiple languages.")
