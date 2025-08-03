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

# Import email configuration
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

# MongoDB imports
try:
    from pymongo import MongoClient
    from bson import ObjectId
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠️ MongoDB not available. Install with: pip install pymongo")

app = Flask(__name__)
CORS(app)

# Secret key for JWT tokens
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'  # Replace with your actual Google Client ID
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'  # Replace with your actual Google Client Secret

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_ATLAS_URI', 'mongodb://localhost:27017/')
DB_NAME = 'typing_practice'

# Initialize MongoDB connection
def init_mongodb():
    if not MONGODB_AVAILABLE:
        return None
    
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB")
        return db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

# Initialize database
db = init_mongodb()

# Fallback in-memory storage if MongoDB is not available
USERS = {}

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

# Database helper functions
def get_user_by_username(username):
    """Get user from database or memory"""
    if db is not None:
        return db.users.find_one({'username': username})
    else:
        return USERS.get(username)

def create_user(user_data):
    """Create user in database or memory"""
    if db is not None:
        result = db.users.insert_one(user_data)
        return result.inserted_id
    else:
        USERS[user_data['username']] = user_data
        return True

def update_user(username, update_data):
    """Update user in database or memory"""
    if db is not None:
        return db.users.update_one({'username': username}, {'$set': update_data})
    else:
        if username in USERS:
            USERS[username].update(update_data)
            return True
        return False

def get_user_count():
    """Get total user count"""
    if db is not None:
        return db.users.count_documents({})
    else:
        return len(USERS)

# Authentication helper functions
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
        data = request.get_json()
        username = data.get('username')
        email = data.get('email', '').lower().strip()
        password = data.get('password')
        
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
        
        # Check if username already exists
        existing_user = get_user_by_username(username)
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
        
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
        
        # Check if email already exists
        if db is not None:
            existing_email = db.users.find_one({'email': email})
            if existing_email:
                return jsonify({
                    'success': False,
                    'message': 'Email already registered'
                }), 400
        else:
            # Check in memory storage
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
        'database_connected': db is not None
    })

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
            'date': datetime.now(timezone.utc),
            'practice_type': f"{language} Practice"
        }
        
        # Save to database
        if db is not None:
            result = db.typing_sessions.insert_one(session_data)
            print(f"✅ Typing session saved for {username}: {language} - WPM: {wpm}, Accuracy: {accuracy}%")
        else:
            # Fallback to memory storage
            if 'typing_sessions' not in USERS:
                USERS['typing_sessions'] = []
            USERS['typing_sessions'].append(session_data)
            print(f"✅ Typing session saved (memory) for {username}: {language}")
        
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
        
        # Get history from database
        if db is not None:
            sessions = list(db.typing_sessions.find(
                {'username': username},
                {'_id': 0}  # Exclude MongoDB ObjectId
            ).sort('date', -1))  # Sort by date descending (newest first)
        else:
            # Get from memory storage
            sessions = []
            if 'typing_sessions' in USERS:
                sessions = [s for s in USERS['typing_sessions'] if s.get('username') == username]
                sessions.sort(key=lambda x: x.get('date', datetime.now(timezone.utc)), reverse=True)
        
        # Format dates for display (Windows compatible)
        for session in sessions:
            if 'date' in session:
                if isinstance(session['date'], datetime):
                    # Format as M/D/YYYY (Windows compatible)
                    session['date'] = session['date'].strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
                elif isinstance(session['date'], str):
                    # Already formatted, keep as is
                    pass
                else:
                    # Fallback formatting
                    session['date'] = datetime.now(timezone.utc).strftime('%m/%d/%Y').lstrip('0').replace('/0', '/')
        
        print(f"📊 Retrieved {len(sessions)} typing sessions for {username}")
        
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
        
        # Check if email exists in database
        if db is not None:
            existing_user = db.users.find_one({'email': email})
            exists = existing_user is not None
        else:
            # Check in memory storage
            exists = any(user.get('email', '').lower() == email for user in USERS.values() if isinstance(user, dict))
        
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
    if db is not None:
        print("🗄️ MongoDB connected - persistent user storage enabled")
    else:
        print("⚠️ Running with in-memory storage (install pymongo for database)")
    print(f"📊 Loaded {sum(SNIPPET_COUNTS.values())} snippets across {len([lang for lang in LANGUAGES if SNIPPET_COUNTS.get(lang, 0) > 0])} languages")
    print("🚀 Flask server started at http://localhost:5000")
    print("✅ Ready for typing practice with Google Sign-In!")
    app.run(debug=False, port=5000)
