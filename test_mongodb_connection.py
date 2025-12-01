#!/usr/bin/env python3
"""
Test script to verify MongoDB connection
"""
import os
import sys
from urllib.parse import urlparse

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_mongodb_url():
    """Test MongoDB URL parsing and validation"""
    mongodb_url = os.getenv("MONGODB_URL") or os.getenv("RENDER_DATABASE_URL") or "mongodb://localhost:27017"
    
    print(f"MongoDB URL: {mongodb_url}")
    
    # Parse the URL
    try:
        parsed = urlparse(mongodb_url)
        print(f"Scheme: {parsed.scheme}")
        print(f"Hostname: {parsed.hostname}")
        print(f"Username: {parsed.username}")
        print(f"Password: {'*' * len(parsed.password) if parsed.password else 'None'}")
        print(f"Path: {parsed.path}")
        
        # Check if it's a valid MongoDB URL
        if parsed.scheme not in ['mongodb', 'mongodb+srv']:
            print("ERROR: Invalid MongoDB scheme")
            return False
            
        if not parsed.hostname:
            print("ERROR: Missing hostname")
            return False
            
        print("MongoDB URL parsing successful")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to parse MongoDB URL: {e}")
        return False

def test_mongodb_connection():
    """Test actual MongoDB connection"""
    try:
        from pymongo import MongoClient
        mongodb_url = os.getenv("MONGODB_URL") or os.getenv("RENDER_DATABASE_URL") or "mongodb://localhost:27017"
        
        print("Attempting to connect to MongoDB...")
        client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test the connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Test database access
        db = client.dpr_evaluation_system
        collections = db.list_collection_names()
        print(f"Available collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to MongoDB: {e}")
        return False

if __name__ == "__main__":
    print("=== MongoDB Connection Test ===")
    
    # Test URL parsing
    print("\n1. Testing URL parsing...")
    if not test_mongodb_url():
        sys.exit(1)
    
    # Test actual connection
    print("\n2. Testing actual connection...")
    if not test_mongodb_connection():
        print("\nConnection test failed. Please check:")
        print("1. Your MONGODB_URL environment variable")
        print("2. That your MongoDB Atlas user exists and has correct credentials")
        print("3. That your MongoDB Atlas network access is configured correctly")
        sys.exit(1)
    
    print("\nAll tests passed!")