#!/bin/bash
# Startup script for Render deployment

echo "Starting AI DPR Evaluation System..."

# Check if we're running on Render
if [ -n "$RENDER" ]; then
    echo "Running on Render environment"
else
    echo "Running in local environment"
fi

# Check if MONGODB_URL is set
if [ -z "$MONGODB_URL" ]; then
    echo "WARNING: MONGODB_URL environment variable not set"
else
    echo "Using MongoDB connection string from environment"
fi

# Start the application
echo "Starting uvicorn server..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}