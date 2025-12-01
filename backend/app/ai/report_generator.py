import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io
import base64
from typing import Dict, List
from app.models.ai_models import EnhancedDPRExtraction, Recommendation

class ReportGenerator:
    """
    Generate PDF reports for DPR analysis
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            ),
            'Heading': ParagraphStyle(
                'CustomHeading',
                parent=self.styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.darkblue
            ),
            'SubHeading': ParagraphStyle(
                'CustomSubHeading',
                parent=self.styles['Heading3'],
                fontSize=14,
                spaceAfter=10,
                textColor=colors.darkgreen
            ),
            'Normal': ParagraphStyle(
                'CustomNormal',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=6
            ),
            'RiskHigh': ParagraphStyle(
                'RiskHigh',
                parent=self.styles['Normal'],
                textColor=colors.red,
                fontSize=10,
                spaceAfter=6
            ),
            'RiskMedium': ParagraphStyle(
                'RiskMedium',
                parent=self.styles['Normal'],
                textColor=colors.orange,
                fontSize=10,
                spaceAfter=6
            ),
            'RiskLow': ParagraphStyle(
                'RiskLow',
                parent=self.styles['Normal'],
                textColor=colors.green,
                fontSize=10,
                spaceAfter=6
            )
        }
    
    def generate_analytical_report(self, 
                                 dpr_id: str,
                                 extraction: EnhancedDPRExtraction,
                                 risk_scores: Dict[str, float],
                                 recommendations: List[Recommendation],
                                 filename: str = None) -> str:
        """
        Generate detailed analytical report with heatmaps and improvement highlights
        """
        if filename is None:
            filename = f"{dpr_id}_Heatmap_Analysis.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph("DPR Analytical Report", self.custom_styles['Title']))
        story.append(Spacer(1, 20))
        
        # Project Information
        story.append(Paragraph("Project Information", self.custom_styles['Heading']))
        project_data = [
            ["Project Title", extraction.project_title or "N/A"],
            ["Department", extraction.department or "N/A"],
            ["State", extraction.state or "N/A"],
            ["District", extraction.district or "N/A"],
            ["Duration", extraction.duration or "N/A"],
            ["Estimated Cost", extraction.estimated_cost or "N/A"]
        ]
        project_table = Table(project_data)
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(project_table)
        story.append(Spacer(1, 20))
        
        # Risk Scores Visualization
        story.append(Paragraph("Risk Analysis Heatmap", self.custom_styles['Heading']))
        risk_chart_buffer = self._create_risk_chart(risk_scores)
        story.append(Image(risk_chart_buffer, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
        
        # Risk Distribution Pie Chart
        story.append(Paragraph("Risk Distribution", self.custom_styles['Heading']))
        pie_chart_buffer = self._create_pie_chart(risk_scores)
        story.append(Image(pie_chart_buffer, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
        
        # Extracted Insights
        story.append(Paragraph("Extracted Insights", self.custom_styles['Heading']))
        insights_data = [
            ["Start Date", extraction.start_date or "N/A"],
            ["End Date", extraction.end_date or "N/A"],
            ["Number of Employees", str(extraction.num_employees) if extraction.num_employees else "N/A"],
            ["Risk Zone", extraction.risk_zone or "N/A"],
            ["Environmental Risks", extraction.environmental_risks or "N/A"]
        ]
        insights_table = Table(insights_data)
        insights_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(insights_table)
        story.append(Spacer(1, 20))
        
        # Risk Correlation Analysis
        story.append(Paragraph("Risk Correlation Analysis", self.custom_styles['Heading']))
        correlation_buffer = self._create_risk_correlation_chart(risk_scores, extraction)
        story.append(Image(correlation_buffer, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
        
        # Risk Summary
        story.append(Paragraph("Identified Risks Summary", self.custom_styles['Heading']))
        for risk_type, score in risk_scores.items():
            risk_level = self._get_risk_level(score)
            risk_style = self._get_risk_style(risk_level)
            story.append(Paragraph(f"{risk_type}: {score:.2f} ({risk_level})", risk_style))
        story.append(Spacer(1, 20))
        
        # Risk Trend Analysis
        story.append(Paragraph("Risk Trend Analysis", self.custom_styles['Heading']))
        story.append(Paragraph("The following analysis shows how different risk factors relate to each other and to project parameters:", self.custom_styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Risk Factor Analysis
        risk_factors = list(risk_scores.keys())
        if len(risk_factors) > 1:
            story.append(Paragraph("Key Risk Relationships:", self.custom_styles['SubHeading']))
            max_risk = max(risk_scores, key=risk_scores.get)
            min_risk = min(risk_scores, key=risk_scores.get)
            story.append(Paragraph(f"• Highest risk factor: {max_risk} ({risk_scores[max_risk]:.2f})", self.custom_styles['Normal']))
            story.append(Paragraph(f"• Lowest risk factor: {min_risk} ({risk_scores[min_risk]:.2f})", self.custom_styles['Normal']))
            
            # Risk balance analysis
            avg_risk = sum(risk_scores.values()) / len(risk_scores)
            if avg_risk > 0.7:
                story.append(Paragraph(f"• Overall risk level is HIGH (avg: {avg_risk:.2f}). Requires immediate attention.", self.custom_styles['RiskHigh']))
            elif avg_risk > 0.4:
                story.append(Paragraph(f"• Overall risk level is MODERATE (avg: {avg_risk:.2f}). Monitor closely.", self.custom_styles['RiskMedium']))
            else:
                story.append(Paragraph(f"• Overall risk level is LOW (avg: {avg_risk:.2f}). Project is relatively stable.", self.custom_styles['RiskLow']))
        story.append(Spacer(1, 20))
        
        # Data Quality Assessment
        story.append(Paragraph("Data Quality Assessment", self.custom_styles['Heading']))
        story.append(Paragraph("Analysis of the completeness and reliability of extracted data:", self.custom_styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Check for missing critical data
        missing_data = []
        if not extraction.estimated_cost:
            missing_data.append("• Estimated cost information")
        if not extraction.duration:
            missing_data.append("• Project duration information")
        if not extraction.num_employees:
            missing_data.append("• Employee/resource allocation data")
        if not extraction.start_date or not extraction.end_date:
            missing_data.append("• Complete timeline information")
        
        if missing_data:
            story.append(Paragraph("Missing Critical Information:", self.custom_styles['SubHeading']))
            for item in missing_data:
                story.append(Paragraph(item, self.custom_styles['RiskHigh']))
            story.append(Paragraph("Recommendation: Obtain missing information to improve risk analysis accuracy.", self.custom_styles['Normal']))
        else:
            story.append(Paragraph("All critical data fields are present.", self.custom_styles['RiskLow']))
        story.append(Spacer(1, 20))
        
        # Overall Quality Score
        overall_score = sum(risk_scores.values()) / len(risk_scores)
        quality = self._get_dpr_quality(overall_score)
        story.append(Paragraph(f"Overall DPR Quality Score: {overall_score:.2f} ({quality})", 
                             self.custom_styles['Heading']))
        
        # Build PDF
        doc.build(story)
        print(f"Analytical report saved to {filename}")
        return filename
    
    def generate_recommendation_report(self,
                                     dpr_id: str,
                                     extraction: EnhancedDPRExtraction,
                                     risk_scores: Dict[str, float],
                                     recommendations: List[Recommendation],
                                     filename: str = None) -> str:
        """
        Generate clean recommendation report with detailed, project-specific recommendations
        """
        if filename is None:
            filename = f"{dpr_id}_Recommendations_Report.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title
        story.append(Paragraph("DPR Recommendation Report", self.custom_styles['Title']))
        story.append(Spacer(1, 20))
        
        # Project Metadata
        story.append(Paragraph("Project Metadata", self.custom_styles['Heading']))
        metadata = [
            ["Field", "Value"],
            ["Project Title", extraction.project_title or "N/A"],
            ["Department", extraction.department or "N/A"],
            ["State", extraction.state or "N/A"],
            ["District", extraction.district or "N/A"],
            ["Duration", extraction.duration or "N/A"],
            ["Estimated Cost", extraction.estimated_cost or "N/A"]
        ]
        metadata_table = Table(metadata)
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 20))
        
        # Extracted Fields
        story.append(Paragraph("Extracted Fields", self.custom_styles['Heading']))
        fields_data = [
            ["Budget", extraction.budget or "N/A"],
            ["Timeline", extraction.timeline or "N/A"],
            ["Resource Allocation", extraction.resource_allocation or "N/A"],
            ["Location", extraction.location or "N/A"],
            ["Environmental Risks", extraction.environmental_risks or "N/A"]
        ]
        fields_table = Table(fields_data)
        fields_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(fields_table)
        story.append(Spacer(1, 20))
        
        # Identified Risks with Detailed Analysis
        story.append(Paragraph("Identified Risks with Detailed Analysis", self.custom_styles['Heading']))
        risks_analysis = []
        risks_analysis.append(["Risk Type", "Score", "Analysis"])
        
        for risk_type, score in risk_scores.items():
            analysis = self._get_risk_analysis(risk_type, score, extraction)
            risks_analysis.append([risk_type, f"{score:.2f}", analysis])
        
        risks_analysis_table = Table(risks_analysis)
        risks_analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(risks_analysis_table)
        story.append(Spacer(1, 20))
        
        # AI-generated Recommendations with Context
        story.append(Paragraph("AI-generated Recommendations", self.custom_styles['Heading']))
        rec_data = []
        rec_data.append(["#", "Recommendation", "Priority", "Context"])
        
        for i, rec in enumerate(recommendations, 1):
            context = self._get_recommendation_context(rec, risk_scores, extraction)
            rec_data.append([f"{i}", rec.description, rec.priority, context])
        
        rec_table = Table(rec_data)
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 20))
        
        # Detailed Recommendation Sections
        story.append(Paragraph("Detailed Action Plan", self.custom_styles['Heading']))
        story.append(Paragraph("Based on the identified risks, here is a comprehensive action plan:", self.custom_styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Categorized Recommendations
        high_priority_recs = [rec for rec in recommendations if rec.priority == "High"]
        medium_priority_recs = [rec for rec in recommendations if rec.priority == "Medium"]
        low_priority_recs = [rec for rec in recommendations if rec.priority == "Low"]
        
        if high_priority_recs:
            story.append(Paragraph("High Priority Actions:", self.custom_styles['SubHeading']))
            for i, rec in enumerate(high_priority_recs, 1):
                story.append(Paragraph(f"{i}. {rec.description}", self.custom_styles['RiskHigh']))
            story.append(Spacer(1, 10))
        
        if medium_priority_recs:
            story.append(Paragraph("Medium Priority Actions:", self.custom_styles['SubHeading']))
            for i, rec in enumerate(medium_priority_recs, 1):
                story.append(Paragraph(f"{i}. {rec.description}", self.custom_styles['RiskMedium']))
            story.append(Spacer(1, 10))
        
        if low_priority_recs:
            story.append(Paragraph("Low Priority Actions:", self.custom_styles['SubHeading']))
            for i, rec in enumerate(low_priority_recs, 1):
                story.append(Paragraph(f"{i}. {rec.description}", self.custom_styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Implementation Timeline
        story.append(Paragraph("Suggested Implementation Timeline", self.custom_styles['Heading']))
        timeline_data = [
            ["Phase", "Actions", "Timeline"],
            ["Immediate (0-1 month)", "Address high priority risks", "1 month"],
            ["Short-term (1-3 months)", "Implement medium priority actions", "2 months"],
            ["Medium-term (3-6 months)", "Monitor and adjust based on progress", "3 months"],
            ["Long-term (6+ months)", "Continuous improvement and optimization", "Ongoing"]
        ]
        timeline_table = Table(timeline_data)
        timeline_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(timeline_table)
        story.append(Spacer(1, 20))
        
        # Resource Requirements
        story.append(Paragraph("Resource Requirements", self.custom_styles['Heading']))
        story.append(Paragraph("The following resources are recommended for implementing the action plan:", self.custom_styles['Normal']))
        story.append(Spacer(1, 10))
        
        resource_requirements = []
        if any("budget" in rec.description.lower() or "cost" in rec.description.lower() for rec in recommendations):
            resource_requirements.append("• Additional budget allocation for contingency")
        if any("timeline" in rec.description.lower() or "schedule" in rec.description.lower() for rec in recommendations):
            resource_requirements.append("• Project management resources for timeline adjustment")
        if any("resource" in rec.description.lower() or "manpower" in rec.description.lower() for rec in recommendations):
            resource_requirements.append("• Additional manpower or equipment as needed")
        if any("environmental" in rec.description.lower() for rec in recommendations):
            resource_requirements.append("• Environmental compliance specialists")
        
        if resource_requirements:
            for req in resource_requirements:
                story.append(Paragraph(req, self.custom_styles['Normal']))
        else:
            story.append(Paragraph("• Standard project resources should be sufficient", self.custom_styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Overall DPR Health
        overall_score = sum(risk_scores.values()) / len(risk_scores)
        health = self._get_dpr_health(overall_score)
        story.append(Paragraph(f"Overall DPR Health: {health}", self.custom_styles['Heading']))
        
        # Build PDF
        doc.build(story)
        print(f"Recommendation report saved to {filename}")
        return filename
    
    def _create_risk_chart(self, risk_scores: Dict[str, float]) -> io.BytesIO:
        """
        Create risk visualization chart
        """
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        risks = list(risk_scores.keys())
        scores = list(risk_scores.values())
        
        # Color bars based on risk level
        colors_list = []
        for score in scores:
            if score >= 0.7:
                colors_list.append('red')
            elif score >= 0.4:
                colors_list.append('orange')
            else:
                colors_list.append('green')
        
        bars = ax.bar(risks, scores, color=colors_list)
        ax.set_ylabel('Risk Score (0-1)')
        ax.set_title('DPR Risk Analysis')
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{score:.2f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def _create_pie_chart(self, risk_scores: Dict[str, float]) -> io.BytesIO:
        """
        Create pie chart of risk distribution
        """
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        risks = list(risk_scores.keys())
        scores = list(risk_scores.values())
        
        # Only show risks with score > 0.1
        filtered_risks = []
        filtered_scores = []
        for risk, score in zip(risks, scores):
            if score > 0.1:
                filtered_risks.append(risk)
                filtered_scores.append(score)
        
        if filtered_scores:
            ax.pie(filtered_scores, labels=filtered_risks, autopct='%1.1f%%', startangle=90)
        else:
            ax.pie([1], labels=['No Significant Risks'], autopct='%1.1f%%', startangle=90)
        
        ax.set_title('Risk Distribution')
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def _create_risk_correlation_chart(self, risk_scores: Dict[str, float], extraction: EnhancedDPRExtraction) -> io.BytesIO:
        """
        Create risk correlation analysis chart
        """
        # Create heatmap-style visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create a matrix of risk factors and their correlations
        risk_factors = list(risk_scores.keys())
        num_factors = len(risk_factors)
        
        # Create a correlation-like matrix (simplified for visualization)
        correlation_matrix = np.random.rand(num_factors, num_factors)  # Placeholder
        
        # For actual correlation, we'll create a matrix based on risk scores
        for i in range(num_factors):
            for j in range(num_factors):
                if i == j:
                    correlation_matrix[i][j] = 1.0
                else:
                    # Simplified correlation based on risk score similarity
                    score_diff = abs(risk_scores[risk_factors[i]] - risk_scores[risk_factors[j]])
                    correlation_matrix[i][j] = 1.0 - score_diff
        
        # Create heatmap
        im = ax.imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
        ax.set_xticks(np.arange(num_factors))
        ax.set_yticks(np.arange(num_factors))
        ax.set_xticklabels(risk_factors, rotation=45, ha='right')
        ax.set_yticklabels(risk_factors)
        ax.set_title('Risk Factor Correlation Analysis')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Correlation Strength')
        
        # Add value annotations
        for i in range(num_factors):
            for j in range(num_factors):
                text = ax.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                              ha="center", va="center", color="black")
        
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer
    
    def _get_risk_level(self, score: float) -> str:
        """
        Determine risk level based on score
        """
        if score >= 0.7:
            return "High Risk"
        elif score >= 0.4:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def _get_risk_style(self, risk_level: str) -> ParagraphStyle:
        """
        Get appropriate style for risk level
        """
        if "High" in risk_level:
            return self.custom_styles['RiskHigh']
        elif "Medium" in risk_level:
            return self.custom_styles['RiskMedium']
        else:
            return self.custom_styles['RiskLow']
    
    def _get_dpr_quality(self, score: float) -> str:
        """
        Determine DPR quality based on average risk score
        """
        if score <= 0.3:
            return "Excellent"
        elif score <= 0.6:
            return "Good"
        else:
            return "Poor"
    
    def _get_dpr_health(self, score: float) -> str:
        """
        Determine DPR health based on average risk score
        """
        if score <= 0.3:
            return "Excellent"
        elif score <= 0.6:
            return "Good"
        else:
            return "Poor"
    
    def _get_risk_analysis(self, risk_type: str, score: float, extraction: EnhancedDPRExtraction) -> str:
        """
        Provide detailed analysis for each risk type based on DPR data
        """
        if "cost" in risk_type.lower():
            if extraction.estimated_cost:
                return f"Based on estimated cost of {extraction.estimated_cost}, consider reviewing budget allocation and adding contingency funds."
            else:
                return "Cost estimation data is missing. Recommend adding detailed budget breakdown."
        elif "schedule" in risk_type.lower():
            if extraction.duration:
                return f"Project duration of {extraction.duration} may be insufficient. Consider adding buffer time."
            else:
                return "Timeline data is missing. Recommend specifying clear project milestones."
        elif "resource" in risk_type.lower():
            if extraction.num_employees:
                return f"With {extraction.num_employees} employees allocated, ensure adequate staffing for critical phases."
            else:
                return "Resource allocation data is incomplete. Recommend specifying manpower requirements."
        elif "environmental" in risk_type.lower():
            if extraction.environmental_risks:
                return f"Identified environmental risks: {extraction.environmental_risks}. Ensure compliance with regulations."
            else:
                return "Environmental risk assessment is missing. Recommend conducting environmental impact study."
        else:
            return f"Risk score of {score:.2f} indicates potential issues. Recommend detailed analysis."
    
    def _get_recommendation_context(self, recommendation: Recommendation, risk_scores: Dict[str, float], extraction: EnhancedDPRExtraction) -> str:
        """
        Provide context for each recommendation based on DPR data
        """
        # Get the highest risk score to provide context
        max_risk_type = max(risk_scores, key=risk_scores.get)
        max_risk_score = risk_scores[max_risk_type]
        
        if "cost" in recommendation.improvement_type.lower() or "budget" in recommendation.improvement_type.lower():
            if extraction.estimated_cost:
                return f"Based on {extraction.estimated_cost} budget and {max_risk_score:.2f} cost overrun risk."
            else:
                return f"High cost overrun risk ({max_risk_score:.2f}) with missing budget data."
        elif "schedule" in recommendation.improvement_type.lower() or "timeline" in recommendation.improvement_type.lower():
            if extraction.duration:
                return f"Based on {extraction.duration} timeline and {max_risk_score:.2f} schedule delay risk."
            else:
                return f"High schedule delay risk ({max_risk_score:.2f}) with missing timeline data."
        elif "resource" in recommendation.improvement_type.lower():
            if extraction.num_employees:
                return f"Based on {extraction.num_employees} employees and {max_risk_score:.2f} resource shortage risk."
            else:
                return f"High resource shortage risk ({max_risk_score:.2f}) with missing resource data."
        else:
            return f"Based on {max_risk_type} risk score of {max_risk_score:.2f}."
    
    def _create_cost_timeline_chart(self, extraction: EnhancedDPRExtraction) -> io.BytesIO:
        """
        Create cost vs timeline visualization
        """
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract cost and timeline data
        cost_value = 0
        timeline_months = 0
        
        # Try to extract numeric values
        if extraction.estimated_cost:
            # Extract numeric value from cost string
            cost_text = extraction.estimated_cost.lower().replace('₹', '').replace('rs', '').replace('rupees', '').strip()
            try:
                # Handle crore/lakh notation
                if 'crore' in cost_text:
                    cost_value = float(cost_text.split('crore')[0].strip()) * 10000000
                elif 'lakh' in cost_text:
                    cost_value = float(cost_text.split('lakh')[0].strip()) * 100000
                else:
                    # Try to extract first number
                    import re
                    numbers = re.findall(r'\d+\.?\d*', cost_text)
                    if numbers:
                        cost_value = float(numbers[0])
            except:
                cost_value = 1000000  # Default value
        
        if extraction.duration:
            # Extract months from duration
            duration_text = extraction.duration.lower()
            try:
                if 'month' in duration_text:
                    timeline_months = int(duration_text.replace('months', '').replace('month', '').strip())
                elif 'year' in duration_text:
                    years = int(duration_text.replace('years', '').replace('year', '').strip())
                    timeline_months = years * 12
            except:
                timeline_months = 12  # Default value
        
        # Create visualization
        categories = ['Estimated Cost (₹)', 'Duration (Months)']
        values = [cost_value / 1000000, timeline_months]  # Convert cost to crores for visualization
        
        bars = ax.bar(categories, values, color=['blue', 'green'])
        ax.set_ylabel('Value')
        ax.set_title('Cost vs Timeline Analysis')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            if bar.get_height() > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values) * 0.01,
                       f'{value:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        
        return buffer