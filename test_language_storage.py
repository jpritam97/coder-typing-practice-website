#!/usr/bin/env python3
"""
Test script to verify language storage in typing sessions
"""

import requests
import json
import time

def test_language_storage():
    """Test that language is properly stored in typing sessions"""
    
    base_url = "http://localhost:5000"
    
    # Test data for different languages
    test_sessions = [
        {
            "username": "testuser",
            "language": "python",
            "wpm": 45.5,
            "accuracy": 92,
            "time_taken": 120
        },
        {
            "username": "testuser", 
            "language": "javascript",
            "wpm": 38.2,
            "accuracy": 88,
            "time_taken": 95
        },
        {
            "username": "testuser",
            "language": "cpp", 
            "wpm": 42.1,
            "accuracy": 85,
            "time_taken": 110
        }
    ]
    
    print("🧪 Testing Language Storage in Typing Sessions")
    print("=" * 50)
    
    # Test 1: Save sessions with different languages
    print("\n📝 Saving test sessions...")
    for i, session in enumerate(test_sessions, 1):
        try:
            response = requests.post(f"{base_url}/api/save-typing-session", json=session)
            data = response.json()
            
            if data['success']:
                print(f"✅ Session {i} saved successfully: {session['language']} - WPM: {session['wpm']}")
            else:
                print(f"❌ Session {i} failed: {data.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Error saving session {i}: {e}")
    
    # Test 2: Retrieve typing history
    print("\n📊 Retrieving typing history...")
    try:
        response = requests.get(f"{base_url}/api/get-typing-history?username=testuser")
        data = response.json()
        
        if data['success']:
            sessions = data['sessions']
            print(f"📈 Found {len(sessions)} sessions in history")
            
            for i, session in enumerate(sessions, 1):
                language = session.get('language', 'unknown')
                wpm = session.get('wpm', 0)
                accuracy = session.get('accuracy', 0)
                print(f"  Session {i}: {language} - WPM: {wpm}, Accuracy: {accuracy}%")
                
                # Check if language is properly stored
                if language != 'unknown':
                    print(f"    ✅ Language '{language}' stored correctly")
                else:
                    print(f"    ❌ Language not stored properly")
        else:
            print(f"❌ Failed to retrieve history: {data.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error retrieving history: {e}")
    
    # Test 3: Get user statistics
    print("\n📊 Retrieving user statistics...")
    try:
        response = requests.get(f"{base_url}/api/user-stats/testuser")
        data = response.json()
        
        if data['success']:
            stats = data['stats']
            languages = stats.get('languages_practiced', [])
            print(f"📈 User statistics:")
            print(f"  Total sessions: {stats.get('total_sessions', 0)}")
            print(f"  Average WPM: {stats.get('avg_wpm', 0)}")
            print(f"  Best WPM: {stats.get('best_wpm', 0)}")
            print(f"  Languages practiced: {languages}")
            
            if languages:
                print("    ✅ Languages properly tracked in statistics")
            else:
                print("    ❌ No languages found in statistics")
        else:
            print(f"❌ Failed to get statistics: {data.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
    
    print("\n🎯 Language Storage Test Complete!")

if __name__ == "__main__":
    try:
        test_language_storage()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running. Please start the server first:")
        print("   python server.py")
    except Exception as e:
        print(f"❌ Error: {e}") 