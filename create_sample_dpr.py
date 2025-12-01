from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import blue, black
import os

def create_sample_dpr():
    # Create PDF document
    doc = SimpleDocTemplate("sample_dpr.pdf", pagesize=A4)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=blue,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=black,
        alignment=TA_LEFT,
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Read the content from text file
    with open("sample_dpr_content.txt", "r") as f:
        content = f.read()
    
    # Split content into sections
    sections = content.split("\n\n")
    
    # Create story (content) for PDF
    story = []
    
    # Add title
    story.append(Paragraph("DETAILED PROJECT REPORT", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Process each section
    for section in sections:
        lines = section.strip().split("\n")
        if not lines:
            continue
            
        # First line is the section heading (except for the first section which is the project title)
        if lines[0].startswith("PROJECT TITLE:"):
            # This is the main project title
            project_title = lines[0].replace("PROJECT TITLE:", "").strip()
            story.append(Paragraph(f"Project: {project_title}", heading_style))
        else:
            # Regular section heading
            story.append(Paragraph(lines[0], heading_style))
        
        # Add the rest of the content
        for line in lines[1:]:
            if line.strip():
                story.append(Paragraph(line, normal_style))
        
        # Add space after each section
        story.append(Spacer(1, 0.1*inch))
    
    # Add some additional formatting
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared by: Civil Engineering Department", normal_style))
    story.append(Paragraph("Date: October 6, 2025", normal_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Approved by: District Collector", normal_style))
    story.append(Paragraph("Approval Date: December 15, 2024", normal_style))
    
    # Build PDF
    doc.build(story)
    print("Sample DPR PDF created successfully as 'sample_dpr.pdf'")

if __name__ == "__main__":
    create_sample_dpr()