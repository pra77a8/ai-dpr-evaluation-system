import os
import logging
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection with error handling
MONGODB_URL = os.getenv("MONGODB_URL") or os.getenv("RENDER_DATABASE_URL")

# Validate that we have a proper MongoDB URL, especially in production
if not MONGODB_URL:
    if os.getenv("RENDER"):
        logger.error("CRITICAL: MONGODB_URL environment variable is not set in Render deployment")
        logger.error("Please set MONGODB_URL in your Render dashboard with a MongoDB Atlas SRV connection string")
        logger.error("Example: mongodb+srv://username:password@cluster.mongodb.net/database_name")
        # We'll still fall back to localhost for now, but this should be fixed
        MONGODB_URL = "mongodb://localhost:27017"
    else:
        logger.info("Using localhost MongoDB for development")
        MONGODB_URL = "mongodb://localhost:27017"

# If we're on Render, make sure we have a proper MongoDB URL
if os.getenv("RENDER"):
    if not os.getenv("MONGODB_URL"):
        logger.error("CRITICAL: Running on Render but MONGODB_URL environment variable is not set")
        logger.error("Please set MONGODB_URL in your Render dashboard with your MongoDB Atlas SRV connection string")
        logger.error("Format: mongodb+srv://username:password@cluster.mongodb.net/database_name")
    elif "localhost" in MONGODB_URL:
        logger.error("CRITICAL: Running on Render but MONGODB_URL is pointing to localhost")
        logger.error("Please update MONGODB_URL in your Render dashboard with your MongoDB Atlas SRV connection string")
        logger.error("Format: mongodb+srv://username:password@cluster.mongodb.net/database_name")

# Log the MongoDB URL (without credentials for security)
if MONGODB_URL and "mongodb" in MONGODB_URL:
    # Mask the credentials in the log
    try:
        from urllib.parse import urlparse
        parsed = urlparse(MONGODB_URL)
        masked_url = f"{parsed.scheme}://****:****@{parsed.hostname}{parsed.path}"
        logger.info(f"Attempting to connect to MongoDB at: {masked_url}")
    except Exception as e:
        logger.info(f"Attempting to connect to MongoDB (URL parsing failed): {e}")
else:
    logger.info(f"Attempting to connect to MongoDB at: {MONGODB_URL}")

# Initialize client as None
client = None
database = None

try:
    client = MongoClient(
        MONGODB_URL, 
        serverSelectionTimeoutMS=10000,  # Increased timeout
        connectTimeoutMS=20000,
        socketTimeoutMS=20000
    )
    # Test the connection
    client.admin.command('ping')
    logger.info("MongoDB connection successful")
    
    # Access database
    database = client.dpr_evaluation_system
    # Test database access
    database.list_collection_names()
    logger.info("Database access successful")
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    # If we're on Render, this is a critical error
    if os.getenv("RENDER"):
        logger.error("CRITICAL: MongoDB connection failed on Render. Check your MONGODB_URL environment variable.")
        logger.error("Common issues and solutions:")
        logger.error("1. Incorrect username or password - Verify your credentials")
        logger.error("2. Database user not created in MongoDB Atlas - Create a database user in Atlas")
        logger.error("3. Network access not configured - Add Render's IP to MongoDB Atlas whitelist")
        logger.error("4. Database user doesn't have access - Ensure user has read/write permissions")
        logger.error("5. Wrong connection string format - Must use mongodb+srv:// not mongodb://")
        logger.error("")
        logger.error("To fix this:")
        logger.error("1. Go to your Render dashboard")
        logger.error("2. Select your service")
        logger.error("3. Go to Environment tab")
        logger.error("4. Add MONGODB_URL with your MongoDB Atlas SRV connection string")
        logger.error("5. Redeploy your service")
    else:
        logger.info("Using in-memory fallback for development")
        # Create a mock database for development/testing
        from pymongo import MongoClient as MockMongoClient
        client = MockMongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1)
        database = client.dpr_evaluation_system

# Collections (with fallback)
try:
    if database is not None:
        users_collection = database.get_collection("users")
        dprs_collection = database.get_collection("dprs")
        risks_collection = database.get_collection("risks")
        feedbacks_collection = database.get_collection("feedbacks")
    else:
        logger.error("Database is None, cannot create collections")
        # Create mock collections for development
        from pymongo import MongoClient as MockMongoClient
        mock_client = MockMongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1)
        mock_db = mock_client.dpr_evaluation_system
        users_collection = mock_db.get_collection("users")
        dprs_collection = mock_db.get_collection("dprs")
        risks_collection = mock_db.get_collection("risks")
        feedbacks_collection = mock_db.get_collection("feedbacks")
except Exception as e:
    logger.error(f"Failed to create collections: {e}")
    # Create mock collections as fallback
    try:
        from pymongo import MongoClient as MockMongoClient
        mock_client = MockMongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1)
        mock_db = mock_client.dpr_evaluation_system
        users_collection = mock_db.get_collection("users")
        dprs_collection = mock_db.get_collection("dprs")
        risks_collection = mock_db.get_collection("risks")
        feedbacks_collection = mock_db.get_collection("feedbacks")
    except Exception as e2:
        logger.error(f"Failed to create mock collections: {e2}")
        # Set to None as last resort
        users_collection = None
        dprs_collection = None
        risks_collection = None
        feedbacks_collection = None

def get_database():
    return database

def get_users_collection():
    return users_collection

def get_dprs_collection():
    return dprs_collection

def get_risks_collection():
    return risks_collection

def get_feedbacks_collection():
    return feedbacks_collection