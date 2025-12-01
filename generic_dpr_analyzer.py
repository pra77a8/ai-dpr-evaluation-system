"""
Generic DPR Analyzer - Works with any DPR PDF format
"""

import pdfplumber
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class DPRInfo:
    project_title: Optional[str] = None
    department: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    location: Optional[str] = None
    project_type: Optional[str] = None
    stakeholders: Optional[List[str]] = None

class GenericDPRAnalyzer:
    """
    Generic DPR Analyzer that works with various DPR formats
    """
    
    def __init__(self):
        # Common patterns for different DPR elements
        self.patterns = {
            'project_title': [
                r'(?:DETAILED PROJECT REPORT|DPR).*?For\s+([^\n]+(?:\n[^\n]+)*)',
                r'Project Title[:\-]?\s*([^\n]+)',
                r'Project Name[:\-]?\s*([^\n]+)',
                r'Title of the Project[:\-]?\s*([^\n]+)',
                r'Name of the Project[:\-]?\s*([^\n]+)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Development|Construction|Project|Scheme|Initiative)[^\n]*)',
            ],
            'department': [
                r'(?:Department|Ministry|Authority)[:\-]?\s*([^\n]+)',
                r'(Public Works|Road Construction|Water Resources|Urban Development|Rural Development)[^\n]*Department',
                r'(?:Ministry of [^\n]+)',
                r'(?:[A-Z][a-z]+ [A-Z][a-z]+) (?:Department|Ministry)',
            ],
            'budget': [
                r'(?:[₹$€£]|Rs\.?|INR)\s*([\d,]+\.?\d*)',
                r'([\d,]+\.?\d*)\s*(?:crore|lakh|million|billion)',
                r'(?:Budget|Cost|Estimated Cost|Outlay)[:\-]?\s*([^\n]+)',
            ],
            'timeline': [
                r'(\d+\s*(?:months?|years?|days?))',
                r'(?:Timeline|Duration|Period)[:\-]?\s*([^\n]+)',
                r'(?:Start|Commencement).*?(?:End|Completion)',
            ],
            'location': [
                r'(?:Location|Region|District|State)[:\-]?\s*([^\n]+)',
                r'(?:Located|Situated)\s+(?:in|at)\s+([^\n]+)',
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:District|State)',
            ],
            'project_type': [
                r'(?:Type|Category)[:\-]?\s*([^\n]+)',
                r'(?:Infrastructure|Development|Construction|Modernization|Upgrade)[^\n]*Project',
            ]
        }
        
        # Common Indian states and districts for location detection
        self.indian_states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
            "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
            "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
            "Uttar Pradesh", "Uttarakhand", "West Bengal"
        ]
        
        self.indian_districts = [
            "Guwahati", "Dispur", "Itanagar", "Kohima", "Imphal",
            "Shillong", "Aizawl", "Agartala", "Gangtok", "Chandigarh",
            "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"
        ]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def extract_dpr_info(self, pdf_path: str) -> DPRInfo:
        """Extract DPR information from PDF"""
        text = self.extract_text_from_pdf(pdf_path)
        return self._extract_from_text(text)

    def _extract_from_text(self, text: str) -> DPRInfo:
        """Extract DPR information from text"""
        info = DPRInfo()
        
        # Extract project title
        info.project_title = self._extract_project_title(text)
        
        # Extract department
        info.department = self._extract_department(text)
        
        # Extract budget
        info.budget = self._extract_budget(text)
        
        # Extract timeline
        info.timeline = self._extract_timeline(text)
        
        # Extract location
        info.location = self._extract_location(text)
        
        # Extract project type
        info.project_type = self._extract_project_type(text)
        
        # Extract stakeholders
        info.stakeholders = self._extract_stakeholders(text)
        
        return info

    def _extract_project_title(self, text: str) -> Optional[str]:
        """Extract project title using multiple strategies"""
        lines = text.split('\n')
        
        # Strategy 1: Look for common DPR title patterns
        for pattern in self.patterns['project_title']:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
                # Clean up multi-line titles
                title = re.sub(r'\s+', ' ', title)
                # Remove common prefixes
                title = re.sub(r'^(?:Project|Scheme|Title|Name)[:\-]?\s*', '', title, flags=re.IGNORECASE)
                if title and len(title) > 3:
                    return title
        
        # Strategy 2: Look for title-like patterns in first few lines
        for i, line in enumerate(lines[:20]):
            # Look for lines that look like titles (capitalized words)
            if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', line.strip()):
                # Check if it contains project-related words
                if any(word in line.lower() for word in ['project', 'scheme', 'development', 'construction']):
                    return line.strip()
        
        # Strategy 3: Look for "For" pattern (common in DPRs)
        for i, line in enumerate(lines):
            if line.strip().lower() == "for" and i + 1 < len(lines):
                # Take the next line as project title
                title = lines[i + 1].strip()
                if title and len(title) > 3:
                    # Check if there's a continuation on the next line
                    if i + 2 < len(lines) and lines[i + 2].strip() and not lines[i + 2].strip().startswith(('1.', '2.', 'Page')):
                        title += " " + lines[i + 2].strip()
                    return title
        
        # Strategy 4: First non-empty line that looks significant
        for line in lines[:10]:
            line = line.strip()
            if line and len(line) > 10 and not any(word in line.lower() for word in ['page', 'draft', 'logo']):
                # Check if it's a proper title (not just a header)
                if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', line):
                    return line
        
        return None

    def _extract_department(self, text: str) -> Optional[str]:
        """Extract department information"""
        # Look for department patterns
        for pattern in self.patterns['department']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Look for Indian government departments
        departments = [
            "Public Works Department", "Road Construction Department",
            "Water Resources Department", "Urban Development Department",
            "Rural Development Department", "Ministry of Parliamentary Affairs",
            "Department of Information Technology"
        ]
        
        for dept in departments:
            if dept.lower() in text.lower():
                return dept
        
        return None

    def _extract_budget(self, text: str) -> Optional[str]:
        """Extract budget information"""
        # Look for budget patterns
        for pattern in self.patterns['budget']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()  # Return the full match
        
        return None

    def _extract_timeline(self, text: str) -> Optional[str]:
        """Extract timeline information"""
        # Look for timeline patterns
        for pattern in self.patterns['timeline']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location information"""
        # Look for location patterns
        for pattern in self.patterns['location']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Look for Indian states and districts
        for state in self.indian_states:
            if state.lower() in text.lower():
                return state
        
        for district in self.indian_districts:
            if district.lower() in text.lower():
                return district
        
        return None

    def _extract_project_type(self, text: str) -> Optional[str]:
        """Extract project type information"""
        # Look for project type patterns
        for pattern in self.patterns['project_type']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

    def _extract_stakeholders(self, text: str) -> List[str]:
        """Extract stakeholder information"""
        stakeholders = []
        
        # Look for common stakeholder patterns
        stakeholder_patterns = [
            r'(?:Stakeholders?|Parties)[:\-]?\s*([^\n.]+)',
            r'(?:Government|Department|Ministry|Authority|Agency)[^\n]*',
        ]
        
        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            stakeholders.extend(matches)
        
        return stakeholders if stakeholders else None

def test_generic_analyzer():
    """Test the generic analyzer with the sample PDF"""
    analyzer = GenericDPRAnalyzer()
    
    print("=== Testing Generic DPR Analyzer ===")
    
    try:
        info = analyzer.extract_dpr_info("Model_DPR_Final 2.0.pdf")
        
        print(f"Project Title: {info.project_title}")
        print(f"Department: {info.department}")
        print(f"Budget: {info.budget}")
        print(f"Timeline: {info.timeline}")
        print(f"Location: {info.location}")
        print(f"Project Type: {info.project_type}")
        print(f"Stakeholders: {info.stakeholders}")
        
        # Show first part of the text for debugging
        text = analyzer.extract_text_from_pdf("Model_DPR_Final 2.0.pdf")
        lines = text.split('\n')
        print("\nFirst 10 lines of PDF:")
        for i, line in enumerate(lines[:10]):
            print(f"{i+1:2d}: {line}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_generic_analyzer()