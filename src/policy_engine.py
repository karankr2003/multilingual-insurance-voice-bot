import os

class PolicyEngine:
    """Recommends health insurance policies based on user profile"""
    
    def __init__(self):
        self.policies = [
            {
                'name': 'HealthGuard Basic',
                'coverage': '₹3 Lakhs',
                'premium_base': 5000,
                'best_for': ['young', 'no_conditions', 'single']
            },
            {
                'name': 'HealthGuard Comprehensive',
                'coverage': '₹10 Lakhs',
                'premium_base': 12000,
                'best_for': ['middle_aged', 'family', 'comprehensive']
            },
            {
                'name': 'HealthGuard Premium Plus',
                'coverage': '₹25 Lakhs',
                'premium_base': 25000,
                'best_for': ['senior', 'conditions', 'premium', 'private']
            },
            {
                'name': 'HealthGuard Family Shield',
                'coverage': '₹15 Lakhs',
                'premium_base': 18000,
                'best_for': ['dependents', 'family']
            }
        ]
        
        # Try to initialize Cohere for enhanced recommendations
        self.cohere_client = None
        try:
            cohere_key = os.getenv('COHERE_API_KEY')
            if cohere_key and cohere_key != 'your_cohere_api_key_here':
                import cohere
                self.cohere_client = cohere.Client(cohere_key)
                print("✅ Cohere-enhanced policy recommendations enabled")
        except Exception as e:
            print(f"ℹ️  Using rule-based recommendations (Cohere unavailable: {e})")
    
    def recommend(self, session_data):
        """Generate policy recommendation based on caller profile"""
        scores = []
        
        for policy in self.policies:
            score = self._calculate_score(policy, session_data)
            scores.append((policy, score))
        
        # Get best policy
        best_policy, best_score = max(scores, key=lambda x: x[1])
        
        # Generate reasons
        reasons = self._generate_reasons(best_policy, session_data)
        
        # Calculate estimated premium
        premium = self._calculate_premium(best_policy, session_data)
        
        return {
            'policy_name': best_policy['name'],
            'coverage': best_policy['coverage'],
            'premium': premium,
            'reasons': reasons,
            'score': best_score
        }
    
    def _calculate_score(self, policy, data):
        """Calculate suitability score for a policy"""
        score = 0
        
        # Age scoring
        age_str = data.get('age', '').lower()
        try:
            age = int(''.join(filter(str.isdigit, age_str)))
        except:
            age = 30  # default
        
        if age < 30 and 'young' in policy['best_for']:
            score += 30
        elif 30 <= age < 50 and 'middle_aged' in policy['best_for']:
            score += 30
        elif age >= 50 and 'senior' in policy['best_for']:
            score += 30
        
        # Medical conditions scoring
        medical = data.get('medical_conditions', '').lower()
        if 'no' in medical or 'none' in medical:
            if 'no_conditions' in policy['best_for']:
                score += 25
        else:
            if 'conditions' in policy['best_for']:
                score += 25
        
        # Coverage preference scoring
        coverage = data.get('coverage', '').lower()
        if 'basic' in coverage and 'young' in policy['best_for']:
            score += 20
        elif 'comprehensive' in coverage and 'comprehensive' in policy['best_for']:
            score += 20
        elif 'premium' in coverage and 'premium' in policy['best_for']:
            score += 20
        
        # Hospital preference scoring
        hospital = data.get('hospital', '').lower()
        if 'private' in hospital and 'private' in policy['best_for']:
            score += 15
        
        # Dependents scoring
        dependents = data.get('dependents', '').lower()
        if 'yes' in dependents and 'dependents' in policy['best_for']:
            score += 30
        elif 'no' in dependents and 'single' in policy['best_for']:
            score += 10
        
        return score
    
    def _generate_reasons(self, policy, data):
        """Generate reasons why this policy is suitable"""
        
        # Try Cohere for personalized natural language reasons
        if self.cohere_client:
            cohere_reasons = self._generate_reasons_with_cohere(policy, data)
            if cohere_reasons:
                return cohere_reasons
        
        # Fallback to rule-based reasons
        reasons = []
        
        age_str = data.get('age', '').lower()
        try:
            age = int(''.join(filter(str.isdigit, age_str)))
        except:
            age = 30
        
        medical = data.get('medical_conditions', '').lower()
        coverage = data.get('coverage', '').lower()
        dependents = data.get('dependents', '').lower()
        occupation = data.get('occupation', '').lower()
        
        # Age-based reasons
        if age < 30:
            reasons.append("it offers affordable premiums for young individuals")
        elif age >= 50:
            reasons.append("it provides comprehensive coverage suitable for your age group")
        else:
            reasons.append("it balances coverage and affordability for your age bracket")
        
        # Medical conditions
        if 'no' in medical or 'none' in medical:
            reasons.append("you have no pre-existing conditions, qualifying you for better rates")
        else:
            reasons.append("it covers pre-existing medical conditions comprehensively")
        
        # Coverage preference
        if 'premium' in coverage or 'comprehensive' in coverage:
            reasons.append("it matches your preference for extensive coverage")
        
        # Dependents
        if 'yes' in dependents:
            reasons.append("it includes coverage for your family dependents")
        
        # Hospital preference
        hospital = data.get('hospital', '').lower()
        if 'private' in hospital:
            reasons.append("it provides access to premium private hospital networks")
        
        # Occupation-based
        if any(word in occupation for word in ['engineer', 'software', 'it', 'developer', 'professional']):
            reasons.append("it's popular among professionals in your field")
        
        return reasons[:2]  # Return top 2 reasons
    
    def _generate_reasons_with_cohere(self, policy, data):
        """Generate personalized reasons using Cohere AI"""
        try:
            response = self.cohere_client.chat(
                model='command-a-03-2025',
                message=f"""You are an insurance advisor. Generate exactly 2 brief, specific reasons (each 8-12 words) why this policy is recommended.

Caller: Age {data.get('age')}, {data.get('occupation')}, {data.get('city')}
Medical: {data.get('medical_conditions')}
Coverage wanted: {data.get('coverage')}
Dependents: {data.get('dependents')}

Policy: {policy['name']} - {policy['coverage']} coverage

Generate 2 reasons (one per line, no numbering):"""
            )
            
            text = response.text.strip()
            reasons = [r.strip() for r in text.split('\n') if r.strip()]
            
            if len(reasons) >= 2:
                return reasons[:2]
        except Exception as e:
            print(f"Cohere reason generation failed: {e}")
        
        return None
    
    def _calculate_premium(self, policy, data):
        """Calculate estimated premium"""
        premium = policy['premium_base']
        
        # Age adjustment
        age_str = data.get('age', '').lower()
        try:
            age = int(''.join(filter(str.isdigit, age_str)))
        except:
            age = 30
        
        if age >= 50:
            premium *= 1.5
        elif age >= 40:
            premium *= 1.3
        elif age >= 30:
            premium *= 1.1
        
        # Medical conditions adjustment
        medical = data.get('medical_conditions', '').lower()
        if 'yes' in medical or ('no' not in medical and 'none' not in medical and len(medical) > 5):
            premium *= 1.2
        
        # Dependents adjustment
        dependents = data.get('dependents', '').lower()
        if 'yes' in dependents:
            premium *= 1.4
        
        return int(premium)
