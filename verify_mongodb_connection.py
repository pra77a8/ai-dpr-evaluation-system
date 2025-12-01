#!/usr/bin/env python3
"""
Script to verify MongoDB connection for the AI DPR Evaluation System
This script helps diagnose MongoDB connection issues in deployment.
"""

import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_mongodb_connection():
    """Verify MongoDB connection with detailed diagnostics"""
    
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URL
    mongodb_url = os.getenv("MONGODB_URL") or os.getenv("RENDER_DATABASE_URL")
    
    print("=" * 60)
    print("MongoDB Connection Verification Script")
    print("=" * 60)
    
    # Check if running on Render
    is_render = bool(os.getenv("RENDER"))
    print(f"Environment: {'Render' if is_render else 'Local Development'}")
    
    # Display current MongoDB URL configuration
    if mongodb_url:
        # Mask credentials for security
        try:
            from urllib.parse import urlparse
            parsed = urlparse(mongodb_url)
            masked_url = f"{parsed.scheme}://****:****@{parsed.hostname}{parsed.path}"
            print(f"MONGODB_URL: {masked_url}")
        except Exception:
            print(f"MONGODB_URL: {mongodb_url}")
    else:
        print("MONGODB_URL: NOT SET")
        if is_render:
            print("❌ CRITICAL: MONGODB_URL must be set in Render environment!")
            return False
    
    # Validate connection string format
    if mongodb_url:
        if mongodb_url.startswith("mongodb+srv://"):
            print("✅ Connection string format: Correct (SRV format)")
        elif mongodb_url.startswith("mongodb://"):
            if "localhost" in mongodb_url or "127.0.0.1" in mongodb_url:
                print("⚠️  Connection string format: Local development URL")
                if is_render:
                    print("❌ CRITICAL: Cannot use localhost MongoDB in Render deployment!")
                    return False
            else:
                print("⚠️  Connection string format: Standard format (should use SRV)")
        else:
            print("❌ Connection string format: Invalid")
            return False
    
    # Test connection if URL is available
    if mongodb_url:
        print("\nTesting MongoDB connection...")
        try:
            # Create client with timeout settings
            client = MongoClient(
                mongodb_url,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            client.admin.command('ping')
            print("✅ MongoDB connection: SUCCESS")
            
            # List databases
            try:
                databases = client.list_database_names()
                print(f"📊 Available databases: {len(databases)}")
                if databases:
                    print(f"   First few: {databases[:3]}")
            except Exception as e:
                print(f"⚠️  Could not list databases: {e}")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"❌ MongoDB connection: FAILED")
            print(f"   Error: {e}")
            
            # Provide specific troubleshooting guidance
            if "localhost" in mongodb_url and is_render:
                print("\n🔧 TROUBLESHOOTING:")
                print("   You're trying to connect to localhost MongoDB in Render.")
                print("   Render doesn't have a local MongoDB instance.")
                print("   Solution: Set MONGODB_URL to your MongoDB Atlas connection string.")
            elif "Authentication failed" in str(e):
                print("\n🔧 TROUBLESHOOTING:")
                print("   Authentication failed. Check your username and password.")
                print("   Make sure the database user exists in MongoDB Atlas.")
            elif "timed out" in str(e):
                print("\n🔧 TROUBLESHOOTING:")
                print("   Connection timed out. Possible causes:")
                print("   1. Incorrect hostname in connection string")
                print("   2. Network access not configured in MongoDB Atlas")
                print("   3. Firewall blocking connection")
            return False
    else:
        print("⚠️  No MongoDB URL configured. Cannot test connection.")
        if is_render:
            print("❌ This will cause failures in Render deployment.")
        return False

def show_render_setup_instructions():
    """Show instructions for setting up MongoDB in Render"""
    print("\n" + "=" * 60)
    print("RENDER SETUP INSTRUCTIONS")
    print("=" * 60)
    print("To fix MongoDB connection in Render:")
    print("")
    print("1. Go to your Render dashboard:")
    print("   https://dashboard.render.com/")
    print("")
    print("2. Select your 'ai-dpr-backend-2' service")
    print("")
    print("3. Click on 'Environment' in the left sidebar")
    print("")
    print("4. Add a new environment variable:")
    print("   Name: MONGODB_URL")
    print("   Value: mongodb+srv://username:password@cluster.mongodb.net/database_name")
    print("   (Replace with your actual MongoDB Atlas connection string)")
    print("")
    print("5. Make sure your MongoDB Atlas is configured:")
    print("   - Database user created with proper permissions")
    print("   - Network access whitelist includes 0.0.0.0/0 (or Render's IPs)")
    print("")
    print("6. Redeploy your service")
    print("")

if __name__ == "__main__":
    print("AI DPR Evaluation System - MongoDB Connection Verifier")
    
    success = verify_mongodb_connection()
    
    if not success and os.getenv("RENDER"):
        show_render_setup_instructions()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ MongoDB verification completed successfully!")
        sys.exit(0)
    else:
        print("❌ MongoDB verification failed!")
        print("   Check the error messages above and follow the troubleshooting steps.")
        sys.exit(1)