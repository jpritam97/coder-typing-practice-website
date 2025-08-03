# MongoDB Setup Guide

## Option 1: MongoDB Atlas (Recommended - Cloud Database)

**Easiest option - no local installation required**

1. **Create MongoDB Atlas Account:**
   - Go to https://www.mongodb.com/atlas
   - Sign up for a free account
   - Create a new cluster (free tier available)

2. **Get Connection String:**
   - In Atlas dashboard, click "Connect"
   - Choose "Connect your application"
   - Copy the connection string

3. **Set Environment Variable:**
   ```bash
   set MONGODB_ATLAS_URI="mongodb+srv://username:password@cluster.mongodb.net/typing_practice?retryWrites=true&w=majority"
   ```

4. **Start Server:**
   ```bash
   python server.py
   ```

## Option 2: Local MongoDB Installation

### Windows Installation:

1. **Download MongoDB Community Server:**
   - Go to https://www.mongodb.com/try/download/community
   - Download the Windows MSI installer
   - Run the installer and follow the setup wizard

2. **Create Data Directory:**
   ```cmd
   mkdir C:\data\db
   ```

3. **Start MongoDB Service:**
   ```cmd
   mongod --dbpath C:\data\db
   ```

4. **Install Python Dependencies:**
   ```bash
   pip install pymongo bcrypt
   ```

5. **Start Server:**
   ```bash
   python server.py
   ```

## Option 3: Docker MongoDB (Advanced)

1. **Install Docker Desktop:**
   - Download from https://www.docker.com/products/docker-desktop

2. **Run MongoDB Container:**
   ```bash
   docker run -d --name mongodb -p 27017:27017 mongo:latest
   ```

3. **Start Server:**
   ```bash
   python server.py
   ```

## Testing Database Connection

After setup, test the connection:

```bash
# Check if server connects to database
python server.py
```

You should see:
- ✅ Connected to MongoDB Atlas (if using Atlas)
- ✅ Connected to local MongoDB (if using local)
- ⚠️ Running without database (if no MongoDB available)

## Database Features

Once connected, your app will have:

✅ **User Registration & Login**
- Secure password hashing
- User session management
- Email-based authentication

✅ **Persistent Data Storage**
- Typing history per user
- Session statistics (WPM, accuracy, time)
- Cross-device data access

✅ **Real-time Sync**
- Immediate database updates
- No data loss on browser clear
- Backup and recovery

## Troubleshooting

**If you see "Database not available":**
1. Check if MongoDB is running
2. Verify connection string (Atlas)
3. Ensure pymongo is installed: `pip install pymongo`

**If you see "ModuleNotFoundError: No module named 'pymongo'":**
```bash
pip install pymongo bcrypt
```

**For local MongoDB issues:**
1. Ensure MongoDB service is running
2. Check if port 27017 is available
3. Verify data directory exists

## Current Status

The application now supports:
- 🔄 **Hybrid Mode**: Database when available, localStorage fallback
- ☁️ **Cloud Database**: MongoDB Atlas support
- 🏠 **Local Database**: Local MongoDB support
- 📱 **Cross-platform**: Works on any device with internet 