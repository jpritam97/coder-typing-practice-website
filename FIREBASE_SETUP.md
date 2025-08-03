# Firebase Authentication Setup Guide

This guide will help you set up Firebase Authentication for the Typing Practice Application.

## Prerequisites

1. **Firebase Account**: Create a Firebase account at [https://firebase.google.com](https://firebase.google.com)
2. **Firebase Project**: Create a new Firebase project
3. **Python Environment**: Ensure you have Python 3.7+ installed

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter a project name (e.g., "typing-practice-app")
4. Choose whether to enable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Authentication

1. In your Firebase project console, go to "Authentication"
2. Click "Get started"
3. Go to the "Sign-in method" tab
4. Enable "Email/Password" authentication:
   - Click on "Email/Password"
   - Toggle "Enable"
   - Click "Save"

## Step 3: Get Firebase Configuration

### Web App Configuration

1. In Firebase Console, go to "Project settings" (gear icon)
2. Scroll down to "Your apps" section
3. Click the web icon (`</>`)
4. Register your app with a nickname (e.g., "typing-practice-web")
5. Copy the configuration object

### Service Account Configuration

1. In Firebase Console, go to "Project settings"
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file

## Step 4: Configure the Application

### Update Firebase Configuration

1. Open `firebase_config.py`
2. Replace the placeholder values with your actual Firebase configuration:

```python
# Firebase Admin SDK Configuration
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "your-actual-project-id",
    "private_key_id": "your-actual-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_ACTUAL_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com",
    "client_id": "your-actual-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project-id.iam.gserviceaccount.com"
}

# Firebase Web SDK Configuration
FIREBASE_WEB_CONFIG = {
    "apiKey": "your-actual-api-key",
    "authDomain": "your-project-id.firebaseapp.com",
    "projectId": "your-project-id",
    "storageBucket": "your-project-id.appspot.com",
    "messagingSenderId": "your-actual-sender-id",
    "appId": "your-actual-app-id"
}
```

### Alternative: Use Service Account File

Instead of hardcoding the service account details, you can:

1. Save the downloaded JSON file as `firebase-service-account.json` in your project root
2. Update `firebase_auth.py` to load from file:

```python
# In firebase_auth.py, replace the credentials initialization
cred = credentials.Certificate('firebase-service-account.json')
```

## Step 5: Install Dependencies

Make sure Firebase Admin SDK is installed:

```bash
pip install firebase-admin
```

## Step 6: Test the Setup

1. Start the server:
   ```bash
   python server.py
   ```

2. Open the application in your browser
3. Try to create a new account using the signup form
4. Check the server console for Firebase initialization messages

## Features

### Firebase Authentication Features

- **Email/Password Authentication**: Users can sign up and sign in with email and password
- **Email Verification**: Automatic email verification for new accounts
- **Secure Token Management**: Firebase handles secure token generation and validation
- **Real-time Auth State**: Automatic authentication state management
- **Fallback Support**: Falls back to traditional authentication if Firebase is not configured

### Security Benefits

- **Password Security**: Firebase handles password hashing and security
- **Token Management**: Secure JWT token generation and validation
- **Email Verification**: Built-in email verification system
- **Rate Limiting**: Firebase provides built-in rate limiting for authentication attempts

## Troubleshooting

### Common Issues

1. **Firebase not initialized**: Check that `firebase_config.py` has correct configuration
2. **Authentication errors**: Verify that Email/Password authentication is enabled in Firebase Console
3. **CORS errors**: Ensure your domain is added to authorized domains in Firebase Console
4. **Service account errors**: Verify the service account JSON file is correct and accessible

### Debug Mode

Enable debug logging by checking the browser console and server logs for:
- Firebase initialization status
- Authentication attempts
- Error messages

## Migration from Traditional Auth

The application supports both Firebase and traditional authentication:

1. **Firebase First**: The app tries Firebase authentication first
2. **Fallback**: If Firebase fails or is not configured, it falls back to traditional authentication
3. **Seamless Transition**: Users can use either method without issues

## Production Deployment

For production deployment:

1. **Environment Variables**: Store Firebase configuration in environment variables
2. **Domain Configuration**: Add your production domain to Firebase authorized domains
3. **Security Rules**: Configure Firebase Security Rules for your database
4. **HTTPS**: Ensure your application uses HTTPS in production

## Support

If you encounter issues:

1. Check the Firebase Console for authentication logs
2. Review server logs for error messages
3. Verify Firebase configuration is correct
4. Ensure all dependencies are installed

## Next Steps

After setting up Firebase Authentication, you can:

1. **Add Social Login**: Enable Google, Facebook, or other social login providers
2. **Password Reset**: Implement password reset functionality
3. **User Profiles**: Add user profile management features
4. **Admin Panel**: Create an admin panel for user management 