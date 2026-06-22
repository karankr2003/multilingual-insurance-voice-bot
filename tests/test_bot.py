import unittest
from session_manager import SessionManager
from policy_engine import PolicyEngine
from language_detector import LanguageDetector

class TestVoiceBot(unittest.TestCase):
    """Test suite for voice bot components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.session_manager = SessionManager(sessions_dir='test_sessions')
        self.policy_engine = PolicyEngine()
        self.language_detector = LanguageDetector()
    
    def test_session_creation(self):
        """Test session creation"""
        call_sid = "TEST_CALL_SID_001"
        session_id = self.session_manager.create_session(call_sid)
        
        self.assertIsNotNone(session_id)
        self.assertIn(call_sid, self.session_manager.sessions)
    
    def test_session_retrieval(self):
        """Test session data retrieval"""
        call_sid = "TEST_CALL_SID_002"
        self.session_manager.create_session(call_sid)
        
        session = self.session_manager.get_session(call_sid)
        self.assertIsNotNone(session)
        self.assertIsInstance(session, dict)
    
    def test_language_detection_english(self):
        """Test English language detection"""
        text = "Hello, my name is John"
        detected = self.language_detector.detect(text)
        self.assertEqual(detected, 'en')
    
    def test_language_detection_hindi(self):
        """Test Hindi language detection"""
        text = "Mera naam Karan hai"
        detected = self.language_detector.detect(text)
        self.assertEqual(detected, 'hi')
    
    def test_policy_recommendation(self):
        """Test policy recommendation generation"""
        session_data = {
            'name': 'Test User',
            'age': '25',
            'city': 'Bangalore',
            'occupation': 'Software Engineer',
            'medical_conditions': 'No',
            'family_history': 'No',
            'coverage': 'Basic',
            'hospital': 'Both',
            'dependents': 'No'
        }
        
        recommendation = self.policy_engine.recommend(session_data)
        
        self.assertIn('policy_name', recommendation)
        self.assertIn('coverage', recommendation)
        self.assertIn('premium', recommendation)
        self.assertIn('reasons', recommendation)
        self.assertEqual(len(recommendation['reasons']), 2)
    
    def test_premium_calculation_young(self):
        """Test premium calculation for young user"""
        session_data = {
            'age': '25',
            'medical_conditions': 'No',
            'dependents': 'No'
        }
        
        recommendation = self.policy_engine.recommend(session_data)
        premium = recommendation['premium']
        
        self.assertIsInstance(premium, int)
        self.assertGreater(premium, 0)
    
    def test_premium_calculation_senior(self):
        """Test premium calculation for senior user"""
        session_data = {
            'age': '55',
            'medical_conditions': 'Yes, diabetes',
            'dependents': 'Yes'
        }
        
        recommendation = self.policy_engine.recommend(session_data)
        premium = recommendation['premium']
        
        self.assertIsInstance(premium, int)
        self.assertGreater(premium, 0)

if __name__ == '__main__':
    unittest.main()
