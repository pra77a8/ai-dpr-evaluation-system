#!/bin/bash
# Build script for Render deployment

echo "Starting build process..."

# Upgrade pip to avoid installation issues
echo "Upgrading pip..."
pip install --upgrade pip

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
if ! pip install -r requirements.txt; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Download spaCy model if spaCy is installed
echo "Checking for spaCy installation..."
if python -c "import spacy" 2>/dev/null; then
    echo "spaCy found, downloading language model..."
    python -m spacy download en_core_web_sm
else
    echo "spaCy not found, skipping model download"
fi

echo "Build completed successfully!"