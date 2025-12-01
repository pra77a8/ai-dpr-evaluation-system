"""
Comprehensive prompt templates for the DPR chatbot
"""

class DPRChatbotPrompts:
    """
    Collection of prompt templates for the DPR chatbot
    """
    
    # System prompt that defines the chatbot's role and capabilities
    SYSTEM_PROMPT = """
    You are an expert AI assistant specialized in analyzing Detailed Project Reports (DPRs) for infrastructure and development projects.
    
    Your expertise includes:
    1. Project Management: Understanding project timelines, budgets, resources, and milestones
    2. Risk Assessment: Identifying cost overruns, schedule delays, resource shortages, and environmental risks
    3. Financial Analysis: Evaluating budget allocations, fund distributions, and financial feasibility
    4. Technical Evaluation: Assessing engineering specifications, materials, and technical feasibility
    5. Compliance Review: Checking adherence to guidelines and identifying missing documentation
    6. Geographic Analysis: Understanding location-specific challenges and risk zones
    
    When answering questions:
    - Always base your responses on the provided DPR context
    - Be specific and cite relevant data from the DPR
    - If information is not available in the context, clearly state so
    - Provide actionable insights and recommendations when appropriate
    - Use clear, professional language suitable for project stakeholders
    - When discussing risks, include both the risk score and its implications
    - When providing recommendations, include priority levels and implementation suggestions
    
    Remember to maintain a professional, helpful tone while being thorough in your analysis.
    """
    
    # Base prompt template for general questions
    BASE_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Context:
    {context}
    
    User Question:
    {question}
    
    Please provide a comprehensive answer based on the DPR context above.
    """
    
    # Prompt for risk analysis questions
    RISK_ANALYSIS_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Risk Analysis Context:
    {context}
    
    User Question:
    {question}
    
    Provide a detailed risk analysis based on the DPR context. Include:
    1. Specific risk identification with scores
    2. Risk implications for the project
    3. Recommendations for risk mitigation
    4. Priority levels for addressing each risk
    """
    
    # Prompt for recommendation questions
    RECOMMENDATION_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Recommendations Context:
    {context}
    
    User Question:
    {question}
    
    Based on the DPR analysis, provide specific recommendations. For each recommendation, include:
    1. Clear description of the suggested improvement
    2. Priority level (High/Medium/Low)
    3. Expected impact on the project
    4. Implementation suggestions
    """
    
    # Prompt for summary questions
    SUMMARY_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Summary Context:
    {context}
    
    User Question:
    {question}
    
    Provide a comprehensive summary of the DPR. Include:
    1. Key project information (title, department, location, duration)
    2. Financial overview (estimated cost, fund allocation, contingency)
    3. Critical timeline milestones
    4. Resource allocation summary
    5. Major identified risks and their scores
    6. Key recommendations
    7. Overall project health assessment
    """
    
    # Prompt for technical feasibility questions
    TECHNICAL_FEASIBILITY_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Technical Context:
    {context}
    
    User Question:
    {question}
    
    Analyze the technical feasibility of the project. Consider:
    1. Engineering specifications and standards
    2. Materials and resources required
    3. Technical risks and challenges
    4. Alignment with industry best practices
    5. Recommendations for technical improvements
    """
    
    # Prompt for financial analysis questions
    FINANCIAL_ANALYSIS_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Financial Context:
    {context}
    
    User Question:
    {question}
    
    Conduct a detailed financial analysis. Include:
    1. Budget breakdown and allocation
    2. Cost-benefit analysis
    3. Financial risks and contingencies
    4. Funding adequacy assessment
    5. Recommendations for financial optimization
    """
    
    # Prompt for compliance questions
    COMPLIANCE_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Compliance Context:
    {context}
    
    User Question:
    {question}
    
    Evaluate the project's compliance status. Address:
    1. Adherence to DPR guidelines
    2. Missing or incomplete documentation
    3. Compliance risks and implications
    4. Recommendations for compliance improvement
    """
    
    # Prompt for location-specific questions
    LOCATION_ANALYSIS_PROMPT_TEMPLATE = """
    {system_prompt}
    
    DPR Location Context:
    {context}
    
    User Question:
    {question}
    
    Analyze location-specific factors. Consider:
    1. Geographic and environmental conditions
    2. Risk zones (flood, landslide, etc.)
    3. Infrastructure and connectivity
    4. Location-based challenges and opportunities
    5. Recommendations for location-specific improvements
    """
    
    @classmethod
    def get_prompt_template(cls, question_type: str = "general") -> str:
        """
        Get the appropriate prompt template based on question type
        """
        question_type = question_type.lower()
        
        if "risk" in question_type:
            return cls.RISK_ANALYSIS_PROMPT_TEMPLATE
        elif "recommend" in question_type:
            return cls.RECOMMENDATION_PROMPT_TEMPLATE
        elif "summary" in question_type or "overview" in question_type:
            return cls.SUMMARY_PROMPT_TEMPLATE
        elif "technical" in question_type or "feasibility" in question_type:
            return cls.TECHNICAL_FEASIBILITY_PROMPT_TEMPLATE
        elif "budget" in question_type or "cost" in question_type or "financial" in question_type:
            return cls.FINANCIAL_ANALYSIS_PROMPT_TEMPLATE
        elif "compliance" in question_type or "guideline" in question_type:
            return cls.COMPLIANCE_PROMPT_TEMPLATE
        elif "location" in question_type or "region" in question_type or "geographic" in question_type:
            return cls.LOCATION_ANALYSIS_PROMPT_TEMPLATE
        else:
            return cls.BASE_PROMPT_TEMPLATE
    
    @classmethod
    def format_context(cls, extraction_data: dict, risk_scores: dict, recommendations: list) -> str:
        """
        Format the context data for the prompt
        """
        context = "PROJECT INFORMATION:\n"
        context += f"  Title: {extraction_data.get('project_title', 'N/A')}\n"
        context += f"  Department: {extraction_data.get('department', 'N/A')}\n"
        context += f"  Region: {extraction_data.get('region', 'N/A')}\n"
        context += f"  Duration: {extraction_data.get('duration', 'N/A')}\n"
        context += f"  Location: {extraction_data.get('location', 'N/A')}\n"
        context += f"  State: {extraction_data.get('state', 'N/A')}\n"
        context += f"  District: {extraction_data.get('district', 'N/A')}\n"
        context += f"  Risk Zone: {extraction_data.get('risk_zone', 'N/A')}\n"
        context += "\n"
        
        context += "FINANCIAL DATA:\n"
        context += f"  Estimated Cost: {extraction_data.get('estimated_cost', 'N/A')}\n"
        context += f"  Fund Allocation: {extraction_data.get('fund_allocation', 'N/A')}\n"
        context += f"  Contingency: {extraction_data.get('contingency', 'N/A')}\n"
        context += f"  Yearly Budget: {extraction_data.get('yearly_budget', 'N/A')}\n"
        context += "\n"
        
        context += "TIMELINE DATA:\n"
        context += f"  Start Date: {extraction_data.get('start_date', 'N/A')}\n"
        context += f"  End Date: {extraction_data.get('end_date', 'N/A')}\n"
        context += f"  Milestones: {', '.join(extraction_data.get('milestones', []))}\n"
        context += "\n"
        
        context += "RESOURCE DATA:\n"
        context += f"  Number of Employees: {extraction_data.get('num_employees', 'N/A')}\n"
        context += f"  Machinery: {', '.join(extraction_data.get('machinery', []))}\n"
        context += f"  Raw Materials: {', '.join(extraction_data.get('raw_materials', []))}\n"
        context += f"  Vendor Details: {', '.join(extraction_data.get('vendor_details', []))}\n"
        context += "\n"
        
        context += "TECHNICAL SECTIONS:\n"
        context += f"  Engineering Details: {extraction_data.get('engineering_details', 'N/A')}\n"
        context += f"  Specifications: {extraction_data.get('specifications', 'N/A')}\n"
        context += f"  Materials: {', '.join(extraction_data.get('materials', []))}\n"
        context += "\n"
        
        context += "COMPLIANCE:\n"
        context += f"  Guidelines Followed: {extraction_data.get('guidelines_followed', 'N/A')}\n"
        context += f"  Missing Documents: {', '.join(extraction_data.get('missing_documents', []))}\n"
        context += "\n"
        
        context += "RISK ASSESSMENT:\n"
        for risk_type, score in risk_scores.items():
            context += f"  {risk_type}: {score:.2f}\n"
        context += "\n"
        
        context += "RECOMMENDATIONS:\n"
        for i, rec in enumerate(recommendations, 1):
            context += f"  {i}. {rec.description} (Priority: {rec.priority})\n"
        
        return context

# Example usage:
if __name__ == "__main__":
    # Example of how to use the prompts
    print("DPR Chatbot Prompts System")
    print("=" * 50)
    print("System Prompt:")
    print(DPRChatbotPrompts.SYSTEM_PROMPT[:200] + "...")
    print("\nAvailable Prompt Templates:")
    print("- BASE_PROMPT_TEMPLATE: General questions")
    print("- RISK_ANALYSIS_PROMPT_TEMPLATE: Risk-related questions")
    print("- RECOMMENDATION_PROMPT_TEMPLATE: Recommendation questions")
    print("- SUMMARY_PROMPT_TEMPLATE: Summary/overview questions")
    print("- TECHNICAL_FEASIBILITY_PROMPT_TEMPLATE: Technical questions")
    print("- FINANCIAL_ANALYSIS_PROMPT_TEMPLATE: Financial questions")
    print("- COMPLIANCE_PROMPT_TEMPLATE: Compliance questions")
    print("- LOCATION_ANALYSIS_PROMPT_TEMPLATE: Location-specific questions")