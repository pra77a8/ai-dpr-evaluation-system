import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom middleware to log all requests for debugging
class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        response = await call_next(request)
        
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        
        return response

app = FastAPI(
    title="AI-Powered DPR Evaluation System",
    description="Backend API for the AI-Powered DPR Evaluation System",
    version="1.0.0"
)

# Add debug middleware to log all requests
app.add_middleware(DebugMiddleware)

# Add CORS middleware to allow React frontend to communicate with backend
# Using specific origins to allow credentials
# For maximum flexibility in deployment while maintaining security
ALLOWED_ORIGINS = [
    "https://ai-dpr-frontend-pra77a8s-projects.vercel.app",
    "https://ai-dpr-evaluation-system-qrtg.vercel.app",
    "http://localhost:5173",  # Local development
    "http://localhost:3000",   # Alternative local development
    "http://localhost:3001",   # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log that CORS middleware has been added
logger.info(f"CORS middleware added with allowed origins: {ALLOWED_ORIGINS}")
logger.info("Debug middleware added to log all requests")

# Include routers with error handling
try:
    from app.routes import auth, dpr, risk, feedback, chat, ai_chat, reports
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(dpr.router, prefix="/api/dpr", tags=["DPR"])
    app.include_router(risk.router, prefix="/api/risk", tags=["Risk Assessment"])
    app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
    app.include_router(chat.router, prefix="/api/chat", tags=["Chatbot"])
    app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Analysis"])
    app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
    logger.info("All routes loaded successfully")
except ImportError as e:
    logger.error(f"Failed to load routes due to missing dependencies: {e}")
    # Load essential routes without AI dependencies
    try:
        from app.routes import auth, dpr, risk, feedback
        app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
        app.include_router(dpr.router, prefix="/api/dpr", tags=["DPR"])
        app.include_router(risk.router, prefix="/api/risk", tags=["Risk Assessment"])
        app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
        logger.info("Loaded essential routes without AI dependencies")
    except Exception as e2:
        logger.error(f"Failed to load even essential routes: {e2}")
        # Load minimal routes for health checks
        logger.info("Loaded minimal routes for health checks only")
except Exception as e:
    logger.error(f"Failed to load routes: {e}")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "AI-Powered DPR Evaluation System API"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    # Check database connection status
    try:
        from app.database import get_database
        db = get_database()
        if db is not None:
            db.list_collection_names()  # This will raise an exception if connection fails
            return {"status": "healthy", "database": "connected"}
        else:
            return {"status": "healthy", "database": "disconnected"}
    except Exception as e:
        return {"status": "healthy", "database": f"error: {str(e)}"}

# Add a simple health check endpoint for deployment verification
@app.get("/healthz")
async def healthz():
    logger.info("Healthz endpoint accessed")
    return {"status": "ok", "message": "Service is running"}

# Add CORS test endpoint
@app.get("/cors-test")
async def cors_test():
    logger.info("CORS test endpoint accessed")
    return {"message": "CORS is working correctly!", "status": "success"}

# Add a route to serve the sample PDF file
@app.get("/sample_dpr.pdf")
async def get_sample_dpr():
    file_path = os.path.join(os.path.dirname(__file__), "..", "sample_dpr.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename='sample_dpr.pdf')
    else:
        return {"error": "File not found"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    logger.info("CORS configuration should be active")
    try:
        # Test database connection
        from app.database import get_database
        db = get_database()
        if db is not None:
            db.list_collection_names()  # This will raise an exception if connection fails
            logger.info("Database connection verified at startup")
        else:
            logger.warning("Database is None at startup")
    except Exception as e:
        logger.error(f"Database connection failed at startup: {e}")
        # Don't crash the app, just log the error
        pass
