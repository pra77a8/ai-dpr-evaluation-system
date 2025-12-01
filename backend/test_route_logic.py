"""
Test the exact logic used in the DPR route
"""
import asyncio
from app.utils.dpr_processor import extract_text_from_pdf, extract_dpr_elements

async def test_route_logic():
    """Test the exact logic used in the DPR route"""
    # Read the test PDF
    with open("test_dpr_document.pdf", "rb") as f:
        file_content = f.read()
    
    print("File size:", len(file_content))
    
    # Extract text based on file type (PDF)
    text = extract_text_from_pdf(file_content)
    print("\nExtracted text:")
    print(repr(text[:200]) + "...")
    
    # Extract DPR elements using existing method
    extracted_data = extract_dpr_elements(text)
    print("\nExtracted data:")
    print("Project Title:", repr(extracted_data.project_title))
    print("Budget:", repr(extracted_data.budget))
    print("Timeline:", repr(extracted_data.timeline))
    print("Resources:", repr(extracted_data.resource_allocation))
    print("Location:", repr(extracted_data.location))
    print("Environmental:", repr(extracted_data.environmental_risks))
    
    # Convert to dict (as done in the route)
    dpr_doc = {
        "file_name": "test_dpr_document.pdf",
        "file_type": "pdf",
        "uploaded_by": "test_user",
        "extracted_data": extracted_data.dict(),
    }
    
    print("\nDPR Document (extracted_data):")
    for key, value in dpr_doc["extracted_data"].items():
        print(f"  {key}: {repr(value)}")

if __name__ == "__main__":
    asyncio.run(test_route_logic())