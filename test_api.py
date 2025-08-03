import requests
import json

# Test the API endpoints
base_url = "http://localhost:5000"

def test_db_status():
    """Test database connection"""
    response = requests.get(f"{base_url}/api/db-status")
    print("Database Status:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_health():
    """Test server health"""
    response = requests.get(f"{base_url}/api/health")
    print("Server Health:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_generate_snippet():
    """Test snippet generation"""
    data = {
        "language": "python",
        "difficulty": "beginner"
    }
    response = requests.post(f"{base_url}/api/generate-snippet", json=data)
    print("Generate Snippet:")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("Testing Typing Practice API...")
    print("=" * 40)
    
    try:
        test_db_status()
        test_health()
        test_generate_snippet()
        print("✅ All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server not running. Please start the server first:")
        print("   C:\\Users\\jprit\\AppData\\Local\\Programs\\Python\\Python313\\python.exe server.py")
    except Exception as e:
        print(f"❌ Error: {e}") 