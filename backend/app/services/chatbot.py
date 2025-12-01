from typing import Dict, Any, List
from bson import ObjectId
from app.database import get_dprs_collection
from app.models.ai_models import EnhancedDPRExtraction, Recommendation

def get_dpr_context(dpr_id: str) -> Dict[str, Any]:
    """
    Retrieve DPR context for the chatbot with enhanced extraction data
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        return {}
    
    # Extract enhanced extraction data if available
    enhanced_extraction = dpr.get("enhanced_extraction", {})
    if enhanced_extraction:
        # Use enhanced extraction data
        context = {
            "enhanced_extraction": enhanced_extraction,
            "risk_scores": dpr.get("risk_scores", {}),
            "recommendations": dpr.get("recommendations", [])
        }
    else:
        # Fallback to basic extraction data
        context = {
            "project_title": dpr.get("extracted_data", {}).get("project_title", ""),
            "budget": dpr.get("extracted_data", {}).get("budget", ""),
            "timeline": dpr.get("extracted_data", {}).get("timeline", ""),
            "location": dpr.get("extracted_data", {}).get("location", ""),
            "resource_allocation": dpr.get("extracted_data", {}).get("resource_allocation", ""),
            "environmental_risks": dpr.get("extracted_data", {}).get("environmental_risks", ""),
            "technical_sections": dpr.get("extracted_data", {}).get("technical_sections", [])
        }
    
    return context

def generate_response(question: str, dpr_context: Dict[str, Any]) -> str:
    """
    Generate a response based on the question and DPR context.
    Enhanced implementation with better analysis capabilities.
    """
    
    # Check if we have enhanced extraction data
    if "enhanced_extraction" in dpr_context:
        return _generate_enhanced_response(question, dpr_context)
    else:
        # Fallback to basic response generation
        return _generate_basic_response(question, dpr_context)

def _generate_enhanced_response(question: str, dpr_context: Dict[str, Any]) -> str:
    """
    Generate response using enhanced extraction data
    """
    enhanced_data = dpr_context.get("enhanced_extraction", {})
    risk_scores = dpr_context.get("risk_scores", {})
    recommendations = dpr_context.get("recommendations", [])
    
    question = question.lower()
    
    # Project Overview Prompts
    if any(keyword in question for keyword in ["summary", "overview", "about", "title", "what is this"]):
        title = enhanced_data.get("project_title", "not specified")
        department = enhanced_data.get("department", "not specified")
        duration = enhanced_data.get("duration", "not specified")
        cost = enhanced_data.get("estimated_cost", "not specified")
        
        # Calculate average risk score
        avg_risk = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0
        
        return f"Project Summary:\n- Title: {title}\n- Department: {department}\n- Duration: {duration}\n- Estimated Cost: {cost}\n- Average Risk Score: {avg_risk:.2f}\n\nThis project {'requires significant attention due to high risk levels' if avg_risk > 0.7 else 'has moderate risks that should be managed' if avg_risk > 0.4 else 'appears to be relatively low-risk'} based on the current analysis."
    
    # Risk Assessment Prompts
    elif any(keyword in question for keyword in ["risk", "danger", "threat", "hazard"]):
        if "biggest" in question or "highest" in question or "worst" in question:
            if risk_scores:
                # Find the highest risk
                max_risk = max(risk_scores.items(), key=lambda x: x[1])
                return f"The biggest risk identified is {max_risk[0]} with a risk score of {max_risk[1]:.2f}. This {'requires immediate attention' if max_risk[1] > 0.7 else 'should be monitored closely' if max_risk[1] > 0.4 else 'is relatively low but worth tracking'}."
            else:
                return "Risk assessment data is not available for this DPR."
        elif "critical" in question:
            critical_risks = {k: v for k, v in risk_scores.items() if v > 0.7}
            if critical_risks:
                risk_list = ", ".join([f"{k} ({v:.2f})" for k, v in critical_risks.items()])
                return f"Critical risks identified: {risk_list}. These risks require immediate mitigation strategies."
            else:
                return "No critical risks (score > 0.7) were identified in this DPR."
        elif "compare" in question:
            if risk_scores and len(risk_scores) >= 2:
                sorted_risks = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)
                if "cost" in question and "schedule" in question:
                    cost_risk = risk_scores.get("Cost Risk", 0)
                    schedule_risk = risk_scores.get("Schedule Risk", 0)
                    comparison = "higher" if cost_risk > schedule_risk else "lower" if cost_risk < schedule_risk else "equal to"
                    return f"The cost overrun risk ({cost_risk:.2f}) is {comparison} the schedule delay risk ({schedule_risk:.2f})."
                else:
                    top_risks = sorted_risks[:3]
                    comparison = "\n".join([f"{i+1}. {risk[0]}: {risk[1]:.2f}" for i, risk in enumerate(top_risks)])
                    return f"Risk ranking (highest to lowest):\n{comparison}"
            else:
                return "Insufficient risk data for comparison."
        elif "concern" in question or "category" in question:
            if risk_scores:
                sorted_risks = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)
                most_concerning = sorted_risks[0] if sorted_risks else ("Unknown", 0)
                return f"The most concerning risk category is {most_concerning[0]} with a score of {most_concerning[1]:.2f}."
            else:
                return "Risk assessment data is not available for this DPR."
        else:
            if risk_scores:
                risk_list = "\n".join([f"- {k}: {v:.2f}" for k, v in risk_scores.items()])
                return f"Identified risks:\n{risk_list}\n\nThese risks should be monitored throughout the project lifecycle."
            else:
                return "Risk assessment data is not available for this DPR."
    
    # Recommendations Prompts
    elif any(keyword in question for keyword in ["recommend", "suggest", "improve", "solution", "mitigation"]):
        if recommendations:
            if "top 3" in question or "three" in question:
                rec_text = "\n".join([f"{i+1}. {rec.get('description', 'N/A')} (Priority: {rec.get('priority', 'N/A')})" 
                                     for i, rec in enumerate(recommendations[:3])])
                return f"Top 3 recommendations for this project:\n{rec_text}\n\nThese recommendations address the most critical areas identified in the risk assessment."
            else:
                rec_text = "\n".join([f"{i+1}. {rec.get('description', 'N/A')} (Priority: {rec.get('priority', 'N/A')})" 
                                     for i, rec in enumerate(recommendations)])
                return f"Recommendations for this project:\n{rec_text}\n\nThese recommendations address the identified risks and should be prioritized for implementation."
        else:
            return "No specific recommendations were provided for this DPR."
    
    # Financial Analysis Prompts
    elif any(keyword in question for keyword in ["budget", "cost", "financial", "fund", "money", "rupee", "crore", "lakh"]):
        cost = enhanced_data.get("estimated_cost", "not specified")
        allocation = enhanced_data.get("fund_allocation", "not specified")
        contingency = enhanced_data.get("contingency", "not specified")
        yearly_budget = enhanced_data.get("yearly_budget", "not specified")
        
        if "adequate" in question or "sufficient" in question:
            # Simple adequacy check based on presence of data
            if cost and cost != "not specified":
                return f"The estimated cost is {cost}. Based on the available information, the budget appears to be {'adequately' if 'crore' in cost or 'lakh' in cost else 'reasonably'} allocated."
            else:
                return "Budget adequacy cannot be determined as cost information is not available."
        elif "allocation" in question:
            return f"Fund allocation details:\n- Estimated Cost: {cost}\n- Fund Allocation: {allocation}\n- Contingency: {contingency}"
        elif "yearly" in question or "breakdown" in question:
            return f"Yearly budget breakdown: {yearly_budget if yearly_budget != 'not specified' else 'Not provided in the DPR'}"
        elif "financial risk" in question:
            cost_risk = risk_scores.get("Cost Risk", 0)
            return f"Financial risk assessment: {cost_risk:.2f}. This {'indicates significant budget overrun concerns' if cost_risk > 0.7 else 'suggests moderate financial risks' if cost_risk > 0.4 else 'suggests the budget is relatively stable'}."
        else:
            return f"Financial information:\n- Estimated Cost: {cost}\n- Fund Allocation: {allocation}\n- Contingency: {contingency}"
    
    # Timeline & Scheduling Prompts
    elif any(keyword in question for keyword in ["timeline", "schedule", "duration", "milestone", "completion", "how long", "take to complete"]):
        duration = enhanced_data.get("duration", "not specified")
        start_date = enhanced_data.get("start_date", "not specified")
        end_date = enhanced_data.get("end_date", "not specified")
        milestones = enhanced_data.get("milestones", [])
        
        if "delay" in question:
            schedule_risk = risk_scores.get("Schedule Risk", 0)
            return f"Schedule delay risk assessment: {schedule_risk:.2f}. This {'suggests potential delays that require mitigation' if schedule_risk > 0.7 else 'indicates moderate scheduling concerns' if schedule_risk > 0.4 else 'suggests the timeline is relatively stable'}."
        elif "milestone" in question:
            if milestones:
                milestone_list = "\n".join([f"- {milestone}" for milestone in milestones[:5]])
                return f"Key milestones:\n{milestone_list}\n\nThese milestones should be tracked throughout the project."
            else:
                return "Milestone information is not available in this DPR."
        elif "how long" in question or "take to complete" in question:
            return f"Project duration: {duration}"
        elif "completion date" in question or "end date" in question:
            return f"Expected completion date: {end_date}"
        else:
            return f"Timeline information:\n- Duration: {duration}\n- Start Date: {start_date}\n- End Date: {end_date}"
    
    # Resource Management Prompts
    elif any(keyword in question for keyword in ["resource", "employee", "manpower", "machinery", "material", "vendor"]):
        employees = enhanced_data.get("num_employees", "not specified")
        machinery = enhanced_data.get("machinery", [])
        materials = enhanced_data.get("materials", [])
        vendor_details = enhanced_data.get("vendor_details", [])
        
        if "sufficient" in question or "shortage" in question:
            resource_risk = risk_scores.get("Resource Risk", 0)
            return f"Resource sufficiency assessment: Risk score {resource_risk:.2f}. This {'indicates potential resource shortages that require planning' if resource_risk > 0.7 else 'suggests moderate resource concerns' if resource_risk > 0.4 else 'suggests adequate resource allocation'}."
        elif "how many" in question and ("employee" in question or "manpower" in question):
            return f"Number of employees allocated to this project: {employees}"
        elif "machinery" in question:
            machinery_list = ", ".join(machinery[:5]) if machinery else "not specified"
            return f"Required machinery: {machinery_list}"
        elif "material" in question:
            materials_list = ", ".join(materials[:7]) if materials else "not specified"
            return f"Required materials: {materials_list}"
        elif "vendor" in question:
            vendor_list = ", ".join(vendor_details[:3]) if vendor_details else "not specified"
            return f"Vendor details: {vendor_list}"
        else:
            machinery_list = ", ".join(machinery[:3]) if machinery else "not specified"
            materials_list = ", ".join(materials[:5]) if materials else "not specified"
            return f"Resource information:\n- Number of Employees: {employees}\n- Key Machinery: {machinery_list}\n- Materials: {materials_list}"
    
    # Location & Environmental Prompts
    elif any(keyword in question for keyword in ["location", "region", "district", "state", "environment", "disaster", "flood", "landslide", "geographic", "where is", "area"]):
        state = enhanced_data.get("state", "not specified")
        district = enhanced_data.get("district", "not specified")
        risk_zone = enhanced_data.get("risk_zone", "not specified")
        region = enhanced_data.get("region", "not specified")
        
        if "disaster" in question or "flood" in question or "landslide" in question:
            env_risk = risk_scores.get("Environmental Risk", 0)
            return f"Natural disaster risk assessment: {env_risk:.2f}. The area is described as '{risk_zone}'. This {'requires specific mitigation planning' if env_risk > 0.7 else 'needs monitoring and preparedness measures' if env_risk > 0.4 else 'appears to have manageable environmental risks'}."
        elif "environment" in question and "risk" in question:
            env_risk = risk_scores.get("Environmental Risk", 0)
            return f"Environmental risk assessment: {env_risk:.2f}. This {'indicates significant environmental concerns' if env_risk > 0.7 else 'suggests moderate environmental risks' if env_risk > 0.4 else 'suggests the environmental impact is relatively low'}."
        elif "where" in question:
            location_parts = []
            if district != "not specified":
                location_parts.append(district)
            if state != "not specified":
                location_parts.append(state)
            if region != "not specified":
                location_parts.append(region)
            location = ", ".join(location_parts) if location_parts else "not specified"
            return f"Project location: {location}"
        else:
            return f"Location information:\n- State: {state}\n- District: {district}\n- Region: {region}\n- Risk Zone: {risk_zone}"
    
    # Technical Evaluation Prompts
    elif any(keyword in question for keyword in ["technical", "feasibility", "engineering", "specification"]):
        engineering = enhanced_data.get("engineering_details", "not specified")
        specifications = enhanced_data.get("specifications", "not specified")
        
        if "feasible" in question or "risk" in question:
            tech_risk = risk_scores.get("Technical Risk", 0)
            return f"Technical feasibility risk assessment: {tech_risk:.2f}. This {'suggests technical challenges that require expert review' if tech_risk > 0.7 else 'indicates moderate technical concerns' if tech_risk > 0.4 else 'suggests the technical approach is sound'}."
        elif "specification" in question:
            return f"Technical specifications: {specifications}"
        else:
            return f"Technical information:\n- Engineering Details: {engineering}\n- Specifications: {specifications}"
    
    # Compliance & Documentation Prompts
    elif any(keyword in question for keyword in ["compliance", "guideline", "policy", "regulation", "document"]):
        guidelines = enhanced_data.get("guidelines_followed", "not specified")
        missing_docs = enhanced_data.get("missing_documents", [])
        
        if "missing" in question:
            if missing_docs:
                doc_list = "\n".join([f"- {doc}" for doc in missing_docs[:5]])
                return f"Missing documents identified:\n{doc_list}\n\nThese documents should be prepared to ensure compliance."
            else:
                return "No missing documents were identified in this DPR."
        elif "follow" in question:
            return f"Guidelines followed: {guidelines}. Compliance status should be verified with relevant authorities."
        else:
            missing_text = ", ".join(missing_docs[:3]) if missing_docs else "None identified"
            return f"Compliance information:\n- Guidelines Followed: {guidelines}\n- Missing Documents: {missing_text}"
    
    # Comparative Analysis Prompts
    elif "compare" in question and "risk" in question:
        if risk_scores:
            sorted_risks = sorted(risk_scores.items(), key=lambda x: x[1], reverse=True)
            if "concern" in question or "category" in question:
                most_concerning = sorted_risks[0] if sorted_risks else ("Unknown", 0)
                return f"The most concerning risk category is {most_concerning[0]} with a score of {most_concerning[1]:.2f}."
            else:
                comparison = "\n".join([f"{i+1}. {risk[0]}: {risk[1]:.2f}" for i, risk in enumerate(sorted_risks[:5])])
                return f"Risk ranking (highest to lowest):\n{comparison}\n\nThis ranking helps prioritize risk mitigation efforts."
        else:
            return "Risk comparison data is not available."
    
    # Visualization Request Prompts
    elif any(keyword in question for keyword in ["chart", "graph", "visualization", "heatmap"]):
        return "Visualization features are available through the web interface. Please use the 'Generate Reports' feature on the DPR details page to create charts, graphs, and heatmaps for risk distribution and other data."
    
    # Report Generation Prompts
    elif any(keyword in question for keyword in ["report", "generate", "create", "produce"]):
        return "Report generation is available through the web interface. Please use the 'Generate Reports' feature on the DPR details page to create analytical and recommendation reports with visualizations."
    
    else:
        return "I can help you analyze various aspects of this DPR. You can ask me about:\n- Risk assessment (e.g., 'What are the biggest risks?')\n- Recommendations for improvement\n- Technical feasibility\n- Financial analysis\n- Compliance status\n- Location-specific challenges\n- Overall project summary\n\nPlease ask a specific question about the DPR, and I'll provide a detailed analysis based on the available data."

def _generate_basic_response(question: str, dpr_context: Dict[str, Any]) -> str:
    """
    Generate response using basic extraction data (fallback)
    """
    question = question.lower()
    
    if "budget" in question or "cost" in question:
        budget = dpr_context.get("budget", "not specified")
        return f"The project budget is {budget}."
    
    elif "timeline" in question or "schedule" in question or "duration" in question:
        timeline = dpr_context.get("timeline", "not specified")
        return f"The project timeline is {timeline}."
    
    elif "location" in question or "region" in question or "area" in question:
        location = dpr_context.get("location", "not specified")
        return f"The project location is {location}."
    
    elif "resource" in question or "manpower" in question:
        resource = dpr_context.get("resource_allocation", "not specified")
        return f"The resource allocation is {resource}."
    
    elif "environment" in question or "risk" in question:
        env_risks = dpr_context.get("environmental_risks", "not specified")
        return f"The environmental risks are {env_risks}."
    
    elif "title" in question or "name" in question:
        title = dpr_context.get("project_title", "not specified")
        return f"The project title is {title}."
    
    else:
        return "I don't have specific information about that. Please ask about the project budget, timeline, location, resources, or environmental risks."