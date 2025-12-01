# AI-Powered DPR Evaluation System - Backend

Backend API for the AI-Powered DPR Evaluation System for MDoNER.

## Features

- User authentication (signup/login)
- DPR upload and management
- Risk assessment and visualization
- Feedback system
- AI-powered analysis (new!)
- Contextual chatbot (new!)
- Automated report generation (new!)

## AI Enhancements

The system has been enhanced with intelligent AI capabilities:

1. **Intelligent Risk Prediction**: Uses trained machine learning models (XGBoost and Random Forest) to predict project risks
2. **Completeness Scoring**: Calculates a completeness score (0-100%) based on the presence of key DPR sections
3. **Enhanced NLP Extraction**: Improved entity extraction with template-specific patterns
4. **Contextual Chatbot**: Answers user questions based on the extracted DPR data and AI analysis
5. **Automated Report Generation**: Generates analytical and recommendation reports with visualizations

For detailed information about the AI enhancements, see [README_AI_ENHANCEMENTS.md](README_AI_ENHANCEMENTS.md).

## Tech Stack

- FastAPI (Python)
- MongoDB (pymongo)
- XGBoost/Scikit-learn for ML
- spaCy for NLP
- pdfplumber, python-docx, pytesseract for document processing
- matplotlib, reportlab for report generation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install AI dependencies (optional):
   ```bash
   pip install -r requirements_ai.txt
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

## Deployment

### Deploying to Railway (Recommended)

1. Create an account at [railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Set the root directory to `/backend`
5. The included `Procfile` will be automatically used
6. Add MongoDB as a database plugin in Railway
7. Set environment variables:
   - `MONGODB_URL`: Your MongoDB connection string (provided by Railway)
8. Deploy the project

### Deploying to Render

1. Create an account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the root directory to `/backend`
5. Set the build command to `pip install -r requirements.txt`
6. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `MONGODB_URL`: Your MongoDB connection string

### Deploying to Heroku

1. Create an account at [heroku.com](https://heroku.com)
2. Install the Heroku CLI
3. Create a new app: `heroku create your-app-name`
4. Set the stack to container: `heroku stack:set container`
5. Deploy: `git push heroku main`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Database

The system uses MongoDB for data storage. Make sure MongoDB is running on your system.

Environment variables:
- `MONGODB_URL`: MongoDB connection string (default: mongodb://localhost:27017)

## AI Model Training

To train the risk prediction models:

```bash
cd backend
python train_risk_model.py
```

## Testing

To test the AI service:

```bash
cd backend
python test_ai_service.py
```

## Recent Updates

- **Render Deployment Configuration**: Added [render.yaml](file://c:\Users\prani\Downloads\AI%20DPR%20Evaluation%20System\render.yaml) and updated dependencies for Render deployment (2025-10-09)