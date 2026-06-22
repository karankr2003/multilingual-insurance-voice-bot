import json
import os
from datetime import datetime
import uuid

class SessionManager:
    """Manages conversation sessions, transcripts, and recommendations"""
    
    def __init__(self, sessions_dir='sessions'):
        self.sessions = {}
        self.sessions_dir = sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
    
    def create_session(self, call_sid):
        """Create a new session"""
        session_id = str(uuid.uuid4())
        self.sessions[call_sid] = {
            'session_id': session_id,
            'call_sid': call_sid,
            'start_time': datetime.now().isoformat(),
            'language': 'en',
            'interactions': [],
            'data': {}
        }
        return session_id
    
    def get_session(self, call_sid):
        """Get session data"""
        if call_sid in self.sessions:
            return self.sessions[call_sid]['data']
        return None
    
    def update_language(self, call_sid, language):
        """Update session language"""
        if call_sid in self.sessions:
            self.sessions[call_sid]['language'] = language
            self.sessions[call_sid]['interactions'].append({
                'timestamp': datetime.now().isoformat(),
                'event': 'language_change',
                'language': language
            })
    
    def add_interaction(self, call_sid, step, user_input, language):
        """Add an interaction to the session"""
        if call_sid in self.sessions:
            self.sessions[call_sid]['interactions'].append({
                'timestamp': datetime.now().isoformat(),
                'step': step,
                'user_input': user_input,
                'language': language
            })
    
    def save_recommendation(self, call_sid, recommendation):
        """Save recommendation to session"""
        if call_sid in self.sessions:
            self.sessions[call_sid]['recommendation'] = recommendation
    
    def save_transcript(self, call_sid):
        """Save complete transcript and recommendation"""
        if call_sid not in self.sessions:
            return
        
        session = self.sessions[call_sid]
        session['end_time'] = datetime.now().isoformat()
        
        # Create transcript
        transcript = {
            'session_id': session['session_id'],
            'call_sid': call_sid,
            'start_time': session['start_time'],
            'end_time': session['end_time'],
            'languages_used': list(set([i.get('language', 'en') for i in session['interactions'] if 'language' in i])),
            'caller_data': session['data'],
            'conversation': session['interactions'],
            'recommendation': session.get('recommendation', {})
        }
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_{timestamp}_{session['session_id'][:8]}.json"
        filepath = os.path.join(self.sessions_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"SESSION COMPLETE: {session['session_id']}")
        print(f"{'='*80}")
        print(f"Caller: {session['data'].get('name', 'Unknown')}")
        print(f"Age: {session['data'].get('age', 'Unknown')}")
        print(f"City: {session['data'].get('city', 'Unknown')}")
        print(f"Occupation: {session['data'].get('occupation', 'Unknown')}")
        print(f"\nRecommendation:")
        if 'recommendation' in session:
            rec = session['recommendation']
            print(f"  Policy: {rec.get('policy_name', 'N/A')}")
            print(f"  Coverage: {rec.get('coverage', 'N/A')}")
            print(f"  Premium: ₹{rec.get('premium', 'N/A')}/year")
            print(f"  Reasons: {', '.join(rec.get('reasons', []))}")
        print(f"\nTranscript saved to: {filepath}")
        print(f"{'='*80}\n")
        
        return filepath
