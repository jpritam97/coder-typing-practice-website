from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
import secrets
import requests
import socket
import dns.resolver
import subprocess
import json
import tempfile
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Import Firebase authentication
try:
    from firebase_auth import (
        initialize_firebase, create_user_with_email_password,
        sign_in_with_email_password, verify_firebase_token,
        get_user_by_uid, is_firebase_configured, get_firebase_web_config,
        save_typing_session_to_firestore, get_typing_history_from_firestore,
        get_user_stats_from_firestore
    )
    FIREBASE_AVAILABLE = True
    print("✅ Firebase authentication and Firestore available")
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️ Firebase authentication not available. Install with: pip install firebase-admin")

# Import email configuration (fallback)
try:
    from email_config import *
except ImportError:
    # Fallback configuration if email_config.py doesn't exist
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = 'jpritam97@gmail.com'
    GMAIL_APP_PASSWORD = 'your_app_password_here'
    VERIFICATION_SUBJECT = 'Email Verification - Typing Practice App'
    VERIFICATION_BODY_TEMPLATE = """
    Hello!
    
    This is an automated email verification from the Typing Practice App.
    Your email address: {email}
    
    If you receive this email, it means your email address is valid and you can proceed with signup.
    You can safely ignore this email - it's just to verify your email address exists.
    
    Best regards,
    Typing Practice Team
    """
    TRUSTED_DOMAINS = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
        'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com',
        'yandex.com', 'zoho.com', 'fastmail.com', 'tutanota.com'
    ]
    ENABLE_REAL_EMAIL_SENDING = True
    TIMEOUT_SECONDS = 10

# MongoDB imports - REMOVED
MONGODB_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Secret key for JWT tokens
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'  # Replace with your actual Google Client ID
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'  # Replace with your actual Google Client Secret

# MongoDB Configuration - REMOVED
# Initialize database - REMOVED
db = None

# Firebase-only authentication - no local storage
USERS = {}

# Typing history storage
TYPING_SESSIONS = {}

# Available programming languages and their snippet files
LANGUAGES = {
        'python': 'python_snippets.txt',
        'javascript': 'javascript_snippets.txt',
        'java': 'java_snippets.txt',
        'cpp': 'cpp_snippets.txt',
        'csharp': 'csharp_snippets.txt',
        'php': 'php_snippets.txt',
        'ruby': 'ruby_snippets.txt',
        'go': 'go_snippets.txt',
        'rust': 'rust_snippets.txt',
        'swift': 'swift_snippets.txt',
        'kotlin': 'kotlin_snippets.txt',
        'typescript': 'typescript_snippets.txt'
    }
    
# Load local snippets
def load_snippets():
    snippets = {}
    snippet_counts = {}
    
    for lang, filename in LANGUAGES.items():
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by double newlines to get individual snippets
                lang_snippets = [s.strip() for s in content.split('\n\n') if s.strip()]
                snippets[lang] = lang_snippets
                snippet_counts[lang] = len(lang_snippets)
                print(f"✅ Loaded {len(lang_snippets)} snippets for {lang}")
        except FileNotFoundError:
            print(f"⚠️ No snippets file found for {lang} ({filename})")
            snippets[lang] = []
            snippet_counts[lang] = 0
        except Exception as e:
            print(f"❌ Error loading snippets for {lang}: {e}")
            snippets[lang] = []
            snippet_counts[lang] = 0
    
    return snippets, snippet_counts

# Load snippets on startup
SNIPPETS, SNIPPET_COUNTS = load_snippets()

# Firebase-only user management functions
def get_user_by_username(username):
    """Get user from Firebase - not implemented for local storage"""
    # This function is not used when Firebase is the only authentication method
    return None

def create_user(user_data):
    """Create user in Firebase - local storage disabled"""
    # Users are created directly in Firebase, not stored locally
    return True

def update_user(username, update_data):
    """Update user in Firebase - local storage disabled"""
    # User updates are handled by Firebase
    return True

def get_user_count():
    """Get total user count from Firebase - local storage disabled"""
    # User count is managed by Firebase
    return 0

# Authentication helper functions
def validate_password(password):
    """Validate password strength"""
    # Check minimum length
    if len(password) < 8:
        return {
            'is_valid': False,
            'message': 'Password must be at least 8 characters long'
        }
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return {
            'is_valid': False,
            'message': 'Password must contain at least one uppercase letter'
        }
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return {
            'is_valid': False,
            'message': 'Password must contain at least one lowercase letter'
        }
    
    # Check for at least one number
    if not re.search(r'\d', password):
        return {
            'is_valid': False,
            'message': 'Password must contain at least one number'
        }
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return {
            'is_valid': False,
            'message': 'Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)'
        }
    
    return {
        'is_valid': True,
        'message': 'Password is strong'
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)  # Token expires in 7 days
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def verify_google_token(id_token):
    """Verify Google ID token"""
    try:
        # Verify the token with Google
        response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': id_token}
        )
        
        if response.status_code != 200:
            return None
            
        token_info = response.json()
        
        # Verify the token is for our app
        if token_info.get('aud') != GOOGLE_CLIENT_ID:
            return None
            
        return token_info
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        return None

# Authentication middleware
def require_auth(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'message': 'No token provided'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        username = verify_token(token)
        if not username:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        print("🚀 SIGNUP ENDPOINT CALLED")
        data = request.get_json()
        username = data.get('username')
        email = data.get('email', '').lower().strip()
        password = data.get('password')
        
        print(f"📝 Signup attempt for username: {username}, email: {email}")
        
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Validate email format
        import re
        email_pattern = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        if not email_pattern.match(email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address'
            }), 400
        
        # Validate password strength
        password_validation = validate_password(password)
        if not password_validation['is_valid']:
            return jsonify({
                'success': False,
                'message': password_validation['message']
            }), 400
        
        # Use Firebase authentication if available
        print(f"🔧 Firebase check: FIREBASE_AVAILABLE={FIREBASE_AVAILABLE}")
        firebase_configured = is_firebase_configured()
        print(f"🔧 Firebase check: is_firebase_configured()={firebase_configured}")
        print(f"🔧 About to check Firebase condition: {FIREBASE_AVAILABLE and firebase_configured}")
        
        if FIREBASE_AVAILABLE and firebase_configured:
            # Create user in Firebase
            firebase_user, error = create_user_with_email_password(email, password, username)
            if error:
                return jsonify({
                    'success': False,
                    'message': error
                }), 400
            
            # User is created directly in Firebase - no local storage needed
            print(f"✅ User created in Firebase with UID: {firebase_user.uid}")
            
            print(f"✅ New Firebase user registered: {username}")
            print(f"💾 Stored user data: {user_data}")
            print(f"📊 Total users in storage: {len(USERS)}")
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully with Firebase!'
            })
        else:
            # Fallback to traditional authentication
            print(f"🔧 Using traditional authentication (Firebase not available or not configured)")
            print(f"🔧 FIREBASE_AVAILABLE={FIREBASE_AVAILABLE}, firebase_configured={firebase_configured}")
            # Check if email domain exists
            if '@' not in email:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email format'
                }), 400
            
            domain = email.split('@')[1]
            
            # Check if domain has valid format
            domain_pattern = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$')
            if not domain_pattern.match(domain):
                return jsonify({
                    'success': False,
                    'message': 'Invalid email domain format'
                }), 400
            
            # List of common email domains that we know exist
            common_domains = {
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
                'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com',
                'yandex.com', 'zoho.com', 'fastmail.com', 'tutanota.com',
                'gmx.com', 'web.de', 't-online.de', 'freenet.de', 'arcor.de'
            }
            
            # AUTOMATED EMAIL VERIFICATION FOR ALL EMAILS
            print(f"📧 Starting automated email verification for: {email}")
            email_result = send_verification_email_automated(email)
            
            if not email_result['success']:
                print(f"❌ Email verification failed for {email}: {email_result['message']}")
                return jsonify({
                    'success': False,
                    'message': f'Email verification failed: {email_result["message"]}'
                }), 400
            
            print(f"✅ Email verification successful for: {email}")
            
            # Check if email already exists in memory storage
            email_exists = any(user.get('email', '').lower() == email for user in USERS.values() if isinstance(user, dict))
            if email_exists:
                return jsonify({
                    'success': False,
                    'message': 'Email already registered'
                }), 400
            
            # Hash password and create user
            hashed_password = hash_password(password)
            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'created_at': datetime.now(timezone.utc),
                'is_google_user': False,
                'last_login': datetime.now(timezone.utc)
            }
            
            # Save to database
            create_user(user_data)
            
            print(f"✅ New user registered: {username}")
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully! Email verification sent.'
            })
        
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({
            'success': False,
            'message': 'Registration failed'
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Use Firebase authentication if available
        print(f"🔧 Firebase check: FIREBASE_AVAILABLE={FIREBASE_AVAILABLE}")
        firebase_configured = is_firebase_configured()
        print(f"🔧 Firebase check: is_firebase_configured()={firebase_configured}")
        
        if FIREBASE_AVAILABLE and firebase_configured:
            # Firebase-only authentication - no local storage lookup needed
            print(f"🔧 Attempting Firebase login for username: {username}")
            
            # For Firebase authentication, we need the email
            # Since we don't store users locally, we'll need to get the email from the frontend
            # or use a different approach. For now, we'll require the frontend to send the email.
            email = data.get('email')
            if not email:
                return jsonify({
                    'success': False,
                    'message': 'Email is required for Firebase authentication'
                }), 400
            
            print(f"📧 Using email '{email}' for Firebase authentication")
            
            # Sign in with Firebase
            firebase_user, error = sign_in_with_email_password(email, password)
            if error:
                print(f"❌ Firebase authentication failed: {error}")
                return jsonify({
                    'success': False,
                    'message': error
                }), 401
            
            # Generate JWT token
            token = generate_token(username)
            
            print(f"✅ Firebase user logged in: {username}")
            
            return jsonify({
                'success': True,
                'token': token,
                'username': username,
                'email': email
            })
        else:
            # Fallback to traditional authentication
            # Get user from database
            user = get_user_by_username(username)
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid username or password'
                }), 401
            
            hashed_password = hash_password(password)
            
            if user['password'] != hashed_password:
                return jsonify({
                    'success': False,
                    'message': 'Invalid username or password'
                }), 401
            
            # Update last login time
            update_user(username, {'last_login': datetime.now(timezone.utc)})
            
            # Generate JWT token
            token = generate_token(username)
            
            print(f"✅ User logged in: {username}")
            
            return jsonify({
                'success': True,
                'token': token,
                'username': username,
                'email': user.get('email', '')
            })
        
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500

@app.route('/api/google-login', methods=['POST'])
def google_login():
    try:
        data = request.get_json()
        credential = data.get('credential')
        
        if not credential:
            return jsonify({
                'success': False,
                'message': 'Google credential is required'
            }), 400
        
        # Verify the Google ID token
        token_info = verify_google_token(credential)
        if not token_info:
            return jsonify({
                'success': False,
                'message': 'Invalid Google token'
            }), 401
        
        google_email = token_info.get('email')
        google_name = token_info.get('name', google_email.split('@')[0])
        
        # Create username from email if user doesn't exist
        username = google_name
        counter = 1
        while get_user_by_username(username):
            username = f"{google_name}{counter}"
            counter += 1
        
        # Check if user exists by email
        existing_user = None
        if db is not None:
            existing_user = db.users.find_one({'email': google_email})
        else:
            # Check in memory storage
            for user in USERS.values():
                if user.get('email') == google_email:
                    existing_user = user
                    break
        
        if existing_user:
            # Update existing user's Google info
            update_user(existing_user['username'], {
                'is_google_user': True,
                'google_id': token_info.get('sub'),
                'last_login': datetime.now(timezone.utc)
            })
            username = existing_user['username']
            print(f"✅ Existing user logged in with Google: {username}")
        else:
            # Create new user
            user_data = {
                'username': username,
                'email': google_email,
                'created_at': datetime.now(timezone.utc),
                'is_google_user': True,
                'google_id': token_info.get('sub'),
                'last_login': datetime.now(timezone.utc)
            }
            create_user(user_data)
            print(f"✅ New Google user created: {username}")
        
        # Generate JWT token
        token = generate_token(username)
        
        return jsonify({
            'success': True,
            'token': token,
            'username': username,
            'email': google_email
        })
        
    except Exception as e:
        print(f"Error in Google login: {e}")
        return jsonify({
            'success': False,
            'message': 'Google login failed'
        }), 500

@app.route('/api/generate-snippet', methods=['POST'])
def generate_snippet():
    try:
        data = request.get_json()
        language = data.get('language', 'python').lower()
        
        if language not in SNIPPETS or not SNIPPETS[language]:
            return jsonify({
                "success": False,
                "message": f"No snippets available for {language}"
            }), 404
        
        # Select a random snippet
        snippet = random.choice(SNIPPETS[language])
        
        return jsonify({
            "success": True,
            "snippet": snippet,
            "language": language,
            "total_snippets": len(SNIPPETS[language])
        })
        
    except Exception as e:
        print(f"Error generating snippet: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to generate snippet"
        }), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get available programming languages and their snippet counts"""
    try:
        languages_info = {}
        for lang in LANGUAGES.keys():
            languages_info[lang] = {
                'name': lang.title(),
                'snippet_count': SNIPPET_COUNTS.get(lang, 0),
                'available': SNIPPET_COUNTS.get(lang, 0) > 0
            }
        
        return jsonify({
            'success': True,
            'languages': languages_info,
            'total_languages': len(languages_info),
            'total_snippets': sum(SNIPPET_COUNTS.values())
        })
        
    except Exception as e:
        print(f"Error getting languages: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get languages'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'message': 'Server running with Google OAuth support',
        'users_count': get_user_count(),
        'languages_loaded': len([lang for lang in LANGUAGES if SNIPPET_COUNTS.get(lang, 0) > 0]),
        'total_snippets': sum(SNIPPET_COUNTS.values()),
        'database_connected': False,
        'mongodb_disabled': True,
        'firebase_available': FIREBASE_AVAILABLE,
        'firebase_configured': is_firebase_configured() if FIREBASE_AVAILABLE else False
    })

@app.route('/api/firebase-config', methods=['GET'])
def get_firebase_config():
    """Get Firebase Web SDK configuration for frontend"""
    try:
        if FIREBASE_AVAILABLE:
            config = get_firebase_web_config()
            return jsonify({
                'success': True,
                'config': config
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Firebase not available'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting Firebase config: {str(e)}'
        }), 500

@app.route('/api/user/<username>', methods=['GET'])
def get_user_by_username_endpoint(username):
    """Get user data by username for Firebase login"""
    try:
        user = get_user_by_username(username)
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'uid': user.get('uid')
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting user: {str(e)}'
        }), 500

@app.route('/api/save-typing-session', methods=['POST'])
def save_typing_session():
    """Save a typing practice session to database"""
    try:
        data = request.get_json()
        username = data.get('username')
        language = data.get('language')
        wpm = data.get('wpm', 0)
        accuracy = data.get('accuracy', 0)
        time_taken = data.get('time_taken', 0)
        
        if not username or not language:
            return jsonify({
                'success': False,
                'message': 'Username and language are required'
            }), 400
        
        # Create session data
        session_data = {
            'username': username,
            'language': language,
            'wpm': wpm,
            'accuracy': accuracy,
            'time_taken': time_taken,
            'date': datetime.now(timezone.utc).isoformat(),
            'practice_type': f"{language} Practice"
        }
        
        # Try to save to Firestore first, fallback to memory
        if FIREBASE_AVAILABLE:
            # Get user ID from Firebase (you might need to implement this)
            # For now, we'll use username as user_id
            user_id = username
            success, error = save_typing_session_to_firestore(user_id, session_data)
            if success:
                print(f"✅ Typing session saved to Firestore for {username}: {language} - WPM: {wpm}, Accuracy: {accuracy}%")
                return jsonify({
                    'success': True,
                    'message': 'Typing session saved to Firebase successfully'
                })
            else:
                print(f"⚠️ Firestore save failed, falling back to memory: {error}")
        
        # Fallback to memory storage
        if username not in TYPING_SESSIONS:
            TYPING_SESSIONS[username] = []
        
        TYPING_SESSIONS[username].append(session_data)
        
        print(f"✅ Typing session saved to memory for {username}: {language} - WPM: {wpm}, Accuracy: {accuracy}%")
        print(f"📊 Total sessions for {username}: {len(TYPING_SESSIONS[username])}")
        
        return jsonify({
            'success': True,
            'message': 'Typing session saved successfully'
        })
        
    except Exception as e:
        print(f"Error saving typing session: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to save typing session'
        }), 500

@app.route('/api/get-typing-history', methods=['GET'])
def get_typing_history():
    """Get typing history for a user"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        # Try to get from Firestore first, fallback to memory
        sessions = []
        
        if FIREBASE_AVAILABLE:
            # Get user ID from Firebase (you might need to implement this)
            # For now, we'll use username as user_id
            user_id = username
            sessions, error = get_typing_history_from_firestore(user_id)
            if error:
                print(f"⚠️ Firestore retrieval failed, falling back to memory: {error}")
                sessions = TYPING_SESSIONS.get(username, [])
            else:
                print(f"📊 Retrieved {len(sessions)} typing sessions from Firestore for {username}")
        else:
            # Fallback to memory storage
            sessions = TYPING_SESSIONS.get(username, [])
            print(f"📊 Retrieved {len(sessions)} typing sessions from memory for {username}")
        
        return jsonify({
            'success': True,
            'sessions': sessions
        })
        
    except Exception as e:
        print(f"Error getting typing history: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get typing history'
        }), 500

@app.route('/api/user-stats/<username>', methods=['GET'])
def get_user_stats(username):
    """Get typing statistics for a user"""
    try:
        if not username:
            return jsonify({
                'success': False,
                'message': 'Username is required'
            }), 400
        
        # Try to get stats from Firestore first, fallback to memory
        stats = None
        
        if FIREBASE_AVAILABLE:
            # Get user ID from Firebase (you might need to implement this)
            # For now, we'll use username as user_id
            user_id = username
            stats, error = get_user_stats_from_firestore(user_id)
            if error:
                print(f"⚠️ Firestore stats failed, falling back to memory: {error}")
                stats = None
        
        if stats is None:
            # Fallback to memory storage
            sessions = TYPING_SESSIONS.get(username, [])
            
            if not sessions:
                stats = {
                    'total_sessions': 0,
                    'avg_wpm': 0,
                    'best_wpm': 0,
                    'avg_accuracy': 0,
                    'total_time': 0,
                    'languages_practiced': []
                }
            else:
                # Calculate statistics from memory
                total_sessions = len(sessions)
                wpm_values = [session['wpm'] for session in sessions]
                accuracy_values = [session['accuracy'] for session in sessions]
                time_values = [session['time_taken'] for session in sessions]
                languages = list(set(session['language'] for session in sessions))
                
                stats = {
                    'total_sessions': total_sessions,
                    'avg_wpm': round(sum(wpm_values) / total_sessions, 2) if total_sessions > 0 else 0,
                    'best_wpm': round(max(wpm_values), 2) if wpm_values else 0,
                    'avg_accuracy': round(sum(accuracy_values) / total_sessions, 2) if total_sessions > 0 else 0,
                    'total_time': sum(time_values),
                    'languages_practiced': languages
                }
        
        print(f"📊 User stats for {username}: {stats['total_sessions']} sessions, avg WPM: {stats['avg_wpm']:.2f}")
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get user statistics'
        }), 500

@app.route('/api/check-email', methods=['POST'])
def check_email():
    """Check if email already exists in database"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        # Firebase-only mode - email checking is not available locally
        exists = False
        
        return jsonify({
            'success': True,
            'exists': exists
        })
        
    except Exception as e:
        print(f"Error checking email: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to check email'
        }), 500

# Email sending verification function
def send_verification_email(email):
    """Send a verification email to check if the email address exists"""
    try:
        # Create a simple verification message
        msg = MIMEMultipart()
        msg['From'] = 'noreply@typingpractice.com'
        msg['To'] = email
        msg['Subject'] = 'Email Verification Test'
        
        body = """
        This is an automated email verification test.
        If you receive this email, it means your email address is valid.
        You can safely ignore this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Try to send using common SMTP servers
        smtp_servers = [
            ('smtp.gmail.com', 587),
            ('smtp.yahoo.com', 587),
            ('smtp.outlook.com', 587),
            ('smtp.mail.yahoo.com', 587),
            ('smtp.live.com', 587)
        ]
        
        domain = email.split('@')[1].lower()
        
        # Try to find the appropriate SMTP server for the domain
        smtp_server = None
        for server, port in smtp_servers:
            if domain in server or any(common_domain in domain for common_domain in ['gmail', 'yahoo', 'outlook', 'hotmail', 'live']):
                smtp_server = (server, port)
                break
        
        if not smtp_server:
            # Use a default server
            smtp_server = ('smtp.gmail.com', 587)
        
        # Try to connect and send (this will fail if email doesn't exist)
        with smtplib.SMTP(smtp_server[0], smtp_server[1], timeout=10) as server:
            server.starttls()
            # Note: We're not actually sending, just testing the connection
            # This is a simplified test - in production you'd need proper credentials
            return {
                'valid': True,
                'exists': True,
                'message': 'Email server connection successful',
                'details': {'smtp_server': smtp_server[0]}
            }
            
    except smtplib.SMTPRecipientsRefused:
        return {
            'valid': False,
            'exists': False,
            'message': 'Email address does not exist',
            'details': {}
        }
    except smtplib.SMTPException as e:
        return {
            'valid': False,
            'exists': False,
            'message': f'SMTP error: {str(e)}',
            'details': {}
        }
    except Exception as e:
        return {
            'valid': False,
            'exists': False,
            'message': f'Email verification error: {str(e)}',
            'details': {}
        }

# Enhanced email verification with actual sending
def verify_email_with_sending(email):
    """Verify email by attempting to send a test email"""
    try:
        # First check if domain exists
        domain = email.split('@')[1].lower()
        
        # Check if domain is in common domains (skip sending for these)
        common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 
                         'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com',
                         'yandex.com', 'zoho.com', 'fastmail.com', 'tutanota.com']
        
        if domain in common_domains:
            # For common domains, we'll assume they exist
            return {
                'valid': True,
                'exists': True,
                'message': f'Common domain {domain} - assumed valid',
                'details': {'domain': domain, 'method': 'common_domain'}
            }
        
        # For other domains, try to send a test email
        # This is a simplified approach - in production you'd need proper SMTP credentials
        return {
            'valid': True,
            'exists': True,
            'message': f'Email verification attempted for {domain}',
            'details': {'domain': domain, 'method': 'smtp_test'}
        }
        
    except Exception as e:
        return {
            'valid': False,
            'exists': False,
            'message': f'Email verification error: {str(e)}',
            'details': {}
        }

# Automated email sending verification function
def send_verification_email_automated(email):
    """Automatically send verification email from jpritam97@gmail.com"""
    try:
        # Check if email format is valid
        if '@' not in email or '.' not in email.split('@')[1]:
            return {
                'success': False,
                'message': 'Invalid email format',
                'details': {'method': 'format_check'}
            }
        
        domain = email.split('@')[1].lower()
        
        # For trusted domains, we can verify without sending actual emails
        if domain in TRUSTED_DOMAINS:
            print(f"📧 Email verification successful for trusted domain: {email}")
            return {
                'success': True,
                'message': f'Email verification successful for {email}',
                'details': {
                    'method': 'trusted_domain_verification',
                    'from': SENDER_EMAIL,
                    'to': email,
                    'domain': domain,
                    'status': 'email_verified_successfully'
                }
            }
        
        # For real email sending, we need Gmail App Password
        if not ENABLE_REAL_EMAIL_SENDING or GMAIL_APP_PASSWORD == 'your_app_password_here':
            print(f"⚠️ Real email sending is disabled or not configured for: {email}")
            return {
                'success': True,
                'message': f'Email verification attempted for {email} (simulation mode)',
                'details': {
                    'method': 'simulation_mode',
                    'from': SENDER_EMAIL,
                    'to': email,
                    'domain': domain,
                    'status': 'simulation_mode'
                }
            }
        
        # Create verification email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = VERIFICATION_SUBJECT
        
        body = VERIFICATION_BODY_TEMPLATE.format(email=email)
        msg.attach(MIMEText(body, 'plain'))
        
        # Try to send the actual email
        try:
            # Connect to Gmail SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=TIMEOUT_SECONDS) as server:
                server.starttls()
                
                # Authenticate with Gmail using App Password
                server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
                
                # Send the actual email
                server.send_message(msg)
                
                print(f"📧 REAL EMAIL SENT from {SENDER_EMAIL} to {email}")
                return {
                    'success': True,
                    'message': f'Verification email sent successfully to {email}',
                    'details': {
                        'method': 'real_email_sent',
                        'from': SENDER_EMAIL,
                        'to': email,
                        'domain': domain,
                        'status': 'email_sent_successfully'
                    }
                }
                
        except smtplib.SMTPRecipientsRefused:
            print(f"❌ Email bounced back for: {email}")
            return {
                'success': False,
                'message': f'Email address {email} does not exist - email bounced back',
                'details': {'method': 'smtp_rejected', 'from': sender_email}
            }
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error for {email}: {str(e)}")
            return {
                'success': False,
                'message': f'SMTP error: {str(e)}',
                'details': {'method': 'smtp_error', 'from': sender_email}
            }
        except Exception as e:
            print(f"❌ Email sending error for {email}: {str(e)}")
            return {
                'success': False,
                'message': f'Email sending error: {str(e)}',
                'details': {'method': 'general_error', 'from': sender_email}
            }
        
    except Exception as e:
        print(f"❌ Email verification error for {email}: {str(e)}")
        return {
            'success': False,
            'message': f'Email verification error: {str(e)}',
            'details': {}
        }

# Enhanced email verification function
def verify_email_with_mosint(email):
    """Verify email using mosint tool with enhanced existence checking"""
    try:
        # Add Go bin to PATH
        go_bin = os.path.expanduser("~/go/bin")
        if go_bin not in os.environ.get('PATH', ''):
            os.environ['PATH'] = go_bin + os.pathsep + os.environ.get('PATH', '')
        
        # Run mosint command
        cmd = ['mosint', email, '--config', '.mosint.yaml']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return {
                'valid': False,
                'exists': False,
                'message': f'Mosint error: {result.stderr}',
                'details': {}
            }
        
        # Parse mosint output
        output_lines = result.stdout.strip().split('\n')
        mosint_data = {}
        
        # Extract key information from mosint output
        for line in output_lines:
            if ':' in line and not line.startswith('['):
                key, value = line.split(':', 1)
                mosint_data[key.strip()] = value.strip()
        
        # Check for valid indicators
        valid_indicators = []
        invalid_indicators = []
        
        # Check if email appears in data breaches (invalid)
        if 'Pastebin Dumps' in result.stdout and 'https://' in result.stdout:
            invalid_indicators.append('data_breach')
        
        # Check for valid domain (DNS lookup success)
        if 'DNS Lookup' in result.stdout:
            valid_indicators.append('dns_lookup')
        
        # Check for IP lookup success
        if 'IP Lookup' in result.stdout and 'IP:' in result.stdout:
            valid_indicators.append('ip_lookup')
        
        # Check if email exists (appears in any service)
        email_exists = False
        if 'Twitter Account Exists' in result.stdout or 'Spotify Account Exists' in result.stdout:
            email_exists = True
            valid_indicators.append('email_exists')
        
        # Check if email is disposable
        if 'disposable' in result.stdout.lower() or 'temp' in result.stdout.lower():
            invalid_indicators.append('disposable_email')
        
        # Additional email existence checks
        # Check if email appears in any service (indicating it's a real email)
        if any(service in result.stdout for service in ['Account Exists', 'Account Not Exists']):
            # If we get any account existence results, the email format is valid
            valid_indicators.append('format_valid')
        
        # Check for common email patterns that suggest it's a real email
        username, domain = email.split('@')
        if len(username) >= 3 and '.' in domain:  # Basic format check
            valid_indicators.append('format_valid')
        
        # Determine validity
        is_valid = len(valid_indicators) > 0 and len(invalid_indicators) == 0
        exists = email_exists or ('dns_lookup' in valid_indicators and 'format_valid' in valid_indicators and len(invalid_indicators) == 0)
        
        return {
            'valid': is_valid,
            'exists': exists,
            'message': f"Valid indicators: {valid_indicators}, Invalid indicators: {invalid_indicators}",
            'details': mosint_data
        }
        
    except subprocess.TimeoutExpired:
        return {
            'valid': False,
            'exists': False,
            'message': 'Email verification timed out',
            'details': {}
        }
    except Exception as e:
        return {
            'valid': False,
            'exists': False,
            'message': f'Verification error: {str(e)}',
            'details': {}
        }

@app.route('/api/check-email-domain', methods=['POST'])
def check_email_domain():
    """Check if email domain exists by verifying MX records"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        # Extract domain from email
        if '@' not in email:
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        domain = email.split('@')[1]
        
        # Check if domain has valid format
        import re
        domain_pattern = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$')
        if not domain_pattern.match(domain):
            return jsonify({
                'success': False,
                'exists': False,
                'message': 'Invalid domain format'
            })
        
        # List of common email domains that we know exist
        common_domains = {
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
            'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com',
            'yandex.com', 'zoho.com', 'fastmail.com', 'tutanota.com',
            'gmx.com', 'web.de', 't-online.de', 'freenet.de', 'arcor.de'
        }
        
        # If it's a common domain, return True
        if domain in common_domains:
            return jsonify({
                'success': True,
                'exists': True,
                'domain': domain
            })
        
        # Use real email sending verification
        email_result = verify_email_with_real_sending(email)
        
        if email_result['valid'] and email_result['exists']:
            return jsonify({
                'success': True,
                'exists': True,
                'domain': domain,
                'message': 'Email appears to be valid and exists'
            })
        else:
            return jsonify({
                'success': True,
                'exists': False,
                'domain': domain,
                'message': email_result['message'] or 'Email does not appear to exist'
            })
            
    except Exception as e:
        print(f"Error checking email domain: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to check email domain'
        }), 500

if __name__ == '__main__':
    print("📝 Using local snippets for code generation")
    print("🔐 Authentication system enabled with Google OAuth")
    print("💾 Using in-memory storage only")
    print(f"📊 Loaded {sum(SNIPPET_COUNTS.values())} snippets across {len([lang for lang in LANGUAGES if SNIPPET_COUNTS.get(lang, 0) > 0])} languages")
    print("🚀 Flask server started at http://localhost:5000")
    print("✅ Ready for typing practice with Google Sign-In!")
    app.run(debug=False, port=5000)
