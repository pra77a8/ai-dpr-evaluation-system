import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URL from environment
MONGODB_URL = os.getenv('MONGODB_URL')

if not MONGODB_URL:
    print("Error: MONGODB_URL environment variable not set")
    exit(1)

print(f"Attempting to connect to: {MONGODB_URL}")

try:
    # Create MongoDB client
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
    
    # List databases
    databases = client.list_database_names()
    print(f"Available databases: {databases}")
    
except Exception as e:
    print(f"MongoDB connection failed: {e}")
finally:
    if 'client' in locals():
        client.close()