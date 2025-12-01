from app.database import get_users_collection, get_dprs_collection, get_risks_collection, get_feedbacks_collection

def init_db():
    """
    Initialize database with required indexes
    """
    # Create indexes for users collection
    users_collection = get_users_collection()
    users_collection.create_index("email", unique=True)
    
    # Create indexes for dprs collection
    dprs_collection = get_dprs_collection()
    dprs_collection.create_index("uploaded_by")
    
    # Create indexes for risks collection
    risks_collection = get_risks_collection()
    risks_collection.create_index("dpr_id", unique=True)
    
    # Create indexes for feedbacks collection
    feedbacks_collection = get_feedbacks_collection()
    feedbacks_collection.create_index("dpr_id")
    feedbacks_collection.create_index("civilian_id")
    
    print("Database indexes created successfully!")

if __name__ == "__main__":
    init_db()