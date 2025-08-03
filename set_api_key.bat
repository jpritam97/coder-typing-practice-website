@echo off
echo 🤖 Setting up OpenAI API for Programming Typing Practice
echo.
echo Please enter your OpenAI API key:
set /p OPENAI_API_KEY=

echo.
echo 🔑 API Key set successfully!
echo 🌐 Starting Flask server on port 5000...
echo.
echo Press Ctrl+C to stop the server
echo.

set OPENAI_API_KEY=%OPENAI_API_KEY%
py -3.13 server.py 