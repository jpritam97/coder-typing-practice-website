# Typing Practice Website for Coders

A modern web-based typing practice application with Firebase authentication, multiple programming languages, and performance tracking using Firestore.

## 🚀 Features

### ✨ Core Features
- **Multi-language Typing Practice**: Support for 12 programming languages
  - Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, TypeScript
- **Real-time Performance Metrics**: WPM (Words Per Minute), Accuracy, and Time tracking
- **Firebase Authentication**: Secure login/signup with email/password and Google OAuth
- **Firestore Database**: Cloud-based typing history storage
- **Responsive Design**: Modern UI with Tailwind CSS

### 🔐 Authentication
- **Firebase Authentication**: Email/password authentication
- **Google Sign-In**: OAuth 2.0 integration with Firebase
- **Email Validation**: Domain verification and format checking
- **Session Management**: JWT-based authentication with 7-day expiration

### 📊 Performance Tracking
- **Real-time Metrics**: Live WPM, accuracy, and timer display
- **Session History**: View all completed typing sessions stored in Firestore
- **Progress Tracking**: Monitor improvement over time
- **Language-specific Stats**: Separate tracking for each programming language

### 🎯 User Experience
- **Clean Interface**: Modern, responsive design
- **Snippet Cycling**: Sequential snippet selection for each language
- **Active State Tracking**: Visual feedback for selected languages
- **Smart Field Clearing**: Intelligent form and typing field management

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Tailwind CSS for styling
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Firebase SDK**: Client-side authentication and database integration

### Backend
- **Python**: Flask web framework
- **Firebase Admin SDK**: Server-side Firebase integration
- **Firestore**: NoSQL cloud database for user and session storage
- **JWT**: JSON Web Tokens for session management
- **SHA-256**: Password hashing

### Development Tools
- **Git**: Version control
- **Python 3.13**: Latest Python version
- **Flask-CORS**: Cross-origin resource sharing

## 📁 Project Structure

```
cpp_typing_practice_separated/
├── index.html                 # Main application interface
├── server.py                  # Flask backend server
├── requirements.txt           # Python dependencies
├── firebase_config.py         # Firebase configuration
├── firebase_auth.py          # Firebase authentication functions
├── js/
│   ├── main.js              # Frontend JavaScript logic
│   └── snippets/            # Language-specific code snippets
│       ├── python.js
│       ├── javascript.js
│       ├── java.js
│       └── ... (12 languages)
├── css/
│   └── style.css            # Custom styles
├── README.md                # Project documentation
└── .gitignore              # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Firebase project with Authentication and Firestore enabled
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cpp_typing_practice_separated
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Authentication (Email/Password and Google Sign-in)
   - Enable Firestore Database
   - Download service account key and update `firebase_config.py`
   - Update Firebase Web SDK config in `firebase_config.py`

4. **Configure Google OAuth** (Optional)
   - Create a Google Cloud Project
   - Enable Google+ API
   - Add your domain to authorized origins
   - Update client ID in `index.html`

5. **Run the application**
   ```bash
   python server.py
   ```

6. **Access the application**
   - Open `index.html` in your browser
   - Or serve it through a local server

## 📖 Usage

### Getting Started
1. **Open the application** in your web browser
2. **Create an account** or **sign in** with Firebase authentication
3. **Select a programming language** from the available options
4. **Start typing** the displayed code snippet
5. **Complete the snippet** to save your session to Firestore
6. **View your history** by clicking your username in the navbar

### Features Walkthrough

#### 🔐 Authentication
- **Sign Up**: Create a new account with email and password using Firebase
- **Login**: Access your account with Firebase credentials
- **Google Sign-In**: Quick authentication with Google account via Firebase
- **Logout**: Securely end your session

#### 🎯 Typing Practice
- **Language Selection**: Choose from 12 programming languages
- **Snippet Loading**: Automatic loading of language-specific code snippets
- **Real-time Feedback**: Live WPM, accuracy, and timer updates
- **Error Highlighting**: Visual feedback for typing mistakes
- **Session Completion**: Automatic saving to Firestore when snippet is completed

#### 📊 Performance Tracking
- **WPM Calculation**: Words per minute based on actual typing
- **Accuracy Measurement**: Percentage of correct characters typed
- **Time Tracking**: Session duration in seconds
- **History View**: Access all completed sessions from Firestore
- **Language-specific Stats**: Separate tracking for each language

## 🔧 Configuration

### Firebase Setup
```python
# In firebase_config.py
FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...",
    "client_email": "firebase-adminsdk-xxx@your-project.iam.gserviceaccount.com",
    # ... other config
}

FIREBASE_WEB_CONFIG = {
    "apiKey": "your-api-key",
    "authDomain": "your-project.firebaseapp.com",
    "projectId": "your-project-id",
    # ... other web config
}
```

### Google OAuth Configuration
```html
<!-- In index.html -->
<meta name="google-signin-client_id" content="YOUR_GOOGLE_CLIENT_ID">
```

### Server Configuration
```python
# In server.py
app.run(host='0.0.0.0', port=5000, debug=False)
```

## 📊 API Endpoints

### Authentication
- `POST /api/signup` - User registration with Firebase
- `POST /api/login` - User login with Firebase
- `POST /api/google-login` - Google OAuth login via Firebase

### Typing Sessions
- `POST /api/save-typing-session` - Save completed session to Firestore
- `GET /api/get-typing-history` - Retrieve user history from Firestore
- `GET /api/user-stats/<username>` - Get user statistics

### Health & Status
- `GET /api/health` - Server health check
- `GET /api/languages` - Available languages
- `GET /api/firebase-config` - Get Firebase Web SDK config

## 🎨 Customization

### Adding New Languages
1. Create a new snippet file: `js/snippets/newlanguage.js`
2. Add language button in `index.html`
3. Update language mapping in `server.py`

### Styling
- Modify `css/style.css` for custom styles
- Update Tailwind classes in `index.html`
- Customize color schemes and animations

### Snippets
- Edit files in `js/snippets/` to add/modify code snippets
- Follow the format: `window.snippets = ['snippet1', 'snippet2', ...]`

## 🐛 Troubleshooting

### Common Issues

#### Server Won't Start
- Check if Firebase configuration is correct
- Verify Python dependencies are installed
- Check port 5000 is not in use

#### Authentication Issues
- Verify Firebase project is properly configured
- Check Firebase service account credentials
- Ensure email validation is working

#### Snippets Not Loading
- Check browser console for errors
- Verify snippet files exist in `js/snippets/`
- Ensure file paths are correct

#### Performance Issues
- Clear browser cache
- Check network connectivity
- Verify server is running

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
   
## 🙏 Acknowledgments

- **Flask**: Web framework
- **Firebase**: Authentication and database
- **Firestore**: Cloud database
- **Tailwind CSS**: Styling
- **Google OAuth**: Authentication
- **JWT**: Session management

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Happy Typing! 🚀** 
