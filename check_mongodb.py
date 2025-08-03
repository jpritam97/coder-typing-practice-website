from pymongo import MongoClient

try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['typing_practice']
    users = db['users']
    
    print("📊 Users in MongoDB Database:")
    print("=" * 40)
    
    user_count = users.count_documents({})
    print(f"Total users: {user_count}")
    
    if user_count > 0:
        print("\nUser details:")
        for user in users.find():
            print(f"  Email: {user['email']}")
            print(f"  Username: {user.get('username', 'N/A')}")
            print(f"  Created: {user.get('created_at', 'N/A')}")
            print("  " + "-" * 30)
    else:
        print("No users found in database")
        
    # Check if test@example.com exists
    test_user = users.find_one({"email": "test@example.com"})
    if test_user:
        print(f"\n❌ User with email 'test@example.com' already exists!")
        print(f"   Username: {test_user.get('username', 'N/A')}")
    else:
        print(f"\n✅ Email 'test@example.com' is available for registration")
        
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    print("Make sure MongoDB is running on localhost:27017") 