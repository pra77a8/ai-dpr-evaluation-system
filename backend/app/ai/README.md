# AI/NLP + Analytics Layer for AI-Powered DPR Evaluation System

This module enhances the basic backend with advanced AI/NLP capabilities for comprehensive DPR analysis.

## 🧠 Key Components

### 1. Dataset Design
- **Synthetic Data Generation**: Creates realistic training data for AI models
- **Feature Engineering**: Extracts numerical features for ML model training
- **Risk Labeling**: Assigns risk categories for supervised learning

### 2. NLP Entity Extraction
- **Custom Pattern Matching**: Extracts DPR-specific entities (budget, duration, etc.)
- **Enhanced Data Model**: Comprehensive extraction of all DPR elements
- **Multi-format Support**: Works with PDF, Word, and image documents

### 3. Risk Prediction
- **XGBoost Model**: Machine learning model for risk prediction
- **Multi-risk Assessment**: Predicts cost overrun, schedule delay, resource shortage, and environmental risks
- **Probability Scores**: Outputs risk scores between 0-1 for each risk category

### 4. Intelligent Recommendations
- **Data-driven Suggestions**: Generates actionable recommendations based on detected risks
- **Priority Ranking**: Classifies recommendations by urgency (High/Medium/Low)
- **Context-aware**: Tailors suggestions to specific project characteristics

### 5. Report Generation
- **Analytical Reports**: Detailed PDF reports with risk heatmaps
- **Recommendation Reports**: Clean, structured reports with visualizations
- **Graphical Elements**: Pie charts, bar graphs, and risk distribution visuals

### 6. AI-Powered Chatbot
- **Enhanced Prompt System**: Intelligent question classification and response generation
- **Context Understanding**: Answers complex queries about risks and recommendations
- **Natural Language Interface**: Conversational interaction with DPR analysis

## 📁 Directory Structure

```
backend/app/ai/
├── ai_service.py          # Main AI service integrating all components
├── dataset_generator.py   # Synthetic dataset generation
├── nlp_extractor.py       # NLP entity extraction using custom patterns
├── risk_predictor.py      # XGBoost risk prediction model
├── report_generator.py    # PDF report generation with visualizations
├── chatbot.py            # Enhanced chatbot with prompt engineering
├── chatbot_prompts.py    # Comprehensive prompt templates
├── test_prompts.py       # Prompt testing and demonstration
├── CHATBOT_PROMPT_GUIDE.md # Complete guide for chatbot prompts
└── __init__.py

backend/app/models/
├── ai_models.py          # AI-specific data models

backend/app/routes/
├── ai_chat.py            # AI chatbot API endpoints
```

## 🚀 API Endpoints

### Enhanced DPR Processing
```
POST /api/dpr/upload_with_ai
```
Upload DPR with full AI analysis including risk prediction and report generation.

```
POST /api/dpr/{dpr_id}/analyze_with_ai
```
Perform full AI analysis on an existing DPR.

### AI Chatbot
```
POST /api/ai/chat
```
Chat with a DPR using AI-powered natural language processing.

## 📊 Report Generation

### Analytical Report (DPR_Heatmap_Analysis.pdf)
- Risk heatmaps with color-coded sections
- Extracted insights highlighted inline
- Risk summary with scores
- Improvement recommendations
- Overall DPR quality score

### Recommendation Report (DPR_Recommendations_Report.pdf)
- Project metadata summary
- Identified risks with scores
- AI-generated recommendations
- Risk distribution pie chart
- Cost vs. timeline visualization
- Overall DPR health indicator

## 🤖 Chatbot Prompt Engineering

The chatbot uses advanced prompt engineering to provide context-aware responses. See [CHATBOT_PROMPT_GUIDE.md](CHATBOT_PROMPT_GUIDE.md) for comprehensive examples.

### Key Prompt Categories:

1. **Risk Analysis**: "What are the biggest risks?" / "Show me the risk scores"
2. **Recommendations**: "How can I improve this DPR?" / "What are your suggestions?"
3. **Financial Queries**: "Is the budget adequate?" / "What is the cost overrun risk?"
4. **Technical Assessment**: "Is the technical approach feasible?" / "What are the specifications?"
5. **Compliance Check**: "Are we following guidelines?" / "What documents are missing?"
6. **Location Analysis**: "How does location affect the project?" / "What are the geographic risks?"
7. **Project Summary**: "Give me an overview" / "What is this project about?"

### Best Practices for Chatbot Interaction:

1. **Be Specific**: Instead of "Tell me about risks," ask "What is the cost overrun risk score?"

2. **Ask Follow-up Questions**: 
   - "What is the biggest risk?"
   - "Why is that the biggest risk?"
   - "How can we mitigate that risk?"

3. **Request Actionable Insights**:
   - "What should we do about the schedule delay risk?"
   - "Give me three specific recommendations"

4. **Compare and Contrast**:
   - "How does the environmental risk compare to the resource risk?"
   - "Which recommendations have the highest priority?"

## 🔧 Setup and Initialization

1. **Install Additional Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize AI Models**:
   ```bash
   python init_ai.py
   ```

3. **Set OpenAI API Key** (for advanced chatbot):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🧪 Usage Examples

### Upload DPR with AI Analysis
```bash
curl -X POST "http://localhost:8000/api/dpr/upload_with_ai" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_dpr.pdf" \
  -F "uploaded_by=user123" \
  -F "generate_reports=true"
```

### Chat with DPR
```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the biggest risk in this DPR?",
    "dpr_id": "DPR_001"
  }'
```

## 📈 Machine Learning Model

The risk prediction model uses XGBoost with the following features:
- Contingency ratio
- Project duration in months
- Number of employees
- Number of machinery types
- Number of materials
- Compliance score
- Missing documents count

## 🔒 Security Considerations

- All API endpoints follow the existing authentication scheme
- PDF reports are generated server-side and can be secured
- Chatbot interactions are logged for audit purposes

## 🛠️ Customization

The AI layer is designed to be modular and extensible:
- Add new risk categories by extending the model
- Customize recommendation logic in the recommendation generator
- Extend NLP extraction with domain-specific entities
- Add new visualization types to report generation