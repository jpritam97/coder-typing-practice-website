@echo off
echo MongoDB Atlas Setup
echo ===================
echo.

echo This script will help you set up MongoDB Atlas connection.
echo.
echo Steps:
echo 1. Go to https://www.mongodb.com/atlas
echo 2. Create a free account
echo 3. Create a new cluster (free tier)
echo 4. Click "Connect" and choose "Connect your application"
echo 5. Copy the connection string
echo.

set /p MONGODB_URI="Paste your MongoDB Atlas connection string here: "

if "%MONGODB_URI%"=="" (
    echo ❌ No connection string provided
    pause
    exit /b 1
)

echo.
echo Setting environment variable...
setx MONGODB_ATLAS_URI "%MONGODB_URI%"

if errorlevel 1 (
    echo ❌ Failed to set environment variable
    pause
    exit /b 1
)

echo ✅ MongoDB Atlas connection string set successfully!
echo.
echo You may need to restart your terminal/command prompt for the changes to take effect.
echo.
echo To test the connection, run: python server.py
echo.
pause 