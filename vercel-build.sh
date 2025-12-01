#!/bin/bash

# Vercel build script for AI DPR Evaluation System
echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
npm ci

# Run build
echo "Running build..."
npm run build

echo "Build completed successfully!"