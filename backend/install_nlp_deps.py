"""
Script to download required NLP models for the AI layer
"""
import subprocess
import sys

def install_spacy_model():
    """Install the required spaCy English model"""
    try:
        # Try to import spacy first
        import spacy
        print("spaCy is already installed.")
    except ImportError:
        print("Installing spaCy...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
        import spacy
    
    # Check if the model is already installed
    try:
        spacy.load("en_core_web_sm")
        print("spaCy English model (en_core_web_sm) is already installed.")
    except OSError:
        print("Downloading spaCy English model (en_core_web_sm)...")
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            print("spaCy English model installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading spaCy model: {e}")
            print("You can manually install it with: python -m spacy download en_core_web_sm")
            return False
    
    return True

def main():
    print("Installing AI/NLP dependencies...")
    
    # Install spaCy model
    if install_spacy_model():
        print("All NLP dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Run 'python init_ai.py' to generate training data and train models")
        print("2. Start the server with 'uvicorn main:app --reload'")
        print("3. Use the enhanced AI endpoints for DPR analysis")
    else:
        print("Failed to install NLP dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main()