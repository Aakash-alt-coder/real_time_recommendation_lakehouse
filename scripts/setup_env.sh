#!/bin/bash
# Local environment setup script for Real-Time Recommendation Lakehouse
# Usage: bash scripts/setup_env.sh

set -e

echo "Setting up your local environment..."

# Check if .env.sample exists
if [ ! -f .env.sample ]; then
    echo ".env.sample file not found. Please make sure it exists in the project root."
    exit 1
fi

# Copy .env.sample to .env if .env doesn't exist
if [ ! -f .env ]; then
    cp .env.sample .env
    echo ".env file created from .env.sample."
else
    echo ".env file already exists. Skipping copy."
fi

# Create local data folders for bronze/silver/gold if they don’t exist
for d in bronze silver gold; do
  if [ ! -d "data/$d" ]; then
    mkdir -p "data/$d"
    echo "Created directory data/$d."
  fi
done

# Install Python dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
fi

echo "Local environment setup complete."