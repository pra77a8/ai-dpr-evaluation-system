# Example of improved MongoDB connection handling in FastAPI backend
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# MongoDB connection with error handling
def get_database():
    MONGODB_URL = os.getenv("MONGODB_URL")
    if not MONGODB_URL:
        raise ValueError("MONGODB_URL environment variable not set")
    
    try:
        # Create client with timeout settings
        client = MongoClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        return client
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"MongoDB connection failed: {e}")
        # Don't raise exception here to allow application to start
        # but log the error and handle gracefully in routes
        return None
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        return None

# Initialize database connection
db_client = get_database()
db = db_client["your_database_name"] if db_client else None

# Example route with database error handling
@app.get("/api/test-db")
async def test_db():
    if not db:
        raise HTTPException(
            status_code=500, 
            detail="Database connection not available"
        )
    
    try:
        # Test database operation
        collection = db["test_collection"]
        count = collection.count_documents({})
        return {"message": f"Database connection OK, found {count} documents"}
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Database operation failed: {str(e)}"
        )