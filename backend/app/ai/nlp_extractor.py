import re
from typing import Dict, List, Optional, Tuple
import spacy
from app.models.ai_models import EnhancedDPRExtraction

class NLPExtractor:
    """
    Robust DPR Entity Extractor
    Supports template-based, regex-based, and spaCy-based extraction
    Handles missing fields gracefully
    """

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not available. Named Entity Recognition will be partial.")
            self.nlp = None

        self.patterns = {
            "BUDGET": [
                r'(?:Total Project Cost|Fund Allocation|Budget|Estimated Cost|Outlay|Project Cost|Project Tentative Outlay)[:\-]?\s*([₹Rs$€£.,\s\d]+)',
                r'[₹Rs$€£.,\s]*([\d,]+(?:\.\d+)?)',
                r'([\d,]+)\s*(?:crore|lakh|million|billion)',
            ],
            "DATE": [
                r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}',
                r'\b(?:\d{4})\b',
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{2,4}',
            ],
            "DURATION": [
                r'(?:Project Duration|Duration|Timeline)[:\-]?\s*(\d+\s*(?:months?|years?))',
                r'\d+\s*(?:months?|years?)'
            ],
            "LOCATION": [
                r'(?:State|District|Region|Location)[:\-]?\s*([^\n]+)',
                r'(?:located|situated)\s+(?:in|at)\s+([^\n]+)',
            ],
            "RISK_ZONE": [
                r'(?:flood|landslide|earthquake|disaster)\s*(?:prone|zone|area)',
            ],
            "EMPLOYEE_COUNT": [
                r'(?:No\.?|Number of)\s*(?:employees?|workers?|staff|laborers|engineers)[:\-]?\s*(\d+)',
            ],
            "MACHINERY": [
                r'(excavator|bulldozer|crane|loader|truck|mixer|roller|driller|vehicles)',
            ]
        }

    def extract_entities(self, text: str) -> EnhancedDPRExtraction:
        custom_entities = self._extract_custom_entities(text)
        spacy_entities = self._extract_spacy_entities(text)
        combined = self._combine_entities(custom_entities, spacy_entities, text)
        return EnhancedDPRExtraction(**combined)

    def _extract_custom_entities(self, text: str) -> Dict[str, List[str]]:
        entities = {}
        for key, patterns in self.patterns.items():
            entities[key] = []
            for pattern in patterns:
                try:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    entities[key].extend(matches if isinstance(matches, list) else [matches])
                except:
                    continue
        return entities

    def _extract_spacy_entities(self, text: str) -> Dict[str, List[str]]:
        entities = {"MONEY": [], "GPE": [], "ORG": [], "PERSON": [], "DATE": []}
        if not self.nlp:
            return entities
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        return entities

    def _combine_entities(self, custom: Dict[str, List[str]], spacy_ents: Dict[str, List[str]], text: str) -> Dict[str, any]:
        result = {
            "project_title": self._extract_project_title_enhanced(text),
            "department": self._extract_department_enhanced(text, spacy_ents),
            "region": self._safe_get(custom, "LOCATION", spacy_ents, fallback="GPE"),
            "duration": self._extract_duration_enhanced(text) or self._safe_get(custom, "DURATION"),
            "estimated_cost": self._extract_cost_enhanced(text) or self._safe_get(custom, "BUDGET"),
            "fund_allocation": self._safe_index(custom, "BUDGET", 1),
            "yearly_budget": self._safe_index(custom, "BUDGET", 2),
            "start_date": self._safe_index(custom, "DATE", 0) or self._safe_index(spacy_ents, "DATE", 0),
            "end_date": self._safe_index(custom, "DATE", 1) or self._safe_index(spacy_ents, "DATE", 1),
            "milestones": self._extract_milestones_enhanced(text),
            "num_employees": self._extract_employee_count_enhanced(text) or self._safe_int(custom, "EMPLOYEE_COUNT"),
            "machinery": custom.get("MACHINERY", []),
            "raw_materials": self._extract_materials_enhanced(text),
            "vendor_details": self._extract_vendors_enhanced(text, spacy_ents),
            "state": self._extract_state_enhanced(text, spacy_ents),
            "district": self._extract_district_enhanced(text, spacy_ents),
            "coordinates": self._extract_coordinates_enhanced(text),
            "risk_zone": self._safe_get(custom, "RISK_ZONE"),
            "engineering_details": self._extract_engineering_details_enhanced(text),
            "specifications": self._extract_specifications_enhanced(text),
            "guidelines_followed": self._check_guidelines_followed_enhanced(text),
            "missing_documents": self._extract_missing_documents_enhanced(text)
        }

        # Compatibility mapping
        result["budget"] = result["estimated_cost"]
        result["timeline"] = result["duration"]
        result["resource_allocation"] = str(result["num_employees"]) if result["num_employees"] else None
        result["location"] = result["district"] or result["state"] or result["region"]
        result["environmental_risks"] = result["risk_zone"]
        result["technical_sections"] = ["Introduction", "Methodology", "Implementation"]

        return result

    # ---------- SUPPORT METHODS ---------- #

    def _safe_get(self, custom: dict, key: str, spacy_ent: dict = None, fallback: str = None):
        if custom.get(key):
            return custom[key][0]
        if fallback and spacy_ent.get(fallback):
            return spacy_ent[fallback][0]
        return None

    def _safe_index(self, source: dict, key: str, idx: int):
        return source.get(key, [None])[idx] if len(source.get(key, [])) > idx else None

    def _safe_int(self, custom: dict, key: str):
        try:
            return int(custom.get(key, [None])[0])
        except:
            return None

    # ---------- SIMPLE PLACEHOLDER METHODS ---------- #
    # These methods are safely stubbed to avoid errors if missing

    def _extract_project_title_enhanced(self, text: str) -> Optional[str]:
        match = re.search(r'(?:Project Title|Name of Project)[:\-]\s*(.+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_department_enhanced(self, text: str, ents) -> Optional[str]:
        match = re.search(r'(?:Department|Ministry)[:\-]\s*([^\n]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_cost_enhanced(self, text: str) -> Optional[str]:
        match = re.search(r'(?:Estimated Cost|Project Cost)[:\-]\s*([₹$\d,\. ]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_duration_enhanced(self, text: str) -> Optional[str]:
        match = re.search(r'(?:Duration|Project Duration)[:\-]\s*([^\n]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_milestones_enhanced(self, text: str) -> List[str]:
        return re.findall(r'Milestone[:\-]\s*([^\n]+)', text, re.IGNORECASE)

    def _extract_employee_count_enhanced(self, text: str) -> Optional[int]:
        match = re.search(r'(?:Number of Employees|Manpower)[:\-]\s*(\d+)', text, re.IGNORECASE)
        return int(match.group(1)) if match else None

    def _extract_materials_enhanced(self, text: str) -> List[str]:
        return re.findall(r'(cement|steel|sand|aggregate|bitumen)', text, re.IGNORECASE)

    def _extract_vendors_enhanced(self, text: str, ents) -> List[str]:
        return ents.get("ORG", []) if ents.get("ORG") else []

    def _extract_state_enhanced(self, text: str, ents) -> Optional[str]:
        for loc in ents.get("GPE", []):
            if loc.lower() in ["maharashtra", "karnataka", "gujarat", "delhi"]:
                return loc
        return None

    def _extract_district_enhanced(self, text: str, ents) -> Optional[str]:
        match = re.search(r'District[:\-]\s*([^\n]+)', text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _extract_coordinates_enhanced(self, text: str) -> Optional[str]:
        match = re.search(r'(\d{1,2}\.\d{3,},\s*\d{1,2}\.\d{3,})', text)
        return match.group(1) if match else None

    def _extract_engineering_details_enhanced(self, text: str) -> Optional[str]:
        return "Engineering details extracted" if "foundation" in text.lower() else None

    def _extract_specifications_enhanced(self, text: str) -> Optional[List[str]]:
        return re.findall(r'Specifications?:\s*([^\n]+)', text, re.IGNORECASE)

    def _check_guidelines_followed_enhanced(self, text: str) -> Optional[str]:
        return "Yes" if "IS Code" in text or "Guidelines" in text else "No"

    def _extract_missing_documents_enhanced(self, text: str) -> List[str]:
        return ["Environmental Clearance"] if "clearance" not in text.lower() else []
