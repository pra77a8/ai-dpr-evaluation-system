from typing import Dict, List, Any
import os
from app.models.ai_models import EnhancedDPRExtraction, Recommendation

class DPRChatbot:
    """
    Chatbot for answering DPR-related questions with enhanced contextual responses
    """
    
    def __init__(self):
        pass
    
    def analyze_dpr(self, extraction: EnhancedDPRExtraction, 
                   risk_scores: Dict[str, float],
                   recommendations: List[Recommendation]) -> str:
        """
        Create context for the chatbot from DPR analysis
        """
        # Convert extraction to dict for formatting
        extraction_dict = extraction.dict() if hasattr(extraction, 'dict') else vars(extraction)
        
        # Create a comprehensive context string
        context_lines = []
        
        # Project Information
        context_lines.append("PROJECT INFORMATION:")
        context_lines.append(f"Project Title: {extraction_dict.get('project_title', 'Not specified')}")
        context_lines.append(f"Department: {extraction_dict.get('department', 'Not specified')}")
        context_lines.append(f"State: {extraction_dict.get('state', 'Not specified')}")
        context_lines.append(f"District: {extraction_dict.get('district', 'Not specified')}")
        context_lines.append(f"Duration: {extraction_dict.get('duration', 'Not specified')}")
        context_lines.append(f"Estimated Cost: {extraction_dict.get('estimated_cost', 'Not specified')}")
        context_lines.append("")
        
        # Risk Scores
        context_lines.append("RISK ASSESSMENT:")
        for risk_type, score in risk_scores.items():
            context_lines.append(f"{risk_type}: {score:.2f}")
        context_lines.append("")
        
        # Recommendations
        context_lines.append("RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            context_lines.append(f"{i}. {rec.description} (Priority: {rec.priority})")
        context_lines.append("")
        
        # Technical Information
        context_lines.append("TECHNICAL INFORMATION:")
        context_lines.append(f"Engineering Details: {extraction_dict.get('engineering_details', 'Not specified')}")
        context_lines.append(f"Specifications: {extraction_dict.get('specifications', 'Not specified')}")
        if extraction_dict.get('milestones'):
            context_lines.append(f"Milestones: {', '.join(extraction_dict.get('milestones', []))}")
        context_lines.append("")
        
        # Resource Information
        context_lines.append("RESOURCE INFORMATION:")
        context_lines.append(f"Number of Employees: {extraction_dict.get('num_employees', 'Not specified')}")
        if extraction_dict.get('machinery'):
            context_lines.append(f"Machinery: {', '.join(extraction_dict.get('machinery', []))}")
        if extraction_dict.get('materials'):
            context_lines.append(f"Materials: {', '.join(extraction_dict.get('materials', []))}")
        context_lines.append("")
        
        # Compliance Information
        context_lines.append("COMPLIANCE INFORMATION:")
        context_lines.append(f"Guidelines Followed: {extraction_dict.get('guidelines_followed', 'Not specified')}")
        if extraction_dict.get('missing_documents'):
            context_lines.append(f"Missing Documents: {', '.join(extraction_dict.get('missing_documents', []))}")
        
        context = "\n".join(context_lines)
        return context
    
    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on DPR context with enhanced intelligence
        """
        question = question.lower().strip()
        
        # Parse context for quick access
        context_lines = context.split('\n')
        context_dict = {}
        current_section = ""
        
        for line in context_lines:
            if line.endswith(':') and line.isupper():
                current_section = line.rstrip(':')
            elif ':' in line and not line.startswith('-') and not line.startswith(' ') and not line.startswith('  '):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    context_dict[key.lower()] = value
        
        # Generate response based on question type
        if any(keyword in question for keyword in ["biggest risk", "highest risk", "worst risk", "main risk"]):
            # Extract risk scores from context
            risk_lines = [line for line in context_lines if ':' in line and any(risk_term in line.lower() for risk_term in ["cost", "schedule", "resource", "environment"])]
            max_risk = ("Unknown", 0.0)
            for line in risk_lines:
                if ':' in line:
                    parts = line.split(':')
                    if len(parts) == 2:
                        risk_type = parts[0].replace('-', '').strip()
                        try:
                            score = float(parts[1].strip())
                            if score > max_risk[1]:
                                max_risk = (risk_type, score)
                        except:
                            pass
            return f"The biggest risk identified in this DPR is {max_risk[0]} with a risk score of {max_risk[1]:.2f}. This level of risk suggests {'significant concerns that should be addressed immediately' if max_risk[1] > 0.7 else 'moderate concerns that warrant attention' if max_risk[1] > 0.4 else 'relatively low concerns but still worth monitoring'}."
        
        elif any(keyword in question for keyword in ["technical feasibility", "technical viability", "engineering feasibility"]):
            tech_details = context_dict.get('engineering details', 'Not specified')
            specs = context_dict.get('specifications', 'Not specified')
            return f"Technical feasibility analysis: {tech_details}. Specifications: {specs}. Based on the provided information, the technical approach appears {'sound' if 'standard' in tech_details.lower() else 'innovative' if 'innovative' in tech_details.lower() else 'adequate'}. However, a detailed engineering review would be necessary to fully assess technical viability."
        
        elif any(keyword in question for keyword in ["cost risk", "budget risk", "financial risk"]):
            # Look for cost-related risk
            risk_lines = [line for line in context_lines if ':' in line and ('cost' in line.lower() or 'budget' in line.lower())]
            for line in risk_lines:
                return f"Cost-related risk information: {line.strip()}. This risk level suggests {'budget overruns are highly likely and require immediate mitigation strategies' if '0.' in line and float(line.split(':')[-1].strip()) > 0.7 else 'moderate budget concerns that should be monitored' if '0.' in line and float(line.split(':')[-1].strip()) > 0.4 else 'budget risks are relatively low but should still be tracked'}."
            return "No specific cost-related risks were identified in the analysis. The budget appears to be adequately allocated based on the available information."
        
        elif any(keyword in question for keyword in ["recommendation", "suggest", "improve", "solution"]):
            # Extract recommendations
            rec_section_start = -1
            rec_section_end = -1
            for i, line in enumerate(context_lines):
                if line == "RECOMMENDATIONS:":
                    rec_section_start = i + 1
                elif line == "TECHNICAL INFORMATION:":
                    rec_section_end = i
                    break
            
            if rec_section_start != -1 and rec_section_end != -1:
                rec_lines = context_lines[rec_section_start:rec_section_end]
                rec_lines = [line for line in rec_lines if line.strip() and not line.startswith("RECOMMENDATIONS:")]
                
                if rec_lines:
                    response = "Based on the DPR analysis, here are the key recommendations:\n"
                    for i, line in enumerate(rec_lines[:3]):
                        response += f"{line.strip()}\n"
                    response += "\nThese recommendations address the most critical areas identified in the risk assessment and should be prioritized for implementation."
                    return response
            return "No specific recommendations were provided in the analysis. The DPR appears to be relatively well-structured with minimal identified risks."
        
        elif any(keyword in question for keyword in ["summary", "overview", "tell me about"]):
            title = context_dict.get('project title', 'Unknown Project')
            cost = context_dict.get('estimated cost', 'Not specified')
            duration = context_dict.get('duration', 'Not specified')
            location = f"{context_dict.get('district', '')}, {context_dict.get('state', '')}".strip(', ')
            
            # Get risk summary
            risk_lines = [line for line in context_lines if ':' in line and any(risk_term in line.lower() for risk_term in ["cost", "schedule", "resource", "environment"])]
            risk_count = len(risk_lines)
            avg_risk = sum(float(line.split(':')[-1].strip()) for line in risk_lines if ':' in line and '0.' in line.split(':')[-1]) / risk_count if risk_count > 0 else 0
            
            return f"Project Summary:\n- Title: {title}\n- Location: {location}\n- Estimated Cost: {cost}\n- Duration: {duration}\n- Number of Identified Risks: {risk_count}\n- Average Risk Score: {avg_risk:.2f}\n\nThis project {'requires significant attention due to high risk levels' if avg_risk > 0.7 else 'has moderate risks that should be managed' if avg_risk > 0.4 else 'appears to be relatively low-risk'} based on the current analysis."
        
        elif any(keyword in question for keyword in ["compliance", "guideline", "policy", "regulation"]):
            guidelines_followed = context_dict.get('guidelines followed', 'Not specified')
            missing_docs = context_dict.get('missing documents', 'None identified')
            
            if str(guidelines_followed).lower() == 'true':
                return f"The DPR indicates that guidelines have been followed. However, there are {missing_docs if missing_docs else 'no'} missing documents that should be addressed to ensure full compliance."
            else:
                return f"Compliance status: {guidelines_followed}. Missing documents: {missing_docs}. It is recommended to review all applicable DPR guidelines and ensure all required documentation is complete and submitted."
        
        elif any(keyword in question for keyword in ["location", "region", "district", "geographic", "where is"]):
            state = context_dict.get('state', 'Not specified')
            district = context_dict.get('district', 'Not specified')
            risk_zone = context_dict.get('risk zone', 'Not specified')
            
            return f"Location Analysis:\n- State: {state}\n- District: {district}\n- Risk Zone: {risk_zone}\n\nThe geographic location {'presents significant challenges that require mitigation planning' if 'flood' in risk_zone.lower() or 'landslide' in risk_zone.lower() else 'appears to be relatively stable' if 'none' in risk_zone.lower() else 'has some considerations that should be addressed'}. Infrastructure planning should account for these geographic factors."
        
        elif any(keyword in question for keyword in ["resource", "employee", "manpower", "machinery", "material"]):
            employees = context_dict.get('number of employees', 'Not specified')
            machinery = context_dict.get('machinery', 'Not specified')
            materials = context_dict.get('materials', 'Not specified')
            
            return f"Resource Information:\n- Number of Employees: {employees}\n- Machinery: {machinery}\n- Materials: {materials}\n\nThis resource allocation {'appears adequate' if 'not specified' not in [employees, machinery, materials] else 'may need further detail'} for the project scope."
        
        elif any(keyword in question for keyword in ["timeline", "schedule", "duration", "completion"]):
            duration = context_dict.get('duration', 'Not specified')
            milestones = context_dict.get('milestones', 'Not specified')
            
            return f"Timeline Information:\n- Duration: {duration}\n- Key Milestones: {milestones}\n\nThe project timeline {'appears realistic' if 'not specified' not in [duration, milestones] else 'could benefit from more detailed milestone planning'} based on the provided information."
        
        elif "completeness" in question or "complete" in question:
            # Look for completeness information in context
            completeness_info = "The completeness of this DPR cannot be determined from the provided context."
            for line in context_lines:
                if "completeness" in line.lower():
                    completeness_info = line
                    break
            return completeness_info
        
        else:
            # Default response with guidance
            return "I can help you analyze various aspects of this DPR. You can ask me about:\n- Risk assessment (e.g., 'What are the biggest risks?')\n- Recommendations for improvement\n- Technical feasibility\n- Financial analysis\n- Compliance status\n- Location-specific challenges\n- Overall project summary\n\nPlease ask a specific question about the DPR, and I'll provide a detailed analysis based on the available data."