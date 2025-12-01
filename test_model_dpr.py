import pdfplumber
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

# Extract text from Model DPR
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()

# Initialize the extractor
extractor = NLPExtractor()

# Extract entities
extraction = extractor.extract_entities(text)

# Display key extracted information
print("=== Model DPR Final 2.0 ===")
print(f"Project Title: {extraction.project_title}")
print(f"Department: {extraction.department}")
print(f"Estimated Cost: {extraction.estimated_cost}")
print(f"Duration: {extraction.duration}")
print(f"State: {extraction.state}")
print(f"District: {extraction.district}")
print(f"Risk Zone: {extraction.risk_zone}")