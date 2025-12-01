#!/bin/bash
set -e

echo "Starting build process..."

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Install dependencies
echo "Installing dependencies..."
npm ci

# Run build
echo "Running build..."
npm run build

echo "Build completed successfully!"