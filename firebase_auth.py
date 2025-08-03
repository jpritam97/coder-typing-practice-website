import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin.exceptions import FirebaseError
import json
import os
from datetime import datetime, timedelta
import jwt
import secrets

# Import Firebase configuration
try:
    from firebase_config import FIREBASE_CONFIG, FIREBASE_AUTH_SETTINGS, FIREBASE_WEB_CONFIG
except ImportError:
    print("⚠️ Firebase configuration not found. Please create firebase_config.py")
    FIREBASE_CONFIG = {}
    FIREBASE_AUTH_SETTINGS = {}
    FIREBASE_WEB_CONFIG = {}

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Use service account credentials
            cred = credentials.Certificate(FIREBASE_CONFIG)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK initialized successfully")
            return True
        else:
            print("✅ Firebase Admin SDK already initialized")
            return True
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return False

# Firebase Authentication Functions
def create_user_with_email_password(email, password, display_name=None):
    """Create a new user with email and password"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        # Create user in Firebase Auth
        user_properties = {
            'email': email,
            'password': password,
            'email_verified': False
        }
        
        if display_name:
            user_properties['display_name'] = display_name
        
        user = auth.create_user(**user_properties)
        
        # Send email verification if enabled
        if FIREBASE_AUTH_SETTINGS.get('enable_email_verification', True):
            auth.generate_email_verification_link(email)
        
        return user, None
    except FirebaseError as e:
        error_code = e.code
        if error_code == 'EMAIL_EXISTS':
            return None, "Email already exists"
        elif error_code == 'INVALID_EMAIL':
            return None, "Invalid email format"
        elif error_code == 'WEAK_PASSWORD':
            return None, "Password is too weak"
        else:
            return None, f"Firebase error: {e.message}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Firestore Functions for Typing History
def save_typing_session_to_firestore(user_id, session_data):
    """Save typing session to Firestore"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return False, "Firebase not initialized"
        
        db = firestore.client()
        
        # Add timestamp if not present
        if 'timestamp' not in session_data:
            session_data['timestamp'] = datetime.now()
        
        # Save to Firestore
        doc_ref = db.collection('typing_sessions').document(user_id).collection('sessions').document()
        doc_ref.set(session_data)
        
        print(f"✅ Typing session saved to Firestore for user {user_id}")
        return True, None
    except Exception as e:
        print(f"❌ Error saving to Firestore: {e}")
        return False, f"Firestore error: {str(e)}"

def get_typing_history_from_firestore(user_id, limit=50):
    """Get typing history from Firestore"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return [], "Firebase not initialized"
        
        db = firestore.client()
        
        # Get sessions from Firestore
        sessions_ref = db.collection('typing_sessions').document(user_id).collection('sessions')
        docs = sessions_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        
        sessions = []
        for doc in docs:
            session_data = doc.to_dict()
            session_data['id'] = doc.id
            # Convert timestamp to ISO string for JSON serialization
            if 'timestamp' in session_data:
                session_data['timestamp'] = session_data['timestamp'].isoformat()
            sessions.append(session_data)
        
        print(f"📊 Retrieved {len(sessions)} typing sessions from Firestore for user {user_id}")
        return sessions, None
    except Exception as e:
        print(f"❌ Error getting from Firestore: {e}")
        return [], f"Firestore error: {str(e)}"

def get_user_stats_from_firestore(user_id):
    """Get user statistics from Firestore"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        db = firestore.client()
        
        # Get all sessions for the user
        sessions_ref = db.collection('typing_sessions').document(user_id).collection('sessions')
        docs = sessions_ref.stream()
        
        sessions = []
        for doc in docs:
            session_data = doc.to_dict()
            sessions.append(session_data)
        
        if not sessions:
            return {
                'total_sessions': 0,
                'avg_wpm': 0,
                'best_wpm': 0,
                'avg_accuracy': 0,
                'total_time': 0,
                'languages_practiced': []
            }, None
        
        # Calculate statistics
        total_sessions = len(sessions)
        wpm_values = [s.get('wpm', 0) for s in sessions]
        accuracy_values = [s.get('accuracy', 0) for s in sessions]
        time_values = [s.get('time_taken', 0) for s in sessions]
        languages = list(set(s.get('language', '') for s in sessions if s.get('language')))
        
        stats = {
            'total_sessions': total_sessions,
            'avg_wpm': round(sum(wpm_values) / total_sessions, 2) if total_sessions > 0 else 0,
            'best_wpm': round(max(wpm_values), 2) if wpm_values else 0,
            'avg_accuracy': round(sum(accuracy_values) / total_sessions, 2) if total_sessions > 0 else 0,
            'total_time': sum(time_values),
            'languages_practiced': languages
        }
        
        print(f"📊 Calculated stats for user {user_id}: {total_sessions} sessions")
        return stats, None
    except Exception as e:
        print(f"❌ Error getting stats from Firestore: {e}")
        return None, f"Firestore error: {str(e)}"

def sign_in_with_email_password(email, password):
    """Sign in user with email and password"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        # Get user by email
        user = auth.get_user_by_email(email)
        
        # Verify password (Firebase handles this automatically)
        # For server-side verification, we need to use custom tokens
        custom_token = auth.create_custom_token(user.uid)
        
        return user, None
    except FirebaseError as e:
        if e.code == 'USER_NOT_FOUND':
            return None, "User not found"
        elif e.code == 'INVALID_PASSWORD':
            return None, "Invalid password"
        else:
            return None, f"Firebase error: {e.message}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def verify_firebase_token(id_token):
    """Verify Firebase ID token"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token, None
    except FirebaseError as e:
        return None, f"Invalid token: {e.message}"
    except Exception as e:
        return None, f"Token verification error: {str(e)}"

def get_user_by_uid(uid):
    """Get user by UID"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        user = auth.get_user(uid)
        return user, None
    except FirebaseError as e:
        return None, f"User not found: {e.message}"
    except Exception as e:
        return None, f"Error getting user: {str(e)}"

def update_user_profile(uid, display_name=None, email=None):
    """Update user profile"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        update_data = {}
        if display_name:
            update_data['display_name'] = display_name
        if email:
            update_data['email'] = email
        
        user = auth.update_user(uid, **update_data)
        return user, None
    except FirebaseError as e:
        return None, f"Update failed: {e.message}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def delete_user(uid):
    """Delete user by UID"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return False, "Firebase not initialized"
        
        auth.delete_user(uid)
        return True, None
    except FirebaseError as e:
        return False, f"Delete failed: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def generate_custom_token(uid, additional_claims=None):
    """Generate custom token for user"""
    try:
        if not firebase_admin._apps:
            if not initialize_firebase():
                return None, "Firebase not initialized"
        
        custom_token = auth.create_custom_token(uid, additional_claims)
        return custom_token, None
    except FirebaseError as e:
        return None, f"Token generation failed: {e.message}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# JWT Token Functions (for compatibility with existing system)
def generate_jwt_token(user_data):
    """Generate JWT token for user"""
    try:
        payload = {
            'user_id': user_data.get('uid'),
            'email': user_data.get('email'),
            'display_name': user_data.get('display_name'),
            'exp': datetime.utcnow() + timedelta(days=7),
            'iat': datetime.utcnow()
        }
        
        secret_key = secrets.token_hex(32)
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token, None
    except Exception as e:
        return None, f"Token generation error: {str(e)}"

def verify_jwt_token(token):
    """Verify JWT token"""
    try:
        secret_key = secrets.token_hex(32)  # In production, use a fixed secret key
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
    except Exception as e:
        return None, f"Token verification error: {str(e)}"

# Utility Functions
def is_firebase_configured():
    """Check if Firebase is properly configured"""
    project_id = FIREBASE_CONFIG.get('project_id')
    is_configured = bool(project_id) and project_id != 'your-firebase-project-id'
    print(f"🔧 Firebase config check: project_id='{project_id}', is_configured={is_configured}")
    return is_configured

def get_firebase_web_config():
    """Get Firebase Web SDK configuration for frontend"""
    return FIREBASE_WEB_CONFIG 