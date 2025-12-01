# AI-Powered DPR Evaluation System - AI Enhancements

This document describes the AI enhancements made to the DPR Evaluation System to make it more intelligent and capable of:

1. Extracting key project information from uploaded DPR PDFs using NLP and OCR
2. Predicting project risks intelligently using trained models
3. Answering user queries contextually using the uploaded DPR data and dataset
4. Generating visual analytics and detailed reports based on AI evaluation

## Enhanced Features

### 1. Intelligent Risk Prediction

The system now uses trained machine learning models (XGBoost and Random Forest) to predict project risks based on extracted DPR data.

**Risk Types Predicted:**
- Cost Overruns
- Schedule Delays
- Resource Shortages
- Environmental Risks

**Features Used for Prediction:**
- Contingency ratio
- Duration in months
- Number of employees
- Number of machinery types
- Number of materials
- Compliance score
- Missing documents count

### 2. Completeness Scoring

The system calculates a completeness score (0-100%) based on the presence of key DPR sections:
- Project title
- Department
- Estimated cost
- Duration
- State
- District
- Number of employees
- Milestones
- Guidelines followed

### 3. Enhanced NLP Extraction

Improved entity extraction with template-specific patterns for common DPR formats:
- Sample DPR format
- Model DPR Final 2.0 format
- Bridges DPR template

### 4. Contextual Chatbot

An intelligent chatbot that answers user questions based on the extracted DPR data and AI analysis.

### 5. Automated Report Generation

The system generates two types of reports:
- Analytical reports with risk charts and heatmaps
- Recommendation reports with AI-generated suggestions

## Model Training

### Training Script

A dedicated training script (`train_risk_model.py`) is provided to train the risk prediction models using the existing dataset.

**Usage:**
```bash
cd backend
python train_risk_model.py
```

### Models Directory

Trained models are saved in the `models/` directory:
- XGBoost models: `models/xgboost_{risk_type}_model.pkl`
- Random Forest models: `models/randomforest_{risk_type}_model.pkl`

## API Endpoints

### DPR Analysis
- `POST /api/dpr/upload_with_ai` - Upload DPR with full AI analysis
- `POST /api/dpr/{dpr_id}/analyze_with_ai` - Perform full AI analysis on existing DPR
- `GET /api/dpr/{dpr_id}/completeness` - Get completeness score for a DPR

### Risk Assessment
- `POST /api/risk/assess_with_ai/{dpr_id}` - Perform AI-powered risk assessment
- `GET /api/risk/visualize/{dpr_id}` - Get risk data for visualization

### Chatbot
- `POST /api/ai/chat` - Chat with DPR using AI-powered chatbot
- `POST /api/ai/chat_advanced` - Advanced chat with DPR using full AI analysis

### Reports
- `POST /api/reports/generate` - Generate AI-powered reports
- `GET /api/reports/download/{report_filename}` - Download generated reports

## Requirements

The enhanced system requires additional AI/ML libraries specified in `requirements_ai.txt`:

```
torch==2.1.0
transformers==4.35.0
sentence-transformers==2.2.2
faiss-cpu==1.7.4
langchain==0.0.350
openai==1.3.7
tiktoken==0.5.2
PyMuPDF==1.23.5
```

## Usage Examples

### 1. Uploading a DPR with AI Analysis

```bash
curl -X POST "http://localhost:8000/api/dpr/upload_with_ai" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_dpr.pdf" \
  -F "uploaded_by=user123" \
  -F "generate_reports=true"
```

### 2. Getting Risk Assessment

```bash
curl -X POST "http://localhost:8000/api/risk/assess_with_ai/{dpr_id}"
```

### 3. Chatting with the AI

```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the biggest risk in this DPR?", "dpr_id": "{dpr_id}"}'
```

### 4. Generating Reports

```bash
curl -X POST "http://localhost:8000/api/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{"dpr_id": "{dpr_id}", "report_type": "analytical"}'
```

## Model Performance

The trained models show the following performance metrics:

### XGBoost Models:
- Cost Overruns: RMSE 0.2674, R2 0.1889
- Schedule Delays: RMSE 0.1782, R2 -0.0079
- Resource Shortages: RMSE 0.1646, R2 0.0537
- Environmental Risks: RMSE 0.3059, R2 0.1134

### Random Forest Models:
- Cost Overruns: RMSE 0.2569, R2 0.2511
- Schedule Delays: RMSE 0.1697, R2 0.0860
- Resource Shortages: RMSE 0.1586, R2 0.1210
- Environmental Risks: RMSE 0.2904, R2 0.2009

## Future Improvements

1. **Dataset Enhancement**: Collect real DPR risk data to improve model accuracy
2. **Model Tuning**: Fine-tune hyperparameters for better performance
3. **Advanced NLP**: Implement transformer-based models for better entity extraction
4. **Real-time Learning**: Implement continuous learning from user feedback
5. **Multi-language Support**: Add support for regional languages in DPRs

## Testing

A test script (`test_ai_service.py`) is provided to verify the AI service functionality:

```bash
cd backend
python test_ai_service.py
```

This script tests all major AI components including entity extraction, risk prediction, completeness scoring, recommendations, and chatbot functionality.