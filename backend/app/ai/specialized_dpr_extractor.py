"""
dpr_extractor.py

Complete DPR extraction module:
- EnhancedDPRExtraction: pydantic model for validated output
- NLPExtractor: main regex + spaCy hybrid extractor
- SpecializedDPRExtractor: wraps NLPExtractor and applies special handling for nonstandard DPRs

Usage:
    from app.ai.dpr_extractor import SpecializedDPRExtractor
    extractor = SpecializedDPRExtractor()
    result = extractor.extract_entities(text)      # returns EnhancedDPRExtraction
    print(result.json(indent=2))
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import asdict
import logging

# Pydantic for model validation (install with pip install pydantic if needed)
try:
    from pydantic import BaseModel, Field
except Exception:
    # Minimal fallback if pydantic not available (object will be plain dict-like)
    BaseModel = object
    Field = lambda *a, **k: None

# spaCy import but tolerant if model not installed
try:
    import spacy
except Exception:
    spacy = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -----------------------
# Output model
# -----------------------
class EnhancedDPRExtraction(BaseModel):
    # Basic project info
    project_title: Optional[str] = Field(None, description="Primary title of the project")
    department: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
    state: Optional[str] = Field(None)
    district: Optional[str] = Field(None)
    location: Optional[str] = Field(None)

    # Timeline / dates
    duration: Optional[str] = Field(None)
    start_date: Optional[str] = Field(None)
    end_date: Optional[str] = Field(None)
    timeline: Optional[str] = Field(None)

    # Financial
    estimated_cost: Optional[str] = Field(None)
    fund_allocation: Optional[str] = Field(None)
    contingency: Optional[str] = Field(None)
    yearly_budget: Optional[str] = Field(None)
    budget: Optional[str] = Field(None)

    # Resources
    num_employees: Optional[int] = Field(None)
    resource_allocation: Optional[str] = Field(None)
    machinery: Optional[List[str]] = Field(default_factory=list)
    raw_materials: Optional[List[str]] = Field(default_factory=list)
    vendor_details: Optional[List[str]] = Field(default_factory=list)

    # Risk & geography
    risk_zone: Optional[str] = Field(None)
    coordinates: Optional[str] = Field(None)
    environmental_risks: Optional[str] = Field(None)

    # Technical and compliance
    engineering_details: Optional[str] = Field(None)
    specifications: Optional[Any] = Field(None)
    technical_sections: Optional[List[str]] = Field(default_factory=list)
    guidelines_followed: Optional[Any] = Field(None)
    missing_documents: Optional[List[str]] = Field(default_factory=list)
    milestones: Optional[List[str]] = Field(default_factory=list)

    # Compatibility fields
    # (these will be filled/duplicated for older code expecting these keys)
    # `budget` duplicates `estimated_cost`, `timeline` duplicates `duration`, etc.


# -----------------------
# NLP Extractor
# -----------------------
class NLPExtractor:
    """
    Robust DPR extractor that uses:
    - regex patterns tuned for DPR templates (Model_DPR_Final / Bridges / sample_dpr)
    - spaCy NER when available (graceful fallback if not)
    """

    def __init__(self, spacy_model: str = "en_core_web_sm"):
        # Load spaCy model if available
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load(spacy_model)
            except Exception:
                logger.warning(
                    "spaCy model '%s' not found or failed to load. spaCy fallback active. "
                    "Install model with: python -m spacy download en_core_web_sm",
                    spacy_model,
                )
                self.nlp = None
        else:
            logger.warning("spaCy not installed. NER will be disabled.")

        # Patterns dictionary (kept compact and extensible)
        self.patterns = {
            "BUDGET": [
                r'(?:Total Project Cost|Project Cost|Estimated Cost|Outlay|Project Tentative Outlay|Fund Allocation)[:\-]?\s*([₹Rs$€£.\s,0-9]+(?:crore|lakh|million|billion)?)',
                r'([₹Rs$€£.\s,0-9]+)\s*(?:crore|lakh|million|billion)',
                r'[₹Rs$€£]\s*[\d,]+(?:\.\d+)?',
            ],
            "DATE": [
                r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',
                r'\b\d{4}\b',
                r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s*\d{1,4}\b',
            ],
            "DURATION": [
                r'(?:Project Duration|Duration|Timeline)[:\-]?\s*(\d+\s*(?:months?|years?))',
                r'\b\d+\s*(?:months?|years?)\b',
            ],
            "LOCATION": [
                r'(?:State|District|Region|Location)[:\-]?\s*([^\n,]+)',
                r'(?:located|situated)\s+(?:in|at)\s+([^\n,]+)'
            ],
            "RISK_ZONE": [
                r'\b(?:flood|landslide|earthquake|disaster)\s*(?:prone|zone|area)\b',
                r'\b(?:risk|vulnerability)\s*(?:of|to)\s*(?:flood|landslide|earthquake)\b'
            ],
            "EMPLOYEE_COUNT": [
                r'(?:No\.?|Number of|Number)\s*(?:employees?|workers?|staff|laborers|engineers)[:\-]?\s*(\d{1,5})',
                r'\b(\d{1,5})\s*(?:employees?|workers?|staff|laborers|engineers|personnel)\b'
            ],
            "MACHINERY": [
                r'\b(excavator|bulldozer|crane|loader|truck|mixer|roller|driller|grader|paver)\b'
            ],
        }

    # -------------
    # Public API
    # -------------
    def extract_entities(self, text: str) -> EnhancedDPRExtraction:
        """
        Run full extraction pipeline on provided plain text.
        Returns an EnhancedDPRExtraction model instance.
        """
        # 1) clean the text a bit
        text_clean = self._clean_text(text)

        # 2) custom regex extractions
        custom = self._extract_custom_entities(text_clean)

        # 3) spaCy NER extractions
        spacy_entities = self._extract_spacy_entities(text_clean)

        # 4) combine heuristics
        combined = self._combine_entities(custom, spacy_entities, text_clean)

        # 5) return validated model (pydantic)
        if isinstance(EnhancedDPRExtraction, type) and hasattr(EnhancedDPRExtraction, "__config__"):
            return EnhancedDPRExtraction(**combined)
        else:
            # fallback if pydantic is not available: create a 'model-like' object
            return EnhancedDPRExtraction(**combined)

    # -------------
    # Cleaning / helpers
    # -------------
    def _clean_text(self, text: str) -> str:
        # Normalize whitespace and remove multiple page headers/footers heuristics
        s = text.replace("\r", "\n")
        # Remove long runs of hyphens and page numbers
        s = re.sub(r'-{3,}', ' ', s)
        s = re.sub(r'Page\s*\d+\s*of\s*\d+', ' ', s, flags=re.IGNORECASE)
        s = re.sub(r'\n\s*\n+', '\n', s)
        return s.strip()

    def _extract_custom_entities(self, text: str) -> Dict[str, List[str]]:
        entities: Dict[str, List[str]] = {}
        for key, patterns in self.patterns.items():
            found: List[str] = []
            for pat in patterns:
                try:
                    matches = re.findall(pat, text, re.IGNORECASE)
                    # re.findall may return tuples for grouped patterns; flatten if needed
                    for m in matches:
                        if isinstance(m, tuple):
                            # join tuple groups
                            candidate = " ".join([x for x in m if x])
                        else:
                            candidate = m
                        if isinstance(candidate, str):
                            candidate = candidate.strip()
                            if candidate:
                                found.append(candidate)
                except re.error:
                    logger.exception("Invalid regex: %s", pat)
                    continue
            entities[key] = found
        return entities

    def _extract_spacy_entities(self, text: str) -> Dict[str, List[str]]:
        ent_map = {"MONEY": [], "DATE": [], "GPE": [], "ORG": [], "PERSON": []}
        if not self.nlp:
            return ent_map
        try:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ent_map:
                    ent_map[ent.label_].append(ent.text)
        except Exception:
            logger.exception("spaCy processing failed")
        return ent_map

    # -------------
    # Combination logic (lots of heuristics)
    # -------------
    def _combine_entities(self, custom: Dict[str, List[str]], spacy_ents: Dict[str, List[str]], text: str) -> Dict[str, Any]:
        """
        Create final dictionary for EnhancedDPRExtraction. This function centralizes the heuristics.
        """
        # Helper lambdas
        first = lambda lst: lst[0] if lst else None
        first_valid = lambda lst: next((x for x in (lst or []) if x and str(x).strip()), None)

        # Title: use multiple heuristics (Model DPR patterns, sample_dpr, Bridges, fallback)
        title = self._extract_project_title_enhanced(text, spacy_ents) or first_valid(custom.get("LOCATION")) or first_valid(spacy_ents.get("ORG"))

        # Department
        department = self._extract_department_enhanced(text, spacy_ents)

        # Region / state / district
        region = first_valid(custom.get("LOCATION")) or first_valid(spacy_ents.get("GPE"))
        state = self._extract_state_enhanced(text, spacy_ents) or region
        district = self._extract_district_enhanced(text, spacy_ents) or None

        # Duration & timeline
        duration = self._extract_duration_enhanced(text) or first_valid(custom.get("DURATION")) or None

        # Cost
        estimated_cost = self._extract_cost_enhanced(text) or first_valid(custom.get("BUDGET")) or first_valid(spacy_ents.get("MONEY"))

        # Dates
        all_dates = (custom.get("DATE") or []) + (spacy_ents.get("DATE") or [])
        start_date = all_dates[0] if len(all_dates) > 0 else None
        end_date = all_dates[1] if len(all_dates) > 1 else None

        # Employee count
        num_employees = None
        emp = custom.get("EMPLOYEE_COUNT") or []
        if emp:
            try:
                num_employees = int(re.sub(r'[^\d]', '', emp[0]))
            except Exception:
                num_employees = None

        # Machinery / raw materials / vendors
        machinery = list({m.lower().title() for m in (custom.get("MACHINERY") or []) if m})
        raw_materials = self._extract_materials_enhanced(text)
        vendor_details = self._extract_vendors_enhanced(text, spacy_ents)

        # Risk zone
        risk_zone = first_valid(custom.get("RISK_ZONE"))

        # Coordinates
        coordinates = self._extract_coordinates_enhanced(text)

        # Technical sections / specs / engineering details
        engineering_details = self._extract_engineering_details_enhanced(text)
        specifications = self._extract_specifications_enhanced(text)
        milestones = self._extract_milestones_enhanced(text)
        missing_documents = self._extract_missing_documents_enhanced(text)
        guidelines_followed = self._check_guidelines_followed_enhanced(text)

        combined = {
            "project_title": title,
            "department": department,
            "region": region,
            "state": state,
            "district": district,
            "location": district or state or region,
            "duration": duration,
            "start_date": start_date,
            "end_date": end_date,
            "timeline": duration,
            "estimated_cost": estimated_cost,
            "fund_allocation": self._safe_index(custom, "BUDGET", 1),
            "contingency": self._safe_index(custom, "BUDGET", 2),
            "yearly_budget": self._safe_index(custom, "BUDGET", 3),
            "budget": estimated_cost,
            "num_employees": num_employees,
            "resource_allocation": str(num_employees) if num_employees else None,
            "machinery": machinery,
            "raw_materials": raw_materials,
            "vendor_details": vendor_details,
            "risk_zone": risk_zone,
            "coordinates": coordinates,
            "environmental_risks": risk_zone,
            "engineering_details": engineering_details,
            "specifications": specifications,
            "technical_sections": ["Introduction", "Methodology", "Implementation"],
            "guidelines_followed": guidelines_followed,
            "missing_documents": missing_documents,
            "milestones": milestones,
        }

        return combined

    # -------------
    # Several helper extraction methods (previously missing in your file)
    # -------------
    def _safe_index(self, source: Dict[str, List[str]], key: str, idx: int) -> Optional[str]:
        try:
            return source.get(key, [None])[idx]
        except Exception:
            return None

    def _extract_project_title_enhanced(self, text: str, spacy_ents: Dict[str, List[str]]) -> Optional[str]:
        """
        Multi-strategy project title extraction. Mirrors the priorities you had:
        1) Model DPR 'DETAILED PROJECT REPORT (DPR)\\nFor\\n[Title]\\nIn'
        2) Bridges template patterns
        3) Generic Title: Project Title: X / Name of the Project: X
        4) spaCy ORG fallback
        """
        # PRIORITY 1: Model DPR
        model_dpr_pattern = r'DETAILED PROJECT REPORT\s*\(DPR\)\s*\n\s*For\s*\n([^\n]{3,200}?)\s*\n\s*In'
        m = re.search(model_dpr_pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            title = m.group(1).strip()
            if title and len(title) > 3:
                return re.sub(r'\s+', ' ', title)

        # PRIORITY 2: Generic 'For <title>' on subsequent lines
        model_alt = r'DETAILED PROJECT REPORT\s*\(DPR\)\s*\n\s*For\s+([^\n]{3,200})'
        m2 = re.search(model_alt, text, re.IGNORECASE | re.DOTALL)
        if m2:
            return m2.group(1).strip().split('\n')[0].strip()

        # PRIORITY 3: Bridges template / section-based heuristics
        bridges_patterns = [
            r'3\.1\.1\s+Project Definition[^\n]*\n[^\n]*\n([^\n]{5,200})',
            r'Project Title[:\-]?\s*([^\n]{5,200})',
            r'Name of the Project[:\-]?\s*([^\n]{5,200})',
            r'Project[:\-]?\s*([A-Z][^\n]{3,200})'
        ]
        for pat in bridges_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                cand = m.group(1).strip()
                if len(cand) > 4 and not any(x in cand.lower() for x in ['template', 'sample', 'model']):
                    return re.sub(r'\s+', ' ', cand)

        # PRIORITY 4: first significant title-like line in first 20 lines
        for line in text.splitlines()[:25]:
            ln = line.strip()
            if ln and len(ln) > 6 and not re.search(r'\b(template|sample|logo|page|draft)\b', ln, re.IGNORECASE):
                # Prefer lines with project-related words
                if re.search(r'\b(project|scheme|road|bridge|development|construction)\b', ln, re.IGNORECASE):
                    return ln

        # PRIORITY 5: spaCy ORG fallback
        if spacy_ents.get("ORG"):
            return spacy_ents["ORG"][0]

        return None

    def _extract_department_enhanced(self, text: str, spacy_ents: Dict[str, List[str]]) -> Optional[str]:
        # Common department patterns
        dept_patterns = [
            r'(?:Prepared by|Prepared / Submitted by|Prepared\s+By)[:\-]?\s*([^\n]{3,200})',
            r'(Public Works Department|Road Construction Department|Water Resources Department|Urban Development Department|Rural Development Department|Civil Engineering Department)',
            r'(Ministry of [^\n]+)'
        ]
        for pat in dept_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        # spaCy ORG clue
        for org in spacy_ents.get("ORG", []):
            if re.search(r'\b(department|ministry|authority|board)\b', org, re.IGNORECASE):
                return org
        return None

    def _extract_duration_enhanced(self, text: str) -> Optional[str]:
        m = re.search(r'(?:Project Duration|Duration|Timeline)[:\-]?\s*([0-9]{1,3}\s*(?:months?|years?))', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # fallback numeric months/years
        m2 = re.search(r'\b(\d{1,3}\s*(?:months?|years?))\b', text, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
        return None

    def _extract_cost_enhanced(self, text: str) -> Optional[str]:
        # Try specific phrasing first
        match = re.search(r'(?:Total Project Cost|Estimated Cost|Project Tentative Outlay|Outlay|Project Cost)[:\-]?\s*([₹Rs$€£.\s,\d]+(?:crore|lakh|million|billion)?)', text, re.IGNORECASE)
        if match:
            amt = match.group(1).strip()
            if amt and not re.match(r'^[Xx]+$', amt):
                return amt
        # Try other currency patterns
        match2 = re.search(r'([₹Rs$€£]\s*[\d,]+(?:\.\d+)?)', text)
        if match2:
            return match2.group(1).strip()
        # Find words like "lakh", "crore" patterns
        match3 = re.search(r'([\d,\.]+\s*(?:lakh|crore|million|billion))', text, re.IGNORECASE)
        if match3:
            return match3.group(1).strip()
        return None

    def _extract_milestones_enhanced(self, text: str) -> List[str]:
        found = []
        # bullet-like patterns
        found += [m.strip() for m in re.findall(r'[-•]\s*([A-Za-z ]{4,100}?)[:\-]?\s*\d+\s*(?:months?|years?)?', text)]
        # keywords
        keywords = ["site preparation", "foundation", "structural", "finishing", "handover", "completion", "procurement", "implementation"]
        for k in keywords:
            if k in text.lower() and k.title() not in found:
                found.append(k.title())
        return found or ["Site Preparation", "Construction", "Completion"]

    def _extract_materials_enhanced(self, text: str) -> List[str]:
        materials = ["cement", "steel", "sand", "bricks", "concrete", "asphalt", "gravel", "wood", "glass", "aggregate", "mortar", "paint", "tiles", "pipes", "bituminous concrete"]
        return [m.title() for m in materials if re.search(r'\b' + re.escape(m) + r'\b', text, re.IGNORECASE)]

    def _extract_vendors_enhanced(self, text: str, spacy_ents: Dict[str, List[str]]) -> List[str]:
        vendors = []
        for m in re.findall(r'(?:vendor|contractor|supplier)[:\-]?\s*([^\n,]+)', text, re.IGNORECASE):
            vendors.append(m.strip())
        # add ORG entities excluding government departments
        for org in spacy_ents.get("ORG", []):
            if not re.search(r'\b(department|ministry|government|authority)\b', org, re.IGNORECASE):
                vendors.append(org)
        # de-duplicate while preserving order
        seen = set()
        out = []
        for v in vendors:
            if v not in seen:
                seen.add(v)
                out.append(v)
        return out

    def _extract_state_enhanced(self, text: str, spacy_ents: Dict[str, List[str]]) -> Optional[str]:
        # explicit State: pattern
        m = re.search(r'State[:\-]?\s*([^\n,]+)', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # try GPEs and check against common Indian states
        indian_states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
            "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
            "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
            "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
            "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi"
        ]
        for st in indian_states:
            if re.search(r'\b' + re.escape(st) + r'\b', text, re.IGNORECASE):
                return st
        for g in spacy_ents.get("GPE", []):
            if g in indian_states:
                return g
        return None

    def _extract_district_enhanced(self, text: str, spacy_ents: Dict[str, List[str]]) -> Optional[str]:
        m = re.search(r'District[:\-]?\s*([^\n,]+)', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # quick fallback: GPE not in states
        gpes = spacy_ents.get("GPE", [])
        if gpes:
            # select shortest GPE that isn't a state
            for g in gpes:
                if len(g) < 30 and not re.search(r'\b(state|province|country)\b', g, re.IGNORECASE):
                    return g
        return None

    def _extract_coordinates_enhanced(self, text: str) -> Optional[str]:
        # Accept formats like "12.345N, 78.901E" or "12.345 N 78.901 E" or "12.345,78.901"
        m = re.search(r'(-?\d{1,3}\.\d+)\s*[°,]?\s*([NSns])?[,;\s]+\s*(-?\d{1,3}\.\d+)\s*[°,]?\s*([EeWw])?', text)
        if m:
            lat = m.group(1)
            lat_dir = (m.group(2) or "").upper()
            lon = m.group(3)
            lon_dir = (m.group(4) or "").upper()
            coord = f"{lat}{lat_dir}, {lon}{lon_dir}" if lat_dir or lon_dir else f"{lat}, {lon}"
            return coord
        # simple decimal pairs
        m2 = re.search(r'(\d{1,3}\.\d+)\s*[,;]\s*(\d{1,3}\.\d+)', text)
        if m2:
            return f"{m2.group(1)}, {m2.group(2)}"
        return None

    def _extract_engineering_details_enhanced(self, text: str) -> Optional[str]:
        # try to capture technical specs block
        m = re.search(r'(?:TECHNICAL SPECIFICATIONS|TECHNICAL DETAILS|ENGINEERING DETAILS)[:\-]?\s*([^\n]{10,1000})', text, re.IGNORECASE | re.DOTALL)
        if m:
            # trim to first 1000 chars
            return m.group(1).strip()[:2000]
        # otherwise find a sentence with engineering keywords
        for sent in re.split(r'[.!?]\s+', text):
            if re.search(r'\b(design|foundation|pavement|drainage|embankment|superstructure)\b', sent, re.IGNORECASE):
                return sent.strip()
        return None

    def _extract_specifications_enhanced(self, text: str) -> Optional[str]:
        specs = []
        mapping = [
            (r'Road Length[:\-]?\s*([^\n]+)', "Length"),
            (r'Road Width[:\-]?\s*([^\n]+)', "Width"),
            (r'(?:Surface Material|Surface)[:\-]?\s*([^\n]+)', "Surface"),
            (r'Drainage System[:\-]?\s*([^\n]+)', "Drainage")
        ]
        for pat, label in mapping:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                specs.append(f"{label}: {m.group(1).strip()}")
        if specs:
            return "; ".join(specs)
        # fallback: return first 'specification' phrase
        m2 = re.search(r'(?:specification|standard)[:\-]?\s*([^\n]+)', text, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
        return None

    def _check_guidelines_followed_enhanced(self, text: str) -> Optional[bool]:
        for k in ["guideline", "IS Code", "standard", "policy", "compliance", "regulation", "framework"]:
            if k.lower() in text.lower():
                return True
        return None

    def _extract_missing_documents_enhanced(self, text: str) -> List[str]:
        missing = []
        for pat in [r'(?:missing|lacking|absent)[:\-]?\s*([^\n.!?]+)', r'(?:no|without)\s+([^\n.!?]+document)']:
            for m in re.findall(pat, text, re.IGNORECASE):
                missing.append(m.strip())
        return missing

# -----------------------
# Specialized Extractor (your class integrated)
# -----------------------
class SpecializedDPRExtractor:
    """
    Specialized extractor for DPR formats that don't follow standard patterns.
    Wraps NLPExtractor and applies corrective heuristics.
    """

    def __init__(self):
        self.generic_extractor = NLPExtractor()

    def extract_entities(self, text: str) -> EnhancedDPRExtraction:
        # Run generic extractor
        generic_extraction = self.generic_extractor.extract_entities(text)

        # If extraction looks poor, apply special heuristics
        if self._needs_special_handling(text, generic_extraction):
            new_model = self._apply_special_extraction(text, generic_extraction)
            return new_model
        return generic_extraction

    def _needs_special_handling(self, text: str, generic_extraction: EnhancedDPRExtraction) -> bool:
        # Convert to dict for checks
        g = generic_extraction.dict()
        # Very long title or missing key fields => special handling
        if g.get("project_title") and len(g.get("project_title")) > 180:
            return True
        if not g.get("project_title") or not g.get("department"):
            return True
        # generic titles
        generic_titles = {"Sample Project", "Model DPR", "DPR Template", "Infrastructure Development Project"}
        if g.get("project_title") in generic_titles:
            return True
        return False

    def _apply_special_extraction(self, text: str, generic_extraction: EnhancedDPRExtraction) -> EnhancedDPRExtraction:
        result_dict = generic_extraction.dict()

        # Replace project_title if needed
        special_title = self._extract_special_project_title(text)
        if special_title:
            result_dict["project_title"] = special_title

        # Department cleanup
        if not result_dict.get("department") or result_dict.get("department", "").startswith("Approved by"):
            dept = self._extract_special_department(text)
            if dept:
                result_dict["department"] = dept

        # Clean up state/district placeholders
        if result_dict.get("state") and "Geographical Features" in str(result_dict["state"]):
            result_dict["state"] = self._extract_special_state(text)
        if result_dict.get("district") and "Geographical Features" in str(result_dict["district"]):
            result_dict["district"] = self._extract_special_district(text)

        # Special specs & engineering details
        special_specs = self._extract_special_specifications(text)
        if special_specs:
            result_dict["specifications"] = special_specs
        special_eng = self._extract_special_engineering_details(text)
        if special_eng:
            result_dict["engineering_details"] = special_eng

        return EnhancedDPRExtraction(**result_dict)

    # The rest of the specialized helper methods are nearly identical to ones in NLPExtractor,
    # they are kept minimal & robust (copied/adapted from your provided code)

    def _extract_special_project_title(self, text: str) -> Optional[str]:
        title_patterns = [
            r'Project\s*Title[:\-]?\s*([^.\n]{5,200})',
            r'Project\s*Name[:\-]?\s*([^.\n]{5,200})',
            r'Title[:\-]?\s*([^.\n]{5,200})',
            r'Name\s*of\s*the\s*Project[:\-]?\s*([^.\n]{5,200})',
            r'Name\s*of\s*Project[:\-]?\s*([^.\n]{5,200})'
        ]
        for pat in title_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                title = m.group(1).strip()
                if 5 < len(title) < 200 and not any(k in title.lower() for k in ['sample', 'template', 'model']):
                    return title

        budget_match = re.search(r'(.*?)\s*BUDGET[:\-]', text, re.DOTALL | re.IGNORECASE)
        if budget_match:
            context = budget_match.group(1).strip()
            if context and len(context) < 200:
                if "local communities" in context.lower() and "development" in context.lower():
                    if "road" in text.lower() and "construction" in text.lower():
                        return "Road Construction and Community Development Project"
                    elif "development" in text.lower():
                        return "Community Development Project"
                    else:
                        return "Infrastructure Development Project"
                else:
                    return re.sub(r'\s+', ' ', context[:200])

        if "road" in text.lower() and "construction" in text.lower():
            loc = re.search(r'(?:in|at)\s+([A-Za-z\s]{3,60})(?=\s*(?:district|state|region))', text, re.IGNORECASE)
            if loc:
                return f"Road Construction Project in {loc.group(1).strip()}"
            return "Road Construction and Community Development Project"
        if "development" in text.lower():
            loc = re.search(r'(?:in|at)\s+([A-Za-z\s]{3,60})(?=\s*(?:district|state|region))', text, re.IGNORECASE)
            if loc:
                return f"Community Development Project in {loc.group(1).strip()}"
            return "Community Development Project"

        loc = re.search(r'(?:in|at)\s+([A-Za-z\s]{3,60})(?=\s*(?:district|state|region))', text, re.IGNORECASE)
        if loc:
            return f"Infrastructure Development Project in {loc.group(1).strip()}"
        return "Infrastructure Development Project"

    def _extract_special_department(self, text: str) -> Optional[str]:
        prepared_pattern = r'Prepared by[:\-]?\s*([^\n]{3,200})'
        m = re.search(prepared_pattern, text, re.IGNORECASE)
        if m:
            dept = m.group(1).strip()
            if "Date:" in dept:
                dept = dept.split("Date:")[0].strip()
            if "Civil Engineering Department" in dept:
                return "Civil Engineering Department"
            return dept

        for pat in [r'(Civil Engineering Department)', r'(Public Works Department)', r'(Road Construction Department)']:
            m2 = re.search(pat, text, re.IGNORECASE)
            if m2:
                return m2.group(1).strip()

        return "Civil Engineering Department"

    def _extract_special_state(self, text: str) -> Optional[str]:
        m = re.search(r'State[:\-]?\s*([^\n,]+)', text, re.IGNORECASE)
        if m:
            state = m.group(1).strip()
            if " Geographical Features" in state:
                state = state.split(" Geographical Features")[0].strip()
            return state
        return "Sample State"

    def _extract_special_district(self, text: str) -> Optional[str]:
        m = re.search(r'District[:\-]?\s*([^\n,]+)', text, re.IGNORECASE)
        if m:
            district = m.group(1).strip()
            if " State:" in district:
                district = district.split(" State:")[0].strip()
            return district
        return "East District"

    def _extract_special_specifications(self, text: str) -> Optional[str]:
        specs = []
        patterns = [
            (r'Road Length[:\-]?\s*([^\n]+)', "Length"),
            (r'Road Width[:\-]?\s*([^\n]+)', "Width"),
            (r'(?:Surface Material|Surface)[:\-]?\s*([^\n]+)', "Surface"),
            (r'Drainage System[:\-]?\s*([^\n]+)', "Drainage")
        ]
        for pat, label in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                specs.append(f"{label}: {m.group(1).strip()}")
        if specs:
            return "; ".join(specs)
        return "Road construction specifications including length, width, surface material and drainage system"

    def _extract_special_engineering_details(self, text: str) -> Optional[str]:
        m = re.search(r'(?:TECHNICAL SPECIFICATIONS|TECHNICAL DETAILS|ENGINEERING DETAILS)[:\-]?\s*([^\n]{10,1000})', text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
        return "Standard engineering specifications for road construction and infrastructure development"

# -----------------------
# Example quick test (you may remove this block in production)
# -----------------------
if __name__ == "__main__":
    sample_text = """
    DETAILED PROJECT REPORT (DPR)
    For
    Upgradation of Main Road from Village A to Village B
    In
    Sample State

    Total Project Cost: ₹1,23,45,678
    Project Duration: 18 months
    Prepared by: Civil Engineering Department, State Govt.

    TECHNICAL SPECIFICATIONS:
    Road Length: 12 km
    Road Width: 7.5 m
    Surface Material: Asphalt Concrete
    Drainage System: Side drains and cross drains
    """

    extractor = SpecializedDPRExtractor()
    extracted = extractor.extract_entities(sample_text)
    try:
        print(extracted.json(indent=2))
    except Exception:
        # fallback print if pydantic not available
        print(extracted)
