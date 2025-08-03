@echo off
echo ========================================
echo MongoDB Setup for Typing Practice App
echo ========================================

echo.
echo Step 1: Downloading MongoDB Community Server...
powershell -Command "& {Invoke-WebRequest -Uri 'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4-signed.msi' -OutFile 'mongodb-installer.msi'}"

echo.
echo Step 2: Installing MongoDB...
msiexec /i mongodb-installer.msi /quiet /norestart

echo.
echo Step 3: Creating data directory...
if not exist "C:\data\db" mkdir "C:\data\db"

echo.
echo Step 4: MongoDB installation completed!
echo.
echo Next steps:
echo 1. Restart your computer
echo 2. Open a new command prompt
echo 3. Run: mongod --dbpath C:\data\db
echo 4. In another terminal, run: python server.py
echo.
echo Your typing practice app will now use MongoDB for:
echo - User registration and login
echo - Persistent typing history
echo - Cross-device data access
echo.
pause 