// Navigation function
function showPage(pageName) {
  // Check if user is logged in for protected pages (only history requires login)
  const authToken = localStorage.getItem('authToken');
  if (pageName === 'history' && !authToken) {
    showMessage('login-message', 'Please login first to view your typing history.', 'error');
    showPage('login');
    return;
  }
  
  document.querySelectorAll('.page').forEach(page => page.classList.add('hidden'));
  const selectedPage = document.getElementById(pageName);
  if (selectedPage) selectedPage.classList.remove('hidden');
  
  // Clear form fields when showing pages
  clearFormFields(pageName);
  
  // Only hide game container when showing practice page if:
  // 1. User is not logged in, OR
  // 2. No active language is selected (no lesson card has 'active' class)
  if (pageName === 'practice') {
    const authToken = localStorage.getItem('authToken');
    const activeLanguage = document.querySelector('.lesson-card.active');
    
    // Hide game container only if user is not logged in OR no language is selected
    if (!authToken || !activeLanguage) {
      const gameContainer = document.getElementById('game-container');
      if (gameContainer) {
        gameContainer.classList.add('hidden');
      }
    }
    // If user is logged in and has an active language, keep game container visible
  }
}

// Clear form fields based on page
function clearFormFields(pageName) {
  if (pageName === 'login') {
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('login-message').classList.add('hidden');
  } else if (pageName === 'signup') {
    document.getElementById('signup-username').value = '';
    document.getElementById('signup-email').value = '';
    document.getElementById('signup-password').value = '';
    document.getElementById('signup-confirm-password').value = '';
    document.getElementById('signup-message').classList.add('hidden');
  }
  // Removed practice page clearing - typing field stays as is
}

// Authentication state
let currentUser = null;
let googleClient = null;
let availableLanguages = {};
let currentLanguageSnippets = [];
let currentSnippetIndex = 0;
let currentLanguage = 'python'; // Track current language
let firebaseApp = null;
let firebaseAuth = null;

// Google OAuth Configuration
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // Replace with your actual Google Client ID

// Initialize Firebase
async function initializeFirebase() {
  try {
    // Get Firebase configuration from server
    const response = await fetch('http://localhost:5000/api/firebase-config');
    const data = await response.json();
    
    if (data.success && data.config) {
      // Initialize Firebase
      firebaseApp = firebase.initializeApp(data.config);
      firebaseAuth = firebase.auth();
      
      // Test Firebase connection with a simple operation
      try {
        // Try to get current user (this will fail if API key is invalid)
        await firebaseAuth.currentUser;
        
        // Set up auth state listener
        firebaseAuth.onAuthStateChanged((user) => {
          if (user) {
            console.log('✅ Firebase user signed in:', user.email);
            currentUser = {
              uid: user.uid,
              username: user.displayName || user.email.split('@')[0],
              email: user.email,
              displayName: user.displayName
            };
            updateAuthUI(true);
          } else {
            console.log('🔒 Firebase user signed out');
            currentUser = null;
            updateAuthUI(false);
          }
        });
        
        console.log('✅ Firebase initialized successfully');
        return true;
      } catch (firebaseError) {
        console.log('❌ Firebase connection test failed:', firebaseError);
        // Disable Firebase if connection fails
        firebaseApp = null;
        firebaseAuth = null;
        return false;
      }
    } else {
      console.log('⚠️ Firebase not configured, using traditional auth');
      return false;
    }
  } catch (error) {
    console.log('⚠️ Firebase initialization failed:', error);
    return false;
  }
}

// Initialize Google Sign-In
function initializeGoogleSignIn() {
  google.accounts.id.initialize({
    client_id: GOOGLE_CLIENT_ID,
    callback: handleGoogleSignIn
  });
  
  // Render Google Sign-In buttons
  google.accounts.id.renderButton(
    document.getElementById('google-signin-login'),
    { 
      theme: 'outline', 
      size: 'large',
      text: 'signin_with',
      width: '100%'
    }
  );
  
  google.accounts.id.renderButton(
    document.getElementById('google-signin-signup'),
    { 
      theme: 'outline', 
      size: 'large',
      text: 'signup_with',
      width: '100%'
    }
  );
}

// Handle Google Sign-In callback
async function handleGoogleSignIn(response) {
  try {
    const result = await fetch('http://localhost:5000/api/google-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        credential: response.credential 
      })
    });

    const data = await result.json();
    
    if (data.success) {
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('username', data.username);
      localStorage.setItem('userEmail', data.email);
      currentUser = { 
        username: data.username, 
        token: data.token,
        email: data.email,
        isGoogleUser: true
      };
      updateAuthUI(true);
      showMessage('login-message', 'Google login successful!', 'success');
      
      // Clear typing field when user logs in via Google
      clearTypingField();
      
      // Hide game container when user logs in via Google
      const gameContainer = document.getElementById('game-container');
      if (gameContainer) {
        gameContainer.classList.add('hidden');
      }
      
      setTimeout(() => showPage('home'), 1000);
    } else {
      showMessage('login-message', data.message || 'Google login failed', 'error');
    }
  } catch (err) {
    console.error('❌ Google Sign-In Error:', err.message);
    showMessage('login-message', 'Network error. Please try again.', 'error');
  }
}

// Check if user is logged in on page load
function checkAuthStatus() {
  const token = localStorage.getItem('authToken');
  const username = localStorage.getItem('username');
  
  console.log('🔧 checkAuthStatus:', { token: !!token, username });
  
  if (token && username) {
    currentUser = { 
      username, 
      token,
      email: localStorage.getItem('userEmail'),
      isGoogleUser: localStorage.getItem('isGoogleUser') === 'true'
    };
    console.log('🔧 Setting currentUser:', currentUser);
    updateAuthUI(true);
  } else {
    console.log('🔧 No auth token or username found');
    updateAuthUI(false);
  }
}

// Update authentication UI
function updateAuthUI(isLoggedIn) {
  const authLinks = document.getElementById('auth-links');
  const userInfo = document.getElementById('user-info');
  const usernameDisplay = document.getElementById('username-display');
  
  console.log('🔧 updateAuthUI called:', { isLoggedIn, currentUser });
  
  if (isLoggedIn && currentUser) {
    authLinks.classList.add('hidden');
    userInfo.classList.remove('hidden');
    usernameDisplay.textContent = currentUser.username;
    console.log(`👤 User logged in: ${currentUser.username}`);
    
    // Clear typing field when user logs in
    clearTypingField();
  } else {
    authLinks.classList.remove('hidden');
    userInfo.classList.add('hidden');
    usernameDisplay.textContent = '';
    console.log('👤 User logged out');
  }
}

// Load snippets from local text file
async function loadSnippetsFromFile(language) {
  try {
    // Try to load from js/snippets/ folder first
    const scriptPath = `js/snippets/${language}.js`;
    
    try {
      // Load the script dynamically
      const script = document.createElement('script');
      script.src = scriptPath;
      script.type = 'text/javascript';
      
      // Create a promise to wait for the script to load
      const loadPromise = new Promise((resolve, reject) => {
        script.onload = () => {
          // Check if snippets were loaded into window object
          if (window.snippets && window.snippets.length > 0) {
            const snippets = [...window.snippets]; // Copy the array
            window.snippets = []; // Clear for next load
            resolve(snippets);
          } else {
            reject(new Error('No snippets found in loaded file'));
          }
        };
        script.onerror = () => reject(new Error(`Failed to load ${scriptPath}`));
      });
      
      // Add script to document
      document.head.appendChild(script);
      
      // Wait for the script to load
      const snippets = await loadPromise;
      
      currentLanguageSnippets = snippets;
      currentSnippetIndex = 0;
      console.log(`📝 Loaded ${snippets.length} snippets for ${language} from ${scriptPath}`);
      return snippets;
      
    } catch (importError) {
      console.log(`⚠️ Could not load ${scriptPath}, using fallback snippets`);
    }
    
    // Fallback to built-in snippets if file doesn't exist
    const snippets = getDefaultSnippets(language);
    
    currentLanguageSnippets = snippets;
    currentSnippetIndex = 0;
    
    console.log(`📝 Loaded ${snippets.length} fallback snippets for ${language}`);
    return snippets;
  } catch (err) {
    console.error(`❌ Error loading ${language} snippets:`, err.message);
    return [];
  }
}

// Get default snippets for each language
function getDefaultSnippets(language) {
  const snippets = {
    'python': [
      'print("Hello, World!")',
      'for i in range(10):\n    print(i)',
      'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)',
      'numbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers]',
      'class Person:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        return f"Hello, {self.name}!"'
    ],
    'javascript': [
      'console.log("Hello, World!");',
      'for (let i = 0; i < 10; i++) {\n    console.log(i);\n}',
      'function factorial(n) {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}',
      'const numbers = [1, 2, 3, 4, 5];\nconst squares = numbers.map(x => x**2);',
      'class Person {\n    constructor(name) {\n        this.name = name;\n    }\n    greet() {\n        return `Hello, ${this.name}!`;\n    }\n}'
    ],
    'java': [
      'System.out.println("Hello, World!");',
      'for (int i = 0; i < 10; i++) {\n    System.out.println(i);\n}',
      'public static int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}',
      'List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);\nList<Integer> squares = numbers.stream().map(x -> x*x).collect(Collectors.toList());',
      'public class Person {\n    private String name;\n    public Person(String name) {\n        this.name = name;\n    }\n    public String greet() {\n        return "Hello, " + name + "!";\n    }\n}'
    ],
    'cpp': [
      '#include <iostream>\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
      'for (int i = 0; i < 10; i++) {\n    std::cout << i << std::endl;\n}',
      'int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}',
      '#include <vector>\n#include <algorithm>\nstd::vector<int> numbers = {1, 2, 3, 4, 5};\nstd::transform(numbers.begin(), numbers.end(), numbers.begin(), [](int x) { return x*x; });',
      'class Person {\nprivate:\n    std::string name;\npublic:\n    Person(const std::string& n) : name(n) {}\n    std::string greet() const {\n        return "Hello, " + name + "!";\n    }\n};'
    ],
    'csharp': [
      'Console.WriteLine("Hello, World!");',
      'for (int i = 0; i < 10; i++) {\n    Console.WriteLine(i);\n}',
      'public static int Factorial(int n) {\n    if (n <= 1) return 1;\n    return n * Factorial(n-1);\n}',
      'var numbers = new List<int> { 1, 2, 3, 4, 5 };\nvar squares = numbers.Select(x => x * x).ToList();',
      'public class Person {\n    private string name;\n    public Person(string name) {\n        this.name = name;\n    }\n    public string Greet() {\n        return $"Hello, {name}!";\n    }\n}'
    ],
    'php': [
      '<?php\necho "Hello, World!";\n?>',
      '<?php\nfor ($i = 0; $i < 10; $i++) {\n    echo $i . "\\n";\n}\n?>',
      '<?php\nfunction factorial($n) {\n    if ($n <= 1) return 1;\n    return $n * factorial($n-1);\n}\n?>',
      '<?php\n$numbers = [1, 2, 3, 4, 5];\n$squares = array_map(function($x) { return $x * $x; }, $numbers);\n?>',
      '<?php\nclass Person {\n    private $name;\n    public function __construct($name) {\n        $this->name = $name;\n    }\n    public function greet() {\n        return "Hello, " . $this->name . "!";\n    }\n}\n?>'
    ],
    'ruby': [
      'puts "Hello, World!"',
      '10.times do |i|\n    puts i\nend',
      'def factorial(n)\n    return 1 if n <= 1\n    n * factorial(n-1)\nend',
      'numbers = [1, 2, 3, 4, 5]\nsquares = numbers.map { |x| x**2 }',
      'class Person\n    def initialize(name)\n        @name = name\n    end\n    def greet\n        "Hello, #{@name}!"\n    end\nend'
    ],
    'go': [
      'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello, World!")\n}',
      'for i := 0; i < 10; i++ {\n    fmt.Println(i)\n}',
      'func factorial(n int) int {\n    if n <= 1 {\n        return 1\n    }\n    return n * factorial(n-1)\n}',
      'numbers := []int{1, 2, 3, 4, 5}\nfor i, num := range numbers {\n    numbers[i] = num * num\n}',
      'type Person struct {\n    Name string\n}\nfunc (p Person) Greet() string {\n    return "Hello, " + p.Name + "!"\n}'
    ],
    'rust': [
      'fn main() {\n    println!("Hello, World!");\n}',
      'for i in 0..10 {\n    println!("{}", i);\n}',
      'fn factorial(n: u32) -> u32 {\n    if n <= 1 {\n        1\n    } else {\n        n * factorial(n-1)\n    }\n}',
      'let mut numbers = vec![1, 2, 3, 4, 5];\nnumbers.iter_mut().for_each(|x| *x = *x * *x);',
      'struct Person {\n    name: String,\n}\nimpl Person {\n    fn new(name: String) -> Self {\n        Person { name }\n    }\n    fn greet(&self) -> String {\n        format!("Hello, {}!", self.name)\n    }\n}'
    ],
    'swift': [
      'print("Hello, World!")',
      'for i in 0..<10 {\n    print(i)\n}',
      'func factorial(_ n: Int) -> Int {\n    if n <= 1 {\n        return 1\n    }\n    return n * factorial(n-1)\n}',
      'let numbers = [1, 2, 3, 4, 5]\nlet squares = numbers.map { $0 * $0 }',
      'class Person {\n    let name: String\n    init(name: String) {\n        self.name = name\n    }\n    func greet() -> String {\n        return "Hello, \\(name)!"\n    }\n}'
    ],
    'kotlin': [
      'fun main() {\n    println("Hello, World!")\n}',
      'for (i in 0..9) {\n    println(i)\n}',
      'fun factorial(n: Int): Int {\n    return if (n <= 1) 1 else n * factorial(n-1)\n}',
      'val numbers = listOf(1, 2, 3, 4, 5)\nval squares = numbers.map { it * it }',
      'class Person(private val name: String) {\n    fun greet(): String {\n        return "Hello, $name!"\n    }\n}'
    ],
    'typescript': [
      'console.log("Hello, World!");',
      'for (let i = 0; i < 10; i++) {\n    console.log(i);\n}',
      'function factorial(n: number): number {\n    if (n <= 1) return 1;\n    return n * factorial(n-1);\n}',
      'const numbers: number[] = [1, 2, 3, 4, 5];\nconst squares = numbers.map(x => x * x);',
      'class Person {\n    constructor(private name: string) {}\n    greet(): string {\n        return `Hello, ${this.name}!`;\n    }\n}'
    ]
  };
  
  return snippets[language] || ['// No snippets available for this language'];
}

// Get next snippet from current language
function getNextSnippet() {
  if (currentLanguageSnippets.length === 0) {
    return null;
  }
  
  const snippet = currentLanguageSnippets[currentSnippetIndex];
  currentSnippetIndex = (currentSnippetIndex + 1) % currentLanguageSnippets.length;
  
  return snippet;
}

// Load snippet
async function loadSnippet(language) {
  try {
    // Load snippets if not already loaded for this language
    if (currentLanguageSnippets.length === 0) {
      console.log(`🔄 Loading snippets for ${language}...`);
      const snippets = await loadSnippetsFromFile(language);
      if (snippets.length === 0) {
        throw new Error(`No snippets available for ${language}`);
      }
      currentLanguageSnippets = snippets;
      currentSnippetIndex = 0;
      console.log(`✅ Loaded ${snippets.length} snippets for ${language}`);
    }
    
    const snippet = getNextSnippet();
    if (!snippet) {
      throw new Error('No snippet available');
    }
    
    currentSnippet = snippet;
    startTypingUI();
    
    // Show snippet info
    const snippetInfo = document.getElementById('snippet-info');
    if (snippetInfo) {
      snippetInfo.textContent = language.toUpperCase();
    }
    
    console.log(`📝 Loaded ${language} snippet (${currentSnippetIndex}/${currentLanguageSnippets.length})`);
  } catch (err) {
    console.error('❌ Load Snippet Error:', err.message);
    showMessage('snippet-message', 'Failed to load snippet. Please try again.', 'error');
  }
}

// Function to handle language selection
async function selectLanguage(language) {
  try {
    // Set the current language
    currentLanguage = language;
    
    // Remove active class from all cards
    document.querySelectorAll('.lesson-card').forEach(c => c.classList.remove('active'));
    
    // Add active class to the clicked card
    const cards = document.querySelectorAll('.lesson-card');
    for (let card of cards) {
      if (card.textContent.toLowerCase().trim() === language) {
        card.classList.add('active');
        break;
      }
    }
    
    // Reset snippet loading for new language
    currentLanguageSnippets = [];
    currentSnippetIndex = 0;
    
    // Show practice page first
    showPage('practice');
    
    // Load the snippet for the selected language
    await loadSnippet(language);
    
    // Show the game container only after snippet is loaded
    document.getElementById('game-container').classList.remove('hidden');
    
    console.log(`🎯 Language selected: ${language}`);
  } catch (err) {
    console.error('❌ Language Selection Error:', err.message);
    showMessage('snippet-message', 'Failed to load language. Please try again.', 'error');
  }
}

// Login function
async function login(email, password) {
  try {
    // Try Firebase authentication first
    if (firebaseAuth) {
      try {
        console.log('🔥 Using Firebase authentication for login');
        
        // For Firebase authentication, we need the email
        // Use the email provided by the user
        if (!email) {
          showMessage('login-message', 'Please provide your email address for Firebase login', 'error');
          return;
        }
        
        // Sign in with Firebase using email and password
        const userCredential = await firebaseAuth.signInWithEmailAndPassword(email, password);
        const user = userCredential.user;
        
        // Store user info
        localStorage.setItem('authToken', user.uid);
        localStorage.setItem('username', user.displayName || email.split('@')[0]);
        localStorage.setItem('userEmail', email);
        localStorage.setItem('isFirebaseUser', 'true');
        
        currentUser = { 
          uid: user.uid,
          username: user.displayName || email.split('@')[0], 
          email,
          displayName: user.displayName || email.split('@')[0]
        };
        
        updateAuthUI(true);
        showMessage('login-message', 'Login successful with Firebase!', 'success');
        
        // Clear typing field when user logs in
        clearTypingField();
        
        // Hide game container when user logs in
        const gameContainer = document.getElementById('game-container');
        if (gameContainer) {
          gameContainer.classList.add('hidden');
        }
        
        setTimeout(() => showPage('home'), 1000);
        return;
      } catch (firebaseError) {
        console.log('Firebase login failed, trying traditional auth:', firebaseError);
        
        // Check for specific Firebase errors
        if (firebaseError.code === 'auth/api-key-not-valid') {
          showMessage('login-message', 'Firebase configuration error. Please contact administrator.', 'error');
        } else if (firebaseError.code === 'auth/user-not-found') {
          showMessage('login-message', 'User not found. Please check your email and password.', 'error');
        } else if (firebaseError.code === 'auth/wrong-password') {
          showMessage('login-message', 'Incorrect password. Please try again.', 'error');
        } else if (firebaseError.code === 'auth/invalid-email') {
          showMessage('login-message', 'Invalid email format.', 'error');
        } else {
          showMessage('login-message', `Firebase login failed: ${firebaseError.message}`, 'error');
        }
        return;
      }
    }
    
    // Traditional authentication (Firebase-only now)
    console.log('🔧 Using Firebase authentication for login');
    
    // For Firebase-only authentication, we need the email
    // The frontend should store the email during signup and send it during login
    const storedEmail = localStorage.getItem('userEmail') || '';
    
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email.split('@')[0], password, email })
    });

    const data = await response.json();
    
    if (data.success) {
      localStorage.setItem('authToken', data.token);
      localStorage.setItem('username', email.split('@')[0]);
      localStorage.setItem('isGoogleUser', 'false');
      currentUser = { 
        username: email.split('@')[0], 
        token: data.token,
        isGoogleUser: false
      };
      updateAuthUI(true);
      showMessage('login-message', 'Login successful!', 'success');
      
      // Clear typing field when user logs in
      clearTypingField();
      
      // Hide game container when user logs in
      const gameContainer = document.getElementById('game-container');
      if (gameContainer) {
        gameContainer.classList.add('hidden');
      }
      
      setTimeout(() => showPage('home'), 1000);
    } else {
      showMessage('login-message', data.message || 'Login failed', 'error');
    }
  } catch (err) {
    console.error('❌ Login Error:', err.message);
    showMessage('login-message', 'Network error. Please try again.', 'error');
  }
}

// Signup function
async function signup(username, email, password) {
  try {
    console.log(`🚀 Starting signup for: ${username} with email: ${email}`);
    
    // Validate email format
    if (!validateEmail(email)) {
      console.log(`❌ Email format validation failed for: ${email}`);
      showMessage('signup-message', 'Please enter a valid email address', 'error');
      return;
    }
    console.log(`✅ Email format validation passed for: ${email}`);
    
    // Validate password strength
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.isValid) {
      console.log(`❌ Password validation failed: ${passwordValidation.message}`);
      showMessage('signup-message', passwordValidation.message, 'error');
      return;
    }
    console.log(`✅ Password validation passed`);
    
    // Try Firebase authentication first
    if (firebaseAuth) {
      try {
        console.log('🔥 Using Firebase authentication');
        
        // Create user with Firebase
        const userCredential = await firebaseAuth.createUserWithEmailAndPassword(email, password);
        const user = userCredential.user;
        
        // Update display name
        await user.updateProfile({
          displayName: username
        });
        
        // Send email verification
        await user.sendEmailVerification();
        
        // Store user info
        localStorage.setItem('authToken', user.uid);
        localStorage.setItem('username', username);
        localStorage.setItem('userEmail', email);
        localStorage.setItem('isFirebaseUser', 'true');
        
        currentUser = { 
          uid: user.uid,
          username, 
          email,
          displayName: username
        };
        
        updateAuthUI(true);
        showMessage('signup-message', 'Account created successfully with Firebase! Please check your email for verification.', 'success');
        setTimeout(() => showPage('home'), 1000);
        return;
      } catch (firebaseError) {
        console.log('Firebase signup failed, trying traditional auth:', firebaseError);
        
        // Check for specific Firebase errors
        if (firebaseError.code === 'auth/api-key-not-valid') {
          showMessage('signup-message', 'Firebase configuration error. Please contact administrator.', 'error');
        } else if (firebaseError.code === 'auth/email-already-in-use') {
          showMessage('signup-message', 'This email is already registered. Please login instead.', 'error');
        } else if (firebaseError.code === 'auth/weak-password') {
          showMessage('signup-message', 'Password is too weak. Please use a stronger password.', 'error');
        } else {
          showMessage('signup-message', `Firebase signup failed: ${firebaseError.message}`, 'error');
        }
        return;
      }
    }
    
    // Traditional authentication
    console.log('🔧 Using traditional authentication');
    
    // Check if email domain exists
    console.log(`🔍 Checking domain existence for: ${email}`);
    const domainExists = await checkEmailDomainExists(email);
    console.log(`📊 Domain exists result for ${email}: ${domainExists}`);
    if (!domainExists) {
      console.log(`❌ Domain validation failed for: ${email}`);
      showMessage('signup-message', 'This email domain does not exist. Please use a valid email address.', 'error');
      return;
    }
    console.log(`✅ Domain validation passed for: ${email}`);
    console.log(`🚀 Proceeding with signup for: ${email}`);
    console.log(`🔍 About to check email existence for: ${email}`);
    
    // Check if email already exists
    console.log(`🔍 Checking email existence for: ${email}`);
    const emailExists = await checkEmailExists(email);
    console.log(`📊 Email exists result for ${email}: ${emailExists}`);
    if (emailExists) {
      console.log(`❌ Email already exists: ${email}`);
      showMessage('signup-message', 'This email is already registered', 'error');
      return;
    }
    console.log(`✅ Email availability check passed for: ${email}`);
    
    const response = await fetch('http://localhost:5000/api/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();
    
    if (data.success) {
      // Store email in localStorage for Firebase authentication
      localStorage.setItem('userEmail', email);
      showMessage('signup-message', 'Account created successfully! Please login.', 'success');
      setTimeout(() => showPage('login'), 1500);
    } else {
      showMessage('signup-message', data.message || 'Signup failed', 'error');
    }
  } catch (err) {
    console.error('❌ Signup Error:', err.message);
    showMessage('signup-message', 'Network error. Please try again.', 'error');
  }
}

// Logout function
async function logout() {
  // Sign out from Firebase if available
  if (firebaseAuth) {
    try {
      await firebaseAuth.signOut();
      console.log('🔥 Signed out from Firebase');
    } catch (error) {
      console.log('Firebase signout error:', error);
    }
  }
  
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('isGoogleUser');
  localStorage.removeItem('isFirebaseUser');
  currentUser = null;
  updateAuthUI(false);
  
  // Clear typing field and snippet display on logout
  clearTypingField();
  
  // Clear snippet display
  const snippetEl = document.getElementById('snippet');
  if (snippetEl) {
    snippetEl.innerHTML = '';
    snippetEl.className = 'text-lg mb-4 whitespace-pre-wrap';
  }
  
  // Hide game container on logout
  const gameContainer = document.getElementById('game-container');
  if (gameContainer) {
    gameContainer.classList.add('hidden');
  }
  
  // Reset typing state variables
  currentSnippet = '';
  startTime = null;
  isTyping = false;
  isCompleted = false;
  wrongCharMap = new Map();
  
  // Reset metrics display
  const timerEl = document.getElementById('timer');
  const accuracyEl = document.getElementById('accuracy');
  const wpmEl = document.getElementById('wpm');
  
  if (timerEl) timerEl.textContent = '0';
  if (accuracyEl) accuracyEl.textContent = '0%';
  if (wpmEl) wpmEl.textContent = '0';
  
  console.log('🧹 Typing field and snippet cleared on logout');
  showPage('home');
}

// Clear all form fields
function clearAllFormFields() {
  // Clear login fields
  const loginUsername = document.getElementById('login-username');
  const loginPassword = document.getElementById('login-password');
  const loginMessage = document.getElementById('login-message');
  
  if (loginUsername) loginUsername.value = '';
  if (loginPassword) loginPassword.value = '';
  if (loginMessage) loginMessage.classList.add('hidden');
  
  // Clear signup fields
  const signupUsername = document.getElementById('signup-username');
  const signupEmail = document.getElementById('signup-email');
  const signupPassword = document.getElementById('signup-password');
  const signupConfirmPassword = document.getElementById('signup-confirm-password');
  const signupMessage = document.getElementById('signup-message');
  
  if (signupUsername) signupUsername.value = '';
  if (signupEmail) signupEmail.value = '';
  if (signupPassword) signupPassword.value = '';
  if (signupConfirmPassword) signupConfirmPassword.value = '';
  if (signupMessage) signupMessage.classList.add('hidden');
  
  // Clear typing input
  const typingInput = document.getElementById('input');
  if (typingInput) typingInput.value = '';
}

// Clear typing field only
function clearTypingField() {
  const typingInput = document.getElementById('input');
  if (typingInput) {
    typingInput.value = '';
    // Also clear any placeholder or default text
    typingInput.placeholder = '';
    // Reset the input field completely
    typingInput.blur();
    typingInput.focus();
    console.log('🧹 Typing field cleared');
  } else {
    console.log('⚠️ Typing input element not found');
  }
}

// Show message helper
function showMessage(elementId, message, type) {
  const element = document.getElementById(elementId);
  element.textContent = message;
  element.className = `mt-4 text-center ${type === 'success' ? 'text-green-400' : 'text-red-400'}`;
  element.classList.remove('hidden');
  
  setTimeout(() => {
    element.classList.add('hidden');
  }, 3000);
}

// Typing practice variables
let currentSnippet = '';
let startTime = null;
let timerInterval = null;
let isTyping = false;
let isCompleted = false;
let wrongCharMap = new Map();

// Initialize Typing UI
function startTypingUI() {
  const snippetEl = document.getElementById('snippet');
  const inputEl = document.getElementById('input');

  document.getElementById('timer').textContent = '0';
  document.getElementById('accuracy').textContent = '0%';
  document.getElementById('wpm').textContent = '0';

  inputEl.value = '';
  console.log('🧹 Typing field cleared in startTypingUI');
  inputEl.focus();
  inputEl.removeEventListener('input', handleInput);
  inputEl.addEventListener('input', handleInput);

  snippetEl.innerHTML = highlightSnippet('', currentSnippet);
  snippetEl.className = 'text-lg mb-4 whitespace-pre-wrap';

  startTime = null;
  isTyping = false;
  isCompleted = false;
  wrongCharMap = new Map();
}

// Handle Input
function handleInput() {
  const input = document.getElementById('input').value;

  if (!isTyping && input.length > 0) {
    startTimer();
    isTyping = true;
  }

  // Record wrong characters ONLY ON FIRST ERROR per position
  for (let i = 0; i < input.length; i++) {
    if (!wrongCharMap.has(i) && input[i] !== currentSnippet[i]) {
      wrongCharMap.set(i, true);
    }
  }

  // Update colored snippet
  document.getElementById('snippet').innerHTML = highlightSnippet(input, currentSnippet);

  // If fully correct
  if (input === currentSnippet && !isCompleted) {
    stopTimer();
    isCompleted = true;
    
    // Save typing session when completed
    const timeTaken = parseInt(document.getElementById('timer').textContent);
    const wpm = parseFloat(document.getElementById('wpm').textContent);
    const accuracy = parseInt(document.getElementById('accuracy').textContent);
    
    // Use the tracked current language
    const language = currentLanguage || 'python';
    
    // Debug: Log the language being saved
    console.log(`💾 Saving typing session for language: ${language}`);
    
    // Save session to database
    saveTypingSession(language, wpm, accuracy, timeTaken);
  }

  updateMetrics(input);
}

// Highlight Function
function highlightSnippet(input, target) {
  let result = '';
  for (let i = 0; i < target.length; i++) {
    const char = target[i];
    if (i < input.length) {
      result += input[i] === char
        ? `<span class="text-green-500">${char}</span>`
        : `<span class="text-red-500">${char}</span>`;
    } else {
      result += `<span class="text-gray-400">${char}</span>`;
    }
  }
  return result;
}

// Metrics
function updateMetrics(input) {
  const total = input.length;
  const wrong = wrongCharMap.size;

  const accuracy = total > 0 ? Math.round(((total - wrong) / total) * 100) : 0;
  document.getElementById('accuracy').textContent = `${accuracy}%`;

  const time = parseInt(document.getElementById('timer').textContent);
  const wps = time > 0 ? ((input.length / 5) / time).toFixed(2) : 0;
  document.getElementById('wpm').textContent = wps;
}

// Timer
function startTimer() {
  // Reset timer display to 0 first
  document.getElementById('timer').textContent = '0';
  startTime = Date.now();
  timerInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById('timer').textContent = elapsed;
  }, 1000);
}
function stopTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}

// Reset
function resetGame() {
  stopTimer();
  startTypingUI();
}

// Load another
async function generateNewSnippet() {
  const lang = currentLanguage || 'python';
  
  // If we don't have snippets loaded for this language, load them
  if (currentLanguageSnippets.length === 0) {
    await loadSnippet(lang);
  } else {
    // Just get the next snippet from the already loaded array
    const snippet = getNextSnippet();
    if (snippet) {
      currentSnippet = snippet;
      startTypingUI();
      console.log(`📝 Generated new ${lang} snippet (${currentSnippetIndex}/${currentLanguageSnippets.length})`);
    } else {
      console.error('❌ No more snippets available');
    }
  }
}

// Note: Language selection is now handled by onclick attributes in HTML
// which call selectLanguage() function directly

// Save typing session to database
async function saveTypingSession(language, wpm, accuracy, timeTaken) {
  if (!currentUser) return;
  
  try {
    const response = await fetch('http://localhost:5000/api/save-typing-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: currentUser.username,
        language: language,
        wpm: wpm,
        accuracy: accuracy,
        time_taken: timeTaken
      })
    });

    const data = await response.json();
    if (data.success) {
      console.log(`✅ Typing session saved: ${language} - WPM: ${wpm}, Accuracy: ${accuracy}%`);
    } else {
      console.error('❌ Failed to save typing session:', data.message);
    }
  } catch (err) {
    console.error('❌ Error saving typing session:', err.message);
  }
}

// Show typing history page
async function showTypingHistory() {
  if (!currentUser) return;
  
  showPage('history');
  
  // Show loading
  document.getElementById('loading-history').classList.remove('hidden');
  document.getElementById('no-history').classList.add('hidden');
  document.getElementById('history-sessions').innerHTML = '';
  
  try {
    const response = await fetch(`http://localhost:5000/api/get-typing-history?username=${currentUser.username}`);
    const data = await response.json();
    
    // Hide loading
    document.getElementById('loading-history').classList.add('hidden');
    
    if (data.success && data.sessions.length > 0) {
      displayTypingHistory(data.sessions);
    } else {
      // Show no history message
      document.getElementById('no-history').classList.remove('hidden');
    }
  } catch (err) {
    console.error('❌ Error loading typing history:', err.message);
    document.getElementById('loading-history').classList.add('hidden');
    document.getElementById('no-history').classList.remove('hidden');
  }
}

// Display typing history
function displayTypingHistory(sessions) {
  const container = document.getElementById('history-sessions');
  container.innerHTML = '';
  
  sessions.forEach(session => {
    const card = document.createElement('div');
    card.className = 'bg-gray-800 rounded-lg p-6 shadow-lg';
    
    const timeDisplay = session.time_taken ? `${session.time_taken}s` : 'undefineds';
    
    // Format the date for display
    const date = new Date(session.date);
    const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    
    card.innerHTML = `
      <div class="flex justify-between items-start mb-4">
        <div class="text-lg font-semibold text-blue-400">${session.practice_type}</div>
        <div class="text-sm text-gray-400">${formattedDate}</div>
      </div>
      <div class="grid grid-cols-3 gap-4 text-sm">
        <div class="text-center">
          <div class="text-gray-400">WPM</div>
          <div class="text-xl font-bold text-green-400">${session.wpm}</div>
        </div>
        <div class="text-center">
          <div class="text-gray-400">Accuracy</div>
          <div class="text-xl font-bold text-blue-400">${session.accuracy}%</div>
        </div>
        <div class="text-center">
          <div class="text-gray-400">Time</div>
          <div class="text-xl font-bold text-purple-400">${timeDisplay}</div>
        </div>
      </div>
    `;
    
    container.appendChild(card);
  });
}

// Form event listeners
document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Initializing Typing Practice Application...');
  
  // Initialize Firebase first
  const firebaseInitialized = await initializeFirebase();
  console.log(`🔥 Firebase initialization: ${firebaseInitialized ? 'success' : 'fallback'}`);
  
  // Check authentication status
  checkAuthStatus();
  
  // Clear login/signup fields on page load (but not typing field)
  const loginUsername = document.getElementById('login-username');
  const loginPassword = document.getElementById('login-password');
  const loginMessage = document.getElementById('login-message');
  
  if (loginUsername) loginUsername.value = '';
  if (loginPassword) loginPassword.value = '';
  if (loginMessage) loginMessage.classList.add('hidden');
  
  const signupUsername = document.getElementById('signup-username');
  const signupEmail = document.getElementById('signup-email');
  const signupPassword = document.getElementById('signup-password');
  const signupConfirmPassword = document.getElementById('signup-confirm-password');
  const signupMessage = document.getElementById('signup-message');
  
  if (signupUsername) signupUsername.value = '';
  if (signupEmail) signupEmail.value = '';
  if (signupPassword) signupPassword.value = '';
  if (signupConfirmPassword) signupConfirmPassword.value = '';
  if (signupMessage) signupMessage.classList.add('hidden');
  
  // Initialize Google Sign-In
  if (typeof google !== 'undefined') {
    initializeGoogleSignIn();
  } else {
    // Wait for Google API to load
    window.addEventListener('load', () => {
      if (typeof google !== 'undefined') {
        initializeGoogleSignIn();
      }
    });
  }
  
  // Login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      login(email, password);
    });
  }
  
  // Signup form
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const username = document.getElementById('signup-username').value;
      const email = document.getElementById('signup-email').value;
      const password = document.getElementById('signup-password').value;
      const confirmPassword = document.getElementById('signup-confirm-password').value;
      
      if (password !== confirmPassword) {
        showMessage('signup-message', 'Passwords do not match', 'error');
        return;
      }
      
      if (password.length < 6) {
        showMessage('signup-message', 'Password must be at least 6 characters', 'error');
        return;
      }
      
      signup(username, email, password);
    });
  }
  
  // Reset and generate new buttons
  const resetBtn = document.getElementById('reset-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', resetGame);
  }
  
  const generateNewBtn = document.getElementById('generate-new-btn');
  if (generateNewBtn) {
    generateNewBtn.addEventListener('click', generateNewSnippet);
  }

  // Setup email validation for signup
  setupEmailValidation();
  
  console.log('✅ Application initialized successfully');
  
  // Show home page by default
  showPage('home');
});

// Email validation function
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePassword(password) {
  // Check minimum length
  if (password.length < 8) {
    return {
      isValid: false,
      message: 'Password must be at least 8 characters long'
    };
  }
  
  // Check for at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one uppercase letter'
    };
  }
  
  // Check for at least one lowercase letter
  if (!/[a-z]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one lowercase letter'
    };
  }
  
  // Check for at least one number
  if (!/\d/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one number'
    };
  }
  
  // Check for at least one special character
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)'
    };
  }
  
  return {
    isValid: true,
    message: 'Password is strong'
  };
}

// Check if email domain exists (using server endpoint)
async function checkEmailDomainExists(email) {
  try {
    console.log(`🔍 Checking domain for email: ${email}`);
    const response = await fetch('http://localhost:5000/api/check-email-domain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await response.json();
    console.log(`📡 Server response for ${email}:`, data);
    console.log(`📊 Success: ${data.success}, Exists: ${data.exists}`);
    // For domain validation, we want to return true only if the domain exists
    // The server returns success: true, exists: true for valid domains
    // and success: false, exists: false for invalid domains
    const result = data.exists === true;
    console.log(`✅ Final result for ${email}: ${result}`);
    console.log(`🔍 Server response details - success: ${data.success}, exists: ${data.exists}, message: ${data.message || 'none'}`);
    return result;
  } catch (err) {
    console.error('❌ Error checking email domain:', err.message);
    console.log(`🔄 Falling back to client-side check for: ${email}`);
    // Fallback to basic check if server is not available
    return fallbackDomainCheck(email);
  }
}

// Fallback domain check (basic validation)
function fallbackDomainCheck(email) {
  try {
    const domain = email.split('@')[1];
    if (!domain) return false;
    
    // Check if domain has valid format
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/;
    if (!domainRegex.test(domain)) return false;
    
    // List of common email domains
    const commonDomains = [
      'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
      'icloud.com', 'protonmail.com', 'mail.com', 'live.com', 'msn.com',
      'yandex.com', 'zoho.com', 'fastmail.com', 'tutanota.com'
    ];
    
    // If it's a common domain, assume it exists
    if (commonDomains.includes(domain.toLowerCase())) {
      return true;
    }
    
    // For other domains, we can't verify without server, so return false to be safe
    console.log(`⚠️ Domain ${domain} not in common list, returning false for safety`);
    return false;
  } catch (err) {
    console.error('❌ Error in fallback domain check:', err.message);
    return false;
  }
}

// Check if email exists in database
async function checkEmailExists(email) {
  try {
    const response = await fetch('http://localhost:5000/api/check-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await response.json();
    return data.exists;
  } catch (err) {
    console.error('❌ Error checking email:', err.message);
    return false;
  }
}

// Real-time email validation
function setupEmailValidation() {
  const emailInput = document.getElementById('signup-email');
  const emailMessage = document.getElementById('email-validation-message');
  
  if (emailInput) {
    emailInput.addEventListener('blur', async () => {
      const email = emailInput.value.trim();
      
      if (email === '') {
        if (emailMessage) {
          emailMessage.textContent = '';
          emailMessage.classList.add('hidden');
        }
        return;
      }
      
      // Check email format
      if (!validateEmail(email)) {
        if (emailMessage) {
          emailMessage.textContent = 'Please enter a valid email address';
          emailMessage.className = 'mt-2 text-sm text-red-400';
          emailMessage.classList.remove('hidden');
        }
        return;
      }
      
      // Check if email domain exists
      const domainExists = await checkEmailDomainExists(email);
      if (!domainExists) {
        if (emailMessage) {
          emailMessage.textContent = 'This email domain does not exist';
          emailMessage.className = 'mt-2 text-sm text-red-400';
          emailMessage.classList.remove('hidden');
        }
        return;
      }
      
      // Check if email already exists in database
      const exists = await checkEmailExists(email);
      if (exists) {
        if (emailMessage) {
          emailMessage.textContent = 'This email is already registered';
          emailMessage.className = 'mt-2 text-sm text-red-400';
          emailMessage.classList.remove('hidden');
        }
      } else {
        if (emailMessage) {
          emailMessage.textContent = 'Email is available';
          emailMessage.className = 'mt-2 text-sm text-green-400';
          emailMessage.classList.remove('hidden');
        }
      }
    });
    
    // Clear message when user starts typing
    emailInput.addEventListener('input', () => {
      if (emailMessage) {
        emailMessage.textContent = '';
        emailMessage.classList.add('hidden');
      }
    });
  }
}
