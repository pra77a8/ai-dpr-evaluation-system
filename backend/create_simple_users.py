from pymongo import MongoClient
import hashlib

def create_simple_users():
    """
    Create simple test users for the system without password hashing
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['dpr_evaluation_system']
    users_collection = db['users']
    
    # Test users to create
    test_users = [
        {
            "name": "Test Organization",
            "email": "org@test.com",
            "password": "password123",
            "role": "Organization"
        },
        {
            "name": "Test Civilian",
            "email": "civilian@test.com",
            "password": "password123",
            "role": "Civilian"
        }
    ]
    
    created_users = []
    
    for user_data in test_users:
        # Check if user already exists
        existing_user = users_collection.find_one({"email": user_data["email"]})
        if existing_user:
            print(f"User {user_data['email']} already exists")
            created_users.append(existing_user)
            continue
            
        # Simple "hash" password (just for testing)
        hashed_password = hashlib.sha256(user_data["password"].encode()).hexdigest()
        
        # Create user document
        user_doc = {
            "name": user_data["name"],
            "email": user_data["email"],
            "role": user_data["role"],
            "hashed_password": hashed_password
        }
        
        # Insert user into database
        result = users_collection.insert_one(user_doc)
        user_doc["id"] = str(result.inserted_id)
        
        # Remove hashed_password from response
        del user_doc["hashed_password"]
        
        created_users.append(user_doc)
        print(f"Created user: {user_doc['name']} ({user_doc['email']}) with role {user_doc['role']}")
    
    # Close connection
    client.close()
    
    return created_users

if __name__ == "__main__":
    create_simple_users()