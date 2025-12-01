from pymongo import MongoClient

def check_users():
    """
    Check if users are being stored properly in the database
    """
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['dpr_evaluation_system']
        users_collection = db['users']
        
        # Count users
        count = users_collection.count_documents({})
        print(f"Total users in database: {count}")
        
        # Show all users
        if count > 0:
            print("\nUser details:")
            print("-" * 50)
            cursor = users_collection.find()
            for user in cursor:
                print(f"ID: {user.get('_id')}")
                print(f"Name: {user.get('name', 'N/A')}")
                print(f"Email: {user.get('email', 'N/A')}")
                print(f"Role: {user.get('role', 'N/A')}")
                print("-" * 30)
        else:
            print("No users found in the database")
            
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"Error checking users: {e}")

if __name__ == "__main__":
    check_users()