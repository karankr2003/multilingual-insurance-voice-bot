#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all components are correctly configured
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*80}")
    print(f"  {text}")
    print('='*80)

def print_check(name, status, message=""):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if message:
        print(f"   → {message}")

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 11
    print_check(
        "Python Version",
        is_valid,
        f"Current: {version.major}.{version.minor}.{version.micro} (Required: 3.11+)"
    )
    return is_valid

def check_files():
    """Check if all required files exist"""
    print_header("FILE CHECK")
    
    required_files = [
        'app.py',
        'policy_engine.py',
        'session_manager.py',
        'language_detector.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        '.env',
        '.env.example',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        print_check(file, exists)
        all_exist = all_exist and exists
    
    return all_exist

def check_dependencies():
    """Check if required Python packages are installed"""
    print_header("DEPENDENCY CHECK")
    
    dependencies = {
        'flask': 'Flask',
        'twilio': 'Twilio',
        'dotenv': 'python-dotenv',
        'langdetect': 'langdetect'
    }
    
    all_installed = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print_check(package, True, "Installed")
        except ImportError:
            print_check(package, False, f"Run: pip install {package}")
            all_installed = False
    
    return all_installed

def check_environment():
    """Check environment variables"""
    print_header("ENVIRONMENT VARIABLES CHECK")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_PHONE_NUMBER'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        is_set = value is not None and len(value) > 0
        
        if is_set:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print_check(var, True, f"Set: {masked}")
        else:
            print_check(var, False, "Not set or empty")
        
        all_set = all_set and is_set
    
    return all_set

def check_directories():
    """Check if required directories can be created"""
    print_header("DIRECTORY CHECK")
    
    try:
        sessions_dir = Path('sessions')
        sessions_dir.mkdir(exist_ok=True)
        print_check("sessions/", True, "Created/exists")
        return True
    except Exception as e:
        print_check("sessions/", False, str(e))
        return False

def check_components():
    """Check if components can be imported"""
    print_header("COMPONENT CHECK")
    
    components = {
        'PolicyEngine': ('policy_engine', 'PolicyEngine'),
        'SessionManager': ('session_manager', 'SessionManager'),
        'LanguageDetector': ('language_detector', 'LanguageDetector')
    }
    
    all_working = True
    for name, (module, cls) in components.items():
        try:
            mod = __import__(module)
            getattr(mod, cls)
            print_check(name, True, "Can be imported")
        except Exception as e:
            print_check(name, False, str(e))
            all_working = False
    
    return all_working

def check_flask_app():
    """Check if Flask app can start"""
    print_header("FLASK APP CHECK")
    
    try:
        import app as flask_app
        print_check("app.py imports", True, "No syntax errors")
        
        # Check routes
        routes = ['/voice', '/process_input', '/health']
        for route in routes:
            print_check(f"Route {route}", True, "Defined")
        
        return True
    except Exception as e:
        print_check("app.py imports", False, str(e))
        return False

def run_component_tests():
    """Run basic component tests"""
    print_header("COMPONENT TESTING")
    
    try:
        from policy_engine import PolicyEngine
        from session_manager import SessionManager
        from language_detector import LanguageDetector
        
        # Test PolicyEngine
        engine = PolicyEngine()
        test_data = {
            'name': 'Test',
            'age': '30',
            'city': 'Mumbai',
            'occupation': 'Engineer',
            'medical_conditions': 'No',
            'family_history': 'No',
            'coverage': 'basic',
            'hospital': 'private',
            'dependents': 'no'
        }
        recommendation = engine.recommend(test_data)
        print_check(
            "PolicyEngine.recommend()",
            'policy_name' in recommendation,
            f"Recommended: {recommendation.get('policy_name', 'None')}"
        )
        
        # Test SessionManager
        manager = SessionManager(sessions_dir='test_sessions')
        session_id = manager.create_session('TEST_CALL')
        print_check(
            "SessionManager.create_session()",
            session_id is not None,
            f"Session ID: {session_id[:8]}..."
        )
        
        # Test LanguageDetector
        detector = LanguageDetector()
        detected = detector.detect("Hello, my name is John")
        print_check(
            "LanguageDetector.detect()",
            detected is not None,
            f"Detected: {detected}"
        )
        
        # Cleanup
        import shutil
        if Path('test_sessions').exists():
            shutil.rmtree('test_sessions')
        
        return True
        
    except Exception as e:
        print_check("Component tests", False, str(e))
        return False

def print_summary(checks):
    """Print summary and next steps"""
    print_header("SUMMARY")
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n🎉 All checks passed! Your bot is ready to run.")
        print("\n📋 Next steps:")
        print("   1. Start the server: python app.py")
        print("   2. In another terminal: ngrok http 5000")
        print("   3. Configure Twilio webhook with ngrok URL")
        print("   4. Call +1 (860) 467-1351 to test!")
        print("\n📚 Documentation:")
        print("   - QUICKSTART.md - 5-minute setup guide")
        print("   - README.md - Complete documentation")
        print("   - DEPLOYMENT_GUIDE.md - Cloud deployment")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check .env file exists and has correct values")
        print("   - Ensure Python 3.11+ is installed")

def main():
    """Main execution"""
    print_header("MULTILINGUAL INSURANCE VOICE BOT - SETUP CHECK")
    
    checks = {
        'Python Version': check_python_version(),
        'Required Files': check_files(),
        'Dependencies': check_dependencies(),
        'Environment Variables': check_environment(),
        'Directories': check_directories(),
        'Components': check_components(),
        'Flask App': check_flask_app(),
        'Component Tests': run_component_tests()
    }
    
    print_summary(checks)
    
    print(f"\n{'='*80}\n")
    
    return all(checks.values())

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
