"""
Cohere AI Integration for Enhanced Conversation and Language Understanding
Uses chat API with command-a-03-2025 model
"""

import os
from typing import Dict, Optional
import cohere

class CohereAssistant:
    """Cohere AI assistant for natural language understanding and generation"""
    
    def __init__(self):
        api_key = os.getenv('COHERE_API_KEY')
        self.client = None
        self.enabled = False
        self.model = "command-a-03-2025"
        
        if api_key and api_key != 'your_cohere_api_key_here':
            try:
                self.client = cohere.Client(api_key)
                self.enabled = True
                print(f"✅ Cohere AI enabled (model: {self.model})")
            except Exception as e:
                print(f"⚠️  Cohere initialization failed: {e}")
                self.enabled = False
        else:
            print("ℹ️  Cohere API key not configured - using rule-based approach")
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language using Cohere's multilingual understanding
        Returns language code or None
        """
        if not self.enabled or not text:
            return None
        
        try:
            response = self.client.chat(
                model=self.model,
                message=f"""Identify the language of this text. Reply with ONLY one of these codes: en, hi, mr, ta, or kn

Text: "{text}"

Reply with only the code:"""
            )
            
            detected = response.text.strip().lower()
            
            # Validate response
            valid_languages = ['en', 'hi', 'mr', 'ta', 'kn']
            if detected in valid_languages:
                return detected
            
        except Exception as e:
            print(f"Cohere language detection error: {e}")
        
        return None
    
    def enhance_policy_recommendation(self, caller_data: Dict, policy: Dict) -> str:
        """
        Generate a natural, personalized explanation using Cohere
        """
        if not self.enabled:
            return None
        
        try:
            response = self.client.chat(
                model=self.model,
                message=f"""You are an insurance advisor. Generate a brief, friendly explanation for why this health insurance policy is recommended.

Caller Profile:
- Name: {caller_data.get('name')}
- Age: {caller_data.get('age')}
- Occupation: {caller_data.get('occupation')}
- Medical Conditions: {caller_data.get('medical_conditions')}
- Coverage Preference: {caller_data.get('coverage')}
- Dependents: {caller_data.get('dependents')}

Recommended Policy:
- Name: {policy.get('policy_name')}
- Coverage: {policy.get('coverage')}
- Premium: ₹{policy.get('premium')}/year

Generate 2-3 sentences explaining why this policy suits them. Be conversational and specific."""
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Cohere recommendation enhancement error: {e}")
            return None
    
    def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """
        Translate text to target language using Cohere
        """
        if not self.enabled:
            return None
        
        language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'mr': 'Marathi',
            'ta': 'Tamil',
            'kn': 'Kannada'
        }
        
        target_lang_name = language_names.get(target_language, 'English')
        
        try:
            response = self.client.chat(
                model=self.model,
                message=f"""Translate this text to {target_lang_name}. Provide only the translation, no explanations.

Text: "{text}"

Translation:"""
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Cohere translation error: {e}")
            return None
    
    def extract_user_intent(self, text: str) -> Dict:
        """
        Extract structured information from user's free-form response
        """
        if not self.enabled:
            return {}
        
        try:
            response = self.client.chat(
                model=self.model,
                message=f"""Extract key information from this text. Return a JSON object.

Text: "{text}"

Extract if present:
- age (number)
- city (string)
- has_medical_conditions (yes/no)
- coverage_preference (basic/comprehensive/premium)

JSON:"""
            )
            
            # Parse the response
            import json
            result = json.loads(response.text.strip())
            return result
            
        except Exception as e:
            print(f"Cohere intent extraction error: {e}")
            return {}
    
    def generate_follow_up_question(self, context: Dict, current_step: str) -> Optional[str]:
        """
        Generate a contextual follow-up question
        """
        if not self.enabled:
            return None
        
        try:
            response = self.client.chat(
                model=self.model,
                message=f"""You are a friendly insurance bot. Based on the conversation so far, ask the next question naturally.

Context: {context}
Current step: {current_step}

Generate a brief, friendly question in the same language style:"""
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Cohere follow-up generation error: {e}")
            return None
