from langdetect import detect, LangDetectException
import os

class LanguageDetector:
    """Detects language from text input using multiple strategies"""
    
    def __init__(self):
        self.language_map = {
            'en': 'en',
            'hi': 'hi',
            'mr': 'mr',
            'ta': 'ta',
            'kn': 'kn'
        }
        
        # Try to initialize Cohere for enhanced detection
        self.cohere_client = None
        self.cohere_model = "command-a-03-2025"
        try:
            cohere_key = os.getenv('COHERE_API_KEY')
            if cohere_key and cohere_key != 'your_cohere_api_key_here':
                import cohere
                self.cohere_client = cohere.Client(cohere_key)
                print(f"✅ Cohere-enhanced language detection enabled (model: {self.cohere_model})")
        except Exception as e:
            print(f"ℹ️  Using standard language detection (Cohere unavailable: {e})")
    
    def detect(self, text):
        """Detect language from text using multiple methods"""
        if not text or len(text.strip()) < 3:
            return None
        
        # Method 1: Try Cohere for better multilingual detection
        if self.cohere_client:
            cohere_result = self._detect_with_cohere(text)
            if cohere_result:
                return cohere_result
        
        # Method 2: Try langdetect library
        try:
            detected = detect(text)
            
            # Map detected language to supported languages
            if detected in self.language_map:
                return self.language_map[detected]
        except LangDetectException:
            pass
        
        # Method 3: Keyword-based detection for Indian languages
        keyword_result = self._detect_by_keywords(text)
        if keyword_result:
            return keyword_result
        
        # Method 4: Script-based detection (Unicode ranges)
        script_result = self._detect_by_script(text)
        if script_result:
            return script_result
        
        return None
    
    def _detect_with_cohere(self, text):
        """Use Cohere AI for language detection with command-a-03-2025 model"""
        try:
            response = self.cohere_client.chat(
                model=self.cohere_model,
                message=f"""Identify the language. Reply with ONLY one code: en, hi, mr, ta, or kn.

Text: "{text}"

Code:"""
            )
            
            detected = response.text.strip().lower()
            valid_languages = ['en', 'hi', 'mr', 'ta', 'kn']
            
            if detected in valid_languages:
                return detected
        except Exception:
            pass
        
        return None
    
    def _detect_by_keywords(self, text):
        """Detect language using common keywords"""
        text_lower = text.lower()
        
        # Hindi keywords (including romanized)
        hindi_keywords = ['hai', 'hain', 'kya', 'mera', 'aap', 'main', 'naam', 'saal', 'ka', 'ki', 
                         'mein', 'hun', 'hoon', 'toh', 'nahin', 'nahi', 'kuch', 'ek', 'rahata', 
                         'rahti', 'karata', 'karti', 'mere', 'meri']
        hindi_count = sum(1 for word in hindi_keywords if f' {word} ' in f' {text_lower} ' or text_lower.startswith(word) or text_lower.endswith(word))
        if hindi_count >= 2:
            return 'hi'
        
        # Marathi keywords
        marathi_keywords = ['ahe', 'aahe', 'kaay', 'maza', 'tumcha', 'maze', 'vay', 'naam', 
                           'mi', 'tu', 'aahe', 'nahi', 'nako']
        marathi_count = sum(1 for word in marathi_keywords if f' {word} ' in f' {text_lower} ' or text_lower.startswith(word) or text_lower.endswith(word))
        if marathi_count >= 2:
            return 'mr'
        
        # Tamil keywords
        tamil_keywords = ['naan', 'ungal', 'enna', 'irukku', 'peyar', 'vayathu', 'en', 'um']
        tamil_count = sum(1 for word in tamil_keywords if f' {word} ' in f' {text_lower} ' or text_lower.startswith(word) or text_lower.endswith(word))
        if tamil_count >= 2:
            return 'ta'
        
        # Kannada keywords
        kannada_keywords = ['naanu', 'nimma', 'yenu', 'ide', 'hesaru', 'vayasu', 'nanna', 'neenu']
        kannada_count = sum(1 for word in kannada_keywords if f' {word} ' in f' {text_lower} ' or text_lower.startswith(word) or text_lower.endswith(word))
        if kannada_count >= 2:
            return 'kn'
        
        return None
    
    def _detect_by_script(self, text):
        """Detect language based on Unicode script ranges"""
        # Count characters in each script
        devanagari = sum(1 for c in text if '\u0900' <= c <= '\u097F')  # Hindi/Marathi
        tamil = sum(1 for c in text if '\u0B80' <= c <= '\u0BFF')
        kannada = sum(1 for c in text if '\u0C80' <= c <= '\u0CFF')
        
        # If significant non-ASCII characters, determine script
        if devanagari > 5:
            # Distinguish Hindi vs Marathi by keywords
            text_lower = text.lower()
            if any(word in text_lower for word in ['ahe', 'aahe', 'maza', 'tumcha']):
                return 'mr'
            return 'hi'
        
        if tamil > 5:
            return 'ta'
        
        if kannada > 5:
            return 'kn'
        
        return None
