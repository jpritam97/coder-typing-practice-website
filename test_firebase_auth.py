#!/usr/bin/env python3
"""
Test Firebase Authentication
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from firebase_auth import initialize_firebase, create_user_with_email_password, sign_in_with_email_password, is_firebase_configured
    print("✅ Firebase auth module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Firebase auth module: {e}")
    sys.exit(1)

def test_firebase_config():
    """Test Firebase configuration"""
    print("\n🔧 Testing Firebase configuration...")
    
    if is_firebase_configured():
        print("✅ Firebase is properly configured")
        return True
    else:
        print("❌ Firebase is not properly configured")
        return False

def test_firebase_initialization():
    """Test Firebase initialization"""
    print("\n🔧 Testing Firebase initialization...")
    
    try:
        if initialize_firebase():
            print("✅ Firebase initialized successfully")
            return True
        else:
            print("❌ Firebase initialization failed")
            return False
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
        return False

def test_user_creation():
    """Test user creation"""
    print("\n🔧 Testing user creation...")
    
    test_email = "test@example.com"
    test_password = "TestPassword123"
    
    try:
        user, error = create_user_with_email_password(test_email, test_password, "TestUser")
        if user:
            print(f"✅ User created successfully: {user.uid}")
            return user.uid
        else:
            print(f"❌ User creation failed: {error}")
            return None
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return None

def test_user_signin(uid):
    """Test user sign in"""
    print("\n🔧 Testing user sign in...")
    
    test_email = "test@example.com"
    test_password = "TestPassword123"
    
    try:
        user, error = sign_in_with_email_password(test_email, test_password)
        if user:
            print(f"✅ User signed in successfully: {user.uid}")
            return True
        else:
            print(f"❌ User sign in failed: {error}")
            return False
    except Exception as e:
        print(f"❌ User sign in error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Firebase Authentication Tests")
    print("=" * 50)
    
    # Test 1: Configuration
    if not test_firebase_config():
        print("❌ Configuration test failed. Exiting.")
        return False
    
    # Test 2: Initialization
    if not test_firebase_initialization():
        print("❌ Initialization test failed. Exiting.")
        return False
    
    # Test 3: User Creation
    uid = test_user_creation()
    if not uid:
        print("❌ User creation test failed. Exiting.")
        return False
    
    # Test 4: User Sign In
    if not test_user_signin(uid):
        print("❌ User sign in test failed.")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All Firebase authentication tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 