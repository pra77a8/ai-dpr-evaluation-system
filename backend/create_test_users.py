from app.database import get_users_collection
from app.utils.auth import get_password_hash

def create_test_users():
    """
    Create test users for the system
    """
    users_collection = get_users_collection()
    
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
            
        # Hash password
        hashed_password = get_password_hash(user_data["password"])
        
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
    
    return created_users

if __name__ == "__main__":
    create_test_users()