@echo off
echo Installing MongoDB dependencies...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install pymongo
echo Installing pymongo...
pip install pymongo==4.6.1

if errorlevel 1 (
    echo ❌ Failed to install pymongo
    pause
    exit /b 1
)

echo ✅ pymongo installed successfully
echo.
echo 🎉 MongoDB dependencies installed!
echo.
echo Next steps:
echo 1. Set up MongoDB Atlas (recommended) or local MongoDB
echo 2. Set MONGODB_ATLAS_URI environment variable (for Atlas)
echo 3. Run: python server.py
echo.
pause 