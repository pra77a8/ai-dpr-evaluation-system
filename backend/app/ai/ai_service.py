import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import Dict, List, Tuple

from app.ai.dataset_generator import DatasetGenerator
from app.ai.nlp_extractor import NLPExtractor
from app.ai.risk_predictor import RiskPredictor
from app.ai.report_generator import ReportGenerator
from app.ai.chatbot import DPRChatbot
from app.models.ai_models import EnhancedDPRExtraction, Recommendation

from app.ai.specialized_dpr_extractor import SpecializedDPRExtractor


class AIService:
    """
    Main AI service that integrates all AI/NLP components
    """
    
    def __init__(self):
        self.dataset_generator = DatasetGenerator()
        self.nlp_extractor = NLPExtractor()
        self.risk_predictor = RiskPredictor()
        self.report_generator = ReportGenerator()
        self.chatbot = DPRChatbot()
        # Add the specialized extractor
        self.specialized_extractor = SpecializedDPRExtractor()
    
    def generate_training_dataset(self, size: int = 1000, filename: str = "dpr_training_dataset.csv") -> str:
        """
        Generate synthetic training dataset
        """
        print(f"Generating training dataset with {size} samples...")
        dataset = self.dataset_generator.generate_dataset(size)
        self.dataset_generator.save_dataset_to_csv(dataset, filename)
        print(f"Dataset saved to {filename}")
        return filename
    
    def extract_dpr_entities(self, text: str) -> EnhancedDPRExtraction:
        """
        Extract entities from DPR text using NLP
        Now uses specialized extraction for problematic formats
        """
        print("Extracting entities from DPR text...")
        # Use the specialized extractor which handles both generic and special cases
        extraction = self.specialized_extractor.extract_entities(text)
        print("Entity extraction completed.")
        return extraction
    
    def predict_dpr_risks(self, extraction: EnhancedDPRExtraction) -> Dict[str, float]:
        """
        Predict risks for a DPR using ML model
        """
        print("Predicting DPR risks...")
        # Extract features for risk prediction
        features = {
            'contingency_ratio': self._calculate_contingency_ratio(extraction),
            'duration_months': self._extract_duration_months(extraction),
            'num_employees': extraction.num_employees or 50,
            'num_machinery': len(extraction.machinery) if extraction.machinery else 3,
            'num_materials': len(extraction.raw_materials) if extraction.raw_materials else 5,
            'compliance_score': 1 if extraction.guidelines_followed else 0,
            'missing_docs_count': len(extraction.missing_documents) if extraction.missing_documents else 0
        }
        
        # Predict risks using trained models
        risk_scores = self.risk_predictor.predict_risks(features)
        print("Risk prediction completed.")
        return risk_scores
    
    def calculate_completeness_score(self, extraction: EnhancedDPRExtraction) -> float:
        """
        Calculate completeness score based on presence of key sections
        """
        print("Calculating completeness score...")
        
        # Define key sections that should be present in a complete DPR
        key_sections = [
            'project_title',
            'department',
            'estimated_cost',
            'duration',
            'state',
            'district',
            'num_employees',
            'milestones',
            'guidelines_followed'
        ]
        
        # Count how many key sections are present
        present_sections = 0
        for section in key_sections:
            value = getattr(extraction, section, None)
            if value is not None and value != "" and (not isinstance(value, list) or len(value) > 0):
                present_sections += 1
        
        # Calculate completeness score (0-100)
        completeness_score = (present_sections / len(key_sections)) * 100
        print(f"Completeness score: {completeness_score:.2f}%")
        return completeness_score
    
    def generate_recommendations(self, risk_scores: Dict[str, float], completeness_score: float = 100.0) -> List[Recommendation]:
        """
        Generate recommendations based on risk scores and completeness
        """
        print("Generating recommendations...")
        recommendations = []
        
        # Generate recommendations based on risk scores
        for risk_type, score in risk_scores.items():
            if score > 0.7:  # High risk
                if "cost" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Budget Rebalance",
                        description="Increase contingency budget by 10-15%",
                        priority="High"
                    ))
                elif "schedule" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Timeline Adjustment",
                        description="Timeline too short — extend by 3-6 months",
                        priority="High"
                    ))
                elif "resource" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Resource Planning",
                        description="Add alternate supplier for raw material shortage",
                        priority="High"
                    ))
                elif "environmental" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Risk Mitigation",
                        description="Area prone to flood/landslide — require mitigation planning",
                        priority="High"
                    ))
            elif score > 0.4:  # Medium risk
                if "cost" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Budget Review",
                        description="Review budget allocation for potential optimization",
                        priority="Medium"
                    ))
                elif "schedule" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Timeline Review",
                        description="Consider adding buffer time to critical milestones",
                        priority="Medium"
                    ))
                elif "resource" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Resource Optimization",
                        description="Optimize resource allocation to improve efficiency",
                        priority="Medium"
                    ))
                elif "environmental" in risk_type.lower():
                    recommendations.append(Recommendation(
                        improvement_type="Environmental Planning",
                        description="Enhance environmental safeguards and monitoring",
                        priority="Medium"
                    ))
        
        # Add recommendations based on completeness score
        if completeness_score < 30:
            recommendations.append(Recommendation(
                improvement_type="DPR Enhancement",
                description="DPR is significantly incomplete. Add missing sections for better analysis.",
                priority="High"
            ))
        elif completeness_score < 60:
            recommendations.append(Recommendation(
                improvement_type="DPR Improvement",
                description="DPR is moderately incomplete. Consider adding more details to key sections.",
                priority="Medium"
            ))
        
        # Add general recommendation if no specific risks
        if not recommendations:
            recommendations.append(Recommendation(
                improvement_type="General Improvement",
                description="Project appears well-structured with minimal risks. Continue monitoring key metrics.",
                priority="Low"
            ))
        
        print(f"Generated {len(recommendations)} recommendations.")
        return recommendations
    
    def generate_analytical_report(self, 
                                 dpr_id: str,
                                 extraction: EnhancedDPRExtraction,
                                 risk_scores: Dict[str, float],
                                 recommendations: List[Recommendation]) -> str:
        """
        Generate analytical report with heatmaps
        """
        print("Generating analytical report...")
        filename = self.report_generator.generate_analytical_report(
            dpr_id, extraction, risk_scores, recommendations
        )
        print(f"Analytical report saved as {filename}")
        return filename
    
    def generate_recommendation_report(self,
                                     dpr_id: str,
                                     extraction: EnhancedDPRExtraction,
                                     risk_scores: Dict[str, float],
                                     recommendations: List[Recommendation]) -> str:
        """
        Generate recommendation report
        """
        print("Generating recommendation report...")
        filename = self.report_generator.generate_recommendation_report(
            dpr_id, extraction, risk_scores, recommendations
        )
        print(f"Recommendation report saved as {filename}")
        return filename
    
    def answer_dpr_question(self, 
                           question: str,
                           extraction: EnhancedDPRExtraction,
                           risk_scores: Dict[str, float],
                           recommendations: List[Recommendation]) -> str:
        """
        Answer a question about the DPR using the enhanced chatbot
        """
        print(f"Answering question: {question}")
        
        # Create context for the chatbot
        context = self.chatbot.analyze_dpr(extraction, risk_scores, recommendations)
        
        # Answer the question using the enhanced chatbot
        answer = self.chatbot.answer_question(question, context)
        print("Question answered.")
        return answer
    
    def process_dpr_completely(self, dpr_id: str, text: str) -> Tuple[EnhancedDPRExtraction, Dict[str, float], List[Recommendation]]:
        """
        Process a DPR completely: extract entities, predict risks, generate recommendations
        """
        print(f"Processing DPR {dpr_id} completely...")
        
        # Extract entities
        extraction = self.extract_dpr_entities(text)
        
        # Predict risks
        risk_scores = self.predict_dpr_risks(extraction)
        
        # Calculate completeness score
        completeness_score = self.calculate_completeness_score(extraction)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(risk_scores, completeness_score)
        
        print(f"DPR {dpr_id} processing completed.")
        return extraction, risk_scores, recommendations
    
    def _calculate_contingency_ratio(self, extraction: EnhancedDPRExtraction) -> float:
        """
        Calculate contingency ratio for risk prediction
        """
        try:
            if extraction.contingency and extraction.estimated_cost:
                # Extract numeric values
                contingency_text = extraction.contingency.lower().replace('₹', '').replace('crore', '').replace('lakh', '').strip()
                estimated_text = extraction.estimated_cost.lower().replace('₹', '').replace('crore', '').replace('lakh', '').strip()
                
                contingency_value = float(contingency_text.split()[0]) if contingency_text.split() else 0
                estimated_value = float(estimated_text.split()[0]) if estimated_text.split() else 0
                
                return contingency_value / estimated_value if estimated_value > 0 else 0
        except:
            pass
        return 0.05  # Default 5% contingency
    
    def _extract_duration_months(self, extraction: EnhancedDPRExtraction) -> int:
        """
        Extract duration in months for risk prediction
        """
        try:
            if extraction.duration:
                duration = extraction.duration.lower()
                if "month" in duration:
                    return int(duration.replace("months", "").replace("month", "").strip())
                elif "year" in duration:
                    years = int(duration.replace("years", "").replace("year", "").strip())
                    return years * 12
        except:
            pass
        return 12  # Default 12 months

# Example usage
if __name__ == "__main__":
    # Initialize AI service
    ai_service = AIService()
    
    # Example DPR text (in practice, this would come from uploaded documents)
    example_text = """
    Project Title: Road Construction in Assam
    Department: Public Works Department
    Region: Northeast India
    Duration: 18 months
    Estimated Cost: ₹150 crore
    Fund Allocation: ₹140 crore
    Contingency: ₹10 crore
    Start Date: 01/06/2024
    End Date: 01/12/2025
    Number of Employees: 150
    State: Assam
    District: Guwahati
    Risk Zone: Flood prone area
    Engineering Details: Standard road construction specifications
    Guidelines Followed: Yes
    """
    
    # Process DPR completely
    # extraction, risk_scores, recommendations = ai_service.process_dpr_completely("DPR_001", example_text)
    
    # Answer a question
    # question = "What is the biggest risk in this DPR?"
    # answer = ai_service.answer_dpr_question(question, extraction, risk_scores, recommendations)
    # print(f"Question: {question}")
    # print(f"Answer: {answer}")