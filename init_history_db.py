#!/usr/bin/env python3
"""
Initialize Typing History Database
Creates the typing_sessions collection and adds sample data
"""

import os
from datetime import datetime, timezone
from pymongo import MongoClient

def init_history_database():
    """Initialize the typing history database"""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_ATLAS_URI', 'mongodb://localhost:27017/')
    DB_NAME = 'typing_practice'
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB")
        
        # Create typing_sessions collection if it doesn't exist
        if 'typing_sessions' not in db.list_collection_names():
            db.create_collection('typing_sessions')
            print("✅ Created typing_sessions collection")
        else:
            print("✅ typing_sessions collection already exists")
        
        # Add sample typing sessions
        sample_sessions = [
            {
                'username': 'jpritam97',
                'language': 'cpp',
                'wpm': 17,
                'accuracy': 98.8,
                'time_taken': 45,
                'date': datetime.now(timezone.utc),
                'practice_type': 'cpp Practice'
            },
            {
                'username': 'jpritam97',
                'language': 'cpp',
                'wpm': 17,
                'accuracy': 100.0,
                'time_taken': 42,
                'date': datetime.now(timezone.utc),
                'practice_type': 'cpp Practice'
            },
            {
                'username': 'jyotipritam_',
                'language': 'python',
                'wpm': 25,
                'accuracy': 95.5,
                'time_taken': 38,
                'date': datetime.now(timezone.utc),
                'practice_type': 'python Practice'
            },
            {
                'username': 'jyotipritam_',
                'language': 'javascript',
                'wpm': 22,
                'accuracy': 97.2,
                'time_taken': 41,
                'date': datetime.now(timezone.utc),
                'practice_type': 'javascript Practice'
            }
        ]
        
        # Insert sample sessions
        result = db.typing_sessions.insert_many(sample_sessions)
        print(f"✅ Added {len(result.inserted_ids)} sample typing sessions")
        
        # Display current sessions
        all_sessions = list(db.typing_sessions.find({}, {'_id': 0}))
        print(f"\n📊 Current typing sessions in database:")
        for session in all_sessions:
            print(f"  - {session['username']}: {session['practice_type']} - WPM: {session['wpm']}, Accuracy: {session['accuracy']}%")
        
        print(f"\n🎯 Database structure:")
        print(f"  Database: {DB_NAME}")
        print(f"  Collections: {db.list_collection_names()}")
        print(f"  Users: {db.users.count_documents({})}")
        print(f"  Typing Sessions: {db.typing_sessions.count_documents({})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing history database: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ Initializing Typing History Database")
    print("=" * 50)
    
    success = init_history_database()
    
    if success:
        print("\n✅ History database initialized successfully!")
        print("You can now test the typing history feature.")
    else:
        print("\n❌ Failed to initialize history database.") 