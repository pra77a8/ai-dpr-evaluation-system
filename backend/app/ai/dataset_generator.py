import pandas as pd
import numpy as np
import random
from typing import List, Dict, Any
from app.models.ai_models import EnhancedDPRExtraction, RiskLabel, Recommendation, TrainingDataPoint

class DatasetGenerator:
    """
    Generate synthetic dataset for training AI models for DPR evaluation
    """
    
    def __init__(self):
        self.risk_types = [
            RiskLabel.COST_OVERRUN,
            RiskLabel.DELAY,
            RiskLabel.ENVIRONMENTAL,
            RiskLabel.RESOURCE,
            RiskLabel.NONE
        ]
        
        self.departments = [
            "Public Works Department",
            "Road Construction Department",
            "Water Resources Department",
            "Urban Development Department",
            "Rural Development Department"
        ]
        
        self.states = [
            "Assam", "Meghalaya", "Arunachal Pradesh", "Nagaland", "Manipur",
            "Mizoram", "Tripura", "Sikkim"
        ]
        
        self.districts = [
            "Guwahati", "Dispur", "Itanagar", "Kohima", "Imphal",
            "Shillong", "Aizawl", "Agartala", "Gangtok"
        ]
        
        self.risk_zones = ["Flood", "Landslide", "Connectivity", "None"]
        
        self.machinery_types = [
            "Excavator", "Bulldozer", "Crane", "Loader", "Dump Truck",
            "Concrete Mixer", "Road Roller", "Pile Driver"
        ]
        
        self.materials = [
            "Cement", "Steel", "Sand", "Bricks", "Concrete",
            "Asphalt", "Gravel", "Wood", "Glass"
        ]
        
        self.milestones = [
            "Site Preparation", "Foundation Work", "Structural Work",
            "Finishing Work", "Inspection", "Handover"
        ]
        
        self.missing_docs = [
            "Environmental Clearance", "Land Acquisition Papers",
            "Technical Specifications", "Budget Approval", "Timeline Chart"
        ]
        
        self.recommendation_types = [
            "Budget Rebalance", "Timeline Adjustment", "Resource Planning",
            "Risk Mitigation", "Compliance Improvement"
        ]

    def generate_synthetic_dpr(self, dpr_id: str) -> TrainingDataPoint:
        """
        Generate a synthetic DPR data point for training
        """
        # Generate random enhanced DPR extraction
        extraction = EnhancedDPRExtraction(
            project_title=f"Infrastructure Development Project {random.randint(100, 999)}",
            department=random.choice(self.departments),
            region=f"Region {random.randint(1, 10)}",
            duration=f"{random.randint(6, 36)} months",
            estimated_cost=f"₹{random.randint(50, 500)} crore",
            fund_allocation=f"₹{random.randint(40, 450)} crore",
            yearly_budget=f"₹{random.randint(10, 150)} crore",
            contingency=f"₹{random.randint(2, 20)} crore",
            start_date=f"{random.randint(1, 28)}/{random.randint(1, 12)}/202{random.randint(4, 6)}",
            end_date=f"{random.randint(1, 28)}/{random.randint(1, 12)}/202{random.randint(7, 9)}",
            milestones=random.sample(self.milestones, random.randint(2, 4)),
            num_employees=random.randint(10, 200),
            machinery=random.sample(self.machinery_types, random.randint(2, 5)),
            raw_materials=random.sample(self.materials, random.randint(3, 6)),
            vendor_details=[f"Vendor {i}" for i in range(1, random.randint(2, 5))],
            state=random.choice(self.states),
            district=random.choice(self.districts),
            coordinates=f"{random.uniform(24, 28):.4f}N, {random.uniform(92, 98):.4f}E",
            risk_zone=random.choice(self.risk_zones),
            engineering_details=f"Technical specifications for infrastructure project",
            specifications=f"Standard engineering specifications",
            materials=random.sample(self.materials, random.randint(2, 5)),
            guidelines_followed=random.choice([True, False]),
            missing_documents=random.sample(self.missing_docs, random.randint(0, 2)) if random.random() < 0.3 else []
        )
        
        # Assign risk label based on some logic
        risk_label = self._assign_risk_label(extraction)
        
        # Generate recommendation based on risk
        recommendation = self._generate_recommendation(risk_label)
        
        # Generate features for ML model
        features = self._extract_features(extraction)
        
        return TrainingDataPoint(
            dpr_id=dpr_id,
            extracted_data=extraction,
            risk_label=risk_label,
            recommendation=recommendation,
            features=features
        )
    
    def _assign_risk_label(self, extraction: EnhancedDPRExtraction) -> RiskLabel:
        """
        Assign risk label based on extraction data
        """
        # Simple rule-based risk assignment for synthetic data
        risks = []
        
        # Cost overrun risk based on contingency vs estimated cost
        if extraction.contingency and extraction.estimated_cost:
            try:
                contingency_value = float(extraction.contingency.replace("₹", "").replace("crore", "").strip())
                estimated_value = float(extraction.estimated_cost.replace("₹", "").replace("crore", "").strip())
                if contingency_value / estimated_value < 0.05:  # Less than 5% contingency
                    risks.append(RiskLabel.COST_OVERRUN)
            except:
                pass
        
        # Delay risk based on duration
        if extraction.duration:
            try:
                duration_months = int(extraction.duration.replace("months", "").strip())
                if duration_months < 12:  # Less than 12 months might be risky
                    risks.append(RiskLabel.DELAY)
            except:
                pass
        
        # Environmental risk based on risk zone
        if extraction.risk_zone and extraction.risk_zone != "None":
            risks.append(RiskLabel.ENVIRONMENTAL)
        
        # Resource risk based on employee count
        if extraction.num_employees and extraction.num_employees < 30:
            risks.append(RiskLabel.RESOURCE)
        
        # If no risks, assign NONE
        if not risks:
            return RiskLabel.NONE
        
        # Return a random risk if multiple risks
        return random.choice(risks)
    
    def _generate_recommendation(self, risk_label: RiskLabel) -> Recommendation:
        """
        Generate recommendation based on risk label
        """
        recommendations = {
            RiskLabel.COST_OVERRUN: Recommendation(
                improvement_type="Budget Rebalance",
                description="Increase contingency budget by 10%",
                priority="High"
            ),
            RiskLabel.DELAY: Recommendation(
                improvement_type="Timeline Adjustment",
                description="Timeline too short — extend by 3 months",
                priority="High"
            ),
            RiskLabel.ENVIRONMENTAL: Recommendation(
                improvement_type="Risk Mitigation",
                description=f"Area prone to {random.choice(['flood', 'landslide'])} — require mitigation planning",
                priority="High"
            ),
            RiskLabel.RESOURCE: Recommendation(
                improvement_type="Resource Planning",
                description="Add alternate supplier for raw material shortage",
                priority="Medium"
            ),
            RiskLabel.NONE: Recommendation(
                improvement_type="General Improvement",
                description="Project appears well-structured with minimal risks",
                priority="Low"
            )
        }
        
        return recommendations[risk_label]
    
    def _extract_features(self, extraction: EnhancedDPRExtraction) -> Dict[str, Any]:
        """
        Extract numerical features for ML model training
        """
        features = {}
        
        # Financial ratios
        try:
            if extraction.estimated_cost and extraction.contingency:
                est_cost = float(extraction.estimated_cost.replace("₹", "").replace("crore", "").strip())
                contingency = float(extraction.contingency.replace("₹", "").replace("crore", "").strip())
                features['contingency_ratio'] = contingency / est_cost if est_cost > 0 else 0
            else:
                features['contingency_ratio'] = 0
        except:
            features['contingency_ratio'] = 0
        
        # Duration in months
        try:
            if extraction.duration:
                features['duration_months'] = int(extraction.duration.replace("months", "").strip())
            else:
                features['duration_months'] = 12
        except:
            features['duration_months'] = 12
        
        # Employee count
        features['num_employees'] = extraction.num_employees or 50
        
        # Number of machinery types
        features['num_machinery'] = len(extraction.machinery) if extraction.machinery else 3
        
        # Number of materials
        features['num_materials'] = len(extraction.materials) if extraction.materials else 5
        
        # Compliance score (1 if guidelines followed, 0 otherwise)
        features['compliance_score'] = 1 if extraction.guidelines_followed else 0
        
        # Number of missing documents
        features['missing_docs_count'] = len(extraction.missing_documents) if extraction.missing_documents else 0
        
        return features
    
    def generate_dataset(self, size: int = 1000) -> List[TrainingDataPoint]:
        """
        Generate a dataset of specified size
        """
        dataset = []
        for i in range(size):
            dpr_id = f"DPR_{i:04d}"
            data_point = self.generate_synthetic_dpr(dpr_id)
            dataset.append(data_point)
        return dataset
    
    def save_dataset_to_csv(self, dataset: List[TrainingDataPoint], filename: str = "dpr_training_dataset.csv"):
        """
        Save dataset to CSV for training
        """
        # Convert to DataFrame
        rows = []
        for data_point in dataset:
            row = {
                "dpr_id": data_point.dpr_id,
                "project_title": data_point.extracted_data.project_title,
                "department": data_point.extracted_data.department,
                "region": data_point.extracted_data.region,
                "duration": data_point.extracted_data.duration,
                "estimated_cost": data_point.extracted_data.estimated_cost,
                "fund_allocation": data_point.extracted_data.fund_allocation,
                "contingency": data_point.extracted_data.contingency,
                "start_date": data_point.extracted_data.start_date,
                "end_date": data_point.extracted_data.end_date,
                "num_employees": data_point.extracted_data.num_employees,
                "state": data_point.extracted_data.state,
                "district": data_point.extracted_data.district,
                "risk_zone": data_point.extracted_data.risk_zone,
                "guidelines_followed": data_point.extracted_data.guidelines_followed,
                "risk_label": data_point.risk_label,
                "recommendation_type": data_point.recommendation.improvement_type,
                "recommendation_description": data_point.recommendation.description,
                "recommendation_priority": data_point.recommendation.priority
            }
            # Add features
            for key, value in data_point.features.items():
                row[key] = value
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename}")