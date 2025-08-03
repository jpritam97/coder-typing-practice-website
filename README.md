# Typing Practice Application

A modern web-based typing practice application with authentication, multiple programming languages, and performance tracking.

## 🚀 Features

### ✨ Core Features
- **Multi-language Typing Practice**: Support for 12 programming languages
  - Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, TypeScript
- **Real-time Performance Metrics**: WPM (Words Per Minute), Accuracy, and Time tracking
- **User Authentication**: Traditional login/signup with Google OAuth integration
- **Typing History**: Persistent session storage with MongoDB
- **Responsive Design**: Modern UI with Tailwind CSS

### 🔐 Authentication
- **Traditional Login**: Username/password authentication
- **Google Sign-In**: OAuth 2.0 integration
- **Email Validation**: Domain verification and format checking
- **Session Management**: JWT-based authentication with 7-day expiration

### 📊 Performance Tracking
- **Real-time Metrics**: Live WPM, accuracy, and timer display
- **Session History**: View all completed typing sessions
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
- **Google OAuth**: Client-side authentication integration

### Backend
- **Python**: Flask web framework
- **MongoDB**: NoSQL database for user and session storage
- **PyMongo**: Python MongoDB driver
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
- MongoDB (local or Atlas)
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

3. **Set up MongoDB**
   - Install MongoDB locally, or
   - Use MongoDB Atlas (cloud service)
   - Update connection string in `server.py` if using Atlas

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
2. **Create an account** or **sign in** with existing credentials
3. **Select a programming language** from the available options
4. **Start typing** the displayed code snippet
5. **Complete the snippet** to save your session
6. **View your history** by clicking your username in the navbar

### Features Walkthrough

#### 🔐 Authentication
- **Sign Up**: Create a new account with username, email, and password
- **Login**: Access your account with credentials
- **Google Sign-In**: Quick authentication with Google account
- **Logout**: Securely end your session

#### 🎯 Typing Practice
- **Language Selection**: Choose from 12 programming languages
- **Snippet Loading**: Automatic loading of language-specific code snippets
- **Real-time Feedback**: Live WPM, accuracy, and timer updates
- **Error Highlighting**: Visual feedback for typing mistakes
- **Session Completion**: Automatic saving when snippet is completed

#### 📊 Performance Tracking
- **WPM Calculation**: Words per minute based on actual typing
- **Accuracy Measurement**: Percentage of correct characters typed
- **Time Tracking**: Session duration in seconds
- **History View**: Access all completed sessions
- **Language-specific Stats**: Separate tracking for each language

## 🔧 Configuration

### MongoDB Setup
```python
# In server.py
MONGO_URI = "mongodb://localhost:27017/typing_practice"
# Or for Atlas:
# MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/typing_practice"
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
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `POST /api/google-login` - Google OAuth login

### Typing Sessions
- `POST /api/save-typing-session` - Save completed session
- `GET /api/get-typing-history` - Retrieve user history

### Health & Status
- `GET /api/health` - Server health check
- `GET /api/languages` - Available languages

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
- Check if MongoDB is running
- Verify Python dependencies are installed
- Check port 5000 is not in use

#### Authentication Issues
- Verify Google OAuth client ID is correct
- Check MongoDB connection string
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

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Flask**: Web framework
- **MongoDB**: Database
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