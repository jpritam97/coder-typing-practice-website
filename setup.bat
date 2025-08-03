@echo off
echo 🚀 Setting up Programming Typing Practice Backend...
echo.

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🔑 Setting up OpenAI API Key...
echo Please enter your OpenAI API key:
set /p OPENAI_API_KEY=

echo.
echo 🌐 Starting Flask server...
echo Server will run on http://localhost:5000
echo Frontend will run on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

set OPENAI_API_KEY=%OPENAI_API_KEY%
python server.py 