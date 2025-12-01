from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from app.routes import auth, dpr, risk, feedback, chat, ai_chat, reports

# Custom JSON encoder for ObjectId
from bson import json_util
import json

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

app = FastAPI(
    title="AI-Powered DPR Evaluation System",
    description="Backend API for the AI-Powered DPR Evaluation System",
    version="1.0.0"
)

# Add CORS middleware to allow React frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dpr.router, prefix="/api/dpr", tags=["DPR"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk Assessment"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(ai_chat.router, prefix="/api/ai", tags=["AI Analysis"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/")
async def root():
    return {"message": "AI-Powered DPR Evaluation System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}