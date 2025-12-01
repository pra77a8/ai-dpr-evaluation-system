import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    print("✓ ReportLab imported successfully")
    
    # Test basic PDF generation
    filename = "test_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("Test Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("This is a test PDF.", styles['Normal']))
    
    doc.build(story)
    print(f"✓ PDF generated successfully: {filename}")
    
    # Clean up
    if os.path.exists(filename):
        os.remove(filename)
        print("✓ Test file cleaned up")
        
except Exception as e:
    print(f"✗ Error with PDF generation: {e}")
    import traceback
    traceback.print_exc()