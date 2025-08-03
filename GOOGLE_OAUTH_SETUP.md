# Google OAuth Setup Guide

This guide will help you set up Google OAuth for the typing practice application.

## Step 1: Create Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" and then "New Project"
3. Enter a project name (e.g., "Typing Practice App")
4. Click "Create"

## Step 2: Enable Google+ API

1. In your Google Cloud project, go to "APIs & Services" > "Library"
2. Search for "Google+ API" and click on it
3. Click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Typing Practice App"
   - User support email: Your email
   - Developer contact information: Your email
   - Save and continue through the steps

4. Create OAuth 2.0 Client ID:
   - Application type: Web application
   - Name: "Typing Practice Web Client"
   - Authorized JavaScript origins: `http://localhost:5000`
   - Authorized redirect URIs: `http://localhost:5000`
   - Click "Create"

5. Copy the Client ID and Client Secret

## Step 4: Update Configuration Files

### Update server.py
Replace the placeholder values in `server.py`:

```python
# Google OAuth Configuration
GOOGLE_CLIENT_ID = 'your-actual-client-id-here'
GOOGLE_CLIENT_SECRET = 'your-actual-client-secret-here'
```

### Update js/main.js
Replace the placeholder value in `js/main.js`:

```javascript
const GOOGLE_CLIENT_ID = 'your-actual-client-id-here';
```

## Step 5: Install Dependencies

Run the installation script:
```bash
install_auth.bat
```

Or manually install:
```bash
pip install -r requirements.txt
```

## Step 6: Start the Application

1. Start the server:
```bash
python server.py
```

2. Open `index.html` in your browser

## Step 7: Test Google Sign-In

1. Click "Sign Up" or "Login"
2. Click the "Sign in with Google" button
3. Complete the Google OAuth flow
4. You should be logged in successfully

## Troubleshooting

### Common Issues:

1. **"Invalid client" error**: Make sure your Client ID is correct in both `server.py` and `js/main.js`

2. **"Redirect URI mismatch"**: Ensure your authorized redirect URIs in Google Cloud Console match your application URL

3. **"Google API not enabled"**: Make sure you've enabled the Google+ API in your Google Cloud project

4. **CORS errors**: The server includes CORS headers, but if you're still getting errors, check that your domain is properly configured

### Security Notes:

- Never commit your actual Client Secret to version control
- Use environment variables for production deployments
- The Client Secret is only needed on the server side
- The Client ID is safe to include in client-side code

## Production Deployment

For production deployment:

1. Update authorized origins in Google Cloud Console to include your production domain
2. Use environment variables for sensitive configuration
3. Consider using a proper database instead of in-memory storage
4. Implement proper session management and token refresh

## File Structure After Setup

```
├── index.html              # Updated with Google Sign-In buttons
├── js/main.js             # Updated with Google OAuth logic
├── server.py              # Updated with Google login endpoint
├── requirements.txt       # Updated with requests library
├── GOOGLE_OAUTH_SETUP.md # This setup guide
└── install_auth.bat      # Installation script
```

## Next Steps

After setting up Google OAuth:

1. Test the authentication flow
2. Consider adding user profile management
3. Implement user progress tracking
4. Add social features like leaderboards
5. Consider adding other OAuth providers (GitHub, Facebook, etc.) 