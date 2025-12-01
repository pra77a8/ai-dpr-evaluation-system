"""
Script to initialize and train AI models for the DPR Evaluation System
"""
import os
import sys
import pandas as pd
from app.ai.dataset_generator import DatasetGenerator
from app.ai.risk_predictor import RiskPredictor

def main():
    print("Initializing AI models for DPR Evaluation System...")
    
    # Add the backend directory to the Python path
    backend_dir = os.path.join(os.path.dirname(__file__), '.')
    sys.path.append(backend_dir)
    
    try:
        # Step 1: Generate training dataset
        print("Step 1: Generating training dataset...")
        dataset_generator = DatasetGenerator()
        dataset = dataset_generator.generate_dataset(1000)  # Generate 1000 samples
        dataset_generator.save_dataset_to_csv(dataset, "dpr_training_dataset.csv")
        print("Training dataset generated successfully!")
        
        # Step 2: Train risk prediction model
        print("Step 2: Training risk prediction model...")
        risk_predictor = RiskPredictor()
        
        # Check if we have the dataset
        if os.path.exists("dpr_training_dataset.csv"):
            # Prepare data
            X, y = risk_predictor.prepare_data("dpr_training_dataset.csv")
            
            # Train model
            risk_predictor.train_model(X, y)
            print("Risk prediction model trained successfully!")
        else:
            print("Warning: Training dataset not found. Creating fallback model...")
            risk_predictor._create_fallback_model()
            risk_predictor.save_model()
        
        print("AI initialization completed successfully!")
        print("\nNext steps:")
        print("1. The system is now ready to process DPRs with AI analysis")
        print("2. Use the /api/dpr/upload_with_ai endpoint to upload DPRs with full AI analysis")
        print("3. Use the /api/ai/chat endpoint to chat with DPRs")
        print("4. PDF reports will be generated automatically")
        
    except Exception as e:
        print(f"Error during AI initialization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()