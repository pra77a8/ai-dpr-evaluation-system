#!/usr/bin/env python3
"""
Test script to verify MongoDB connection
"""

import os
import sys
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mongodb_connection():
    """Test MongoDB connection with various methods"""
    
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URL from environment
    mongodb_url = os.getenv("MONGODB_URL") or os.getenv("RENDER_DATABASE_URL") or "mongodb://localhost:27017"
    
    logger.info(f"Testing MongoDB connection to: {mongodb_url}")
    
    try:
        # Create MongoDB client
        client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
        
        # Test connection
        logger.info("Attempting to ping MongoDB...")
        client.admin.command('ping')
        logger.info("✓ MongoDB ping successful")
        
        # Test database access
        logger.info("Attempting to access database...")
        db = client.dpr_evaluation_system
        collections = db.list_collection_names()
        logger.info(f"✓ Database access successful. Collections: {collections}")
        
        # Test inserting a document
        logger.info("Attempting to insert test document...")
        test_collection = db.test_connection
        result = test_collection.insert_one({"test": "connection", "status": "successful"})
        logger.info(f"✓ Document insertion successful. ID: {result.inserted_id}")
        
        # Clean up test document
        test_collection.delete_one({"_id": result.inserted_id})
        logger.info("✓ Test document cleaned up")
        
        logger.info("=== ALL TESTS PASSED ===")
        return True
        
    except Exception as e:
        logger.error(f"✗ MongoDB connection failed: {e}")
        logger.info("=== TEST FAILED ===")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)