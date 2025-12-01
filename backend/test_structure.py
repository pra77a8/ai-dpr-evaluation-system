import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

try:
    # Test importing models
    from app.models.user import UserCreate, UserRole
    from app.models.dpr import DPRCreate, FileType
    from app.models.risk import RiskScore
    from app.models.feedback import FeedbackCreate
    
    # Test importing routes
    from app.routes import auth, dpr, risk, feedback, chat
    
    # Test importing utils
    from app.utils.auth import verify_password, get_password_hash
    from app.utils.dpr_processor import extract_dpr_elements
    
    # Test importing services
    from app.services.risk_calculator import calculate_risk_scores
    from app.services.chatbot import get_dpr_context, generate_response
    
    print("All imports successful! Backend structure is valid.")
    
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)