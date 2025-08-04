#!/bin/bash

# Check for environment variables
if [[ -z "$GITHUB_CLIENT_ID" ]]; then
    echo "[ERROR] GITHUB_CLIENT_ID is not set."
    MISSING=true
fi

if [[ -z "$GITHUB_CLIENT_SECRET" ]]; then
    echo "[ERROR] GITHUB_CLIENT_SECRET is not set."
    MISSING=true
fi

if [[ $MISSING == true ]]; then
    echo "❌ Please export the required environment variables:"
    echo "export GITHUB_CLIENT_ID=your_client_id"
    echo "export GITHUB_CLIENT_SECRET=your_client_secret"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [[ $? -ne 0 ]]; then
    echo "❌ Failed to install dependencies. Aborting."
    exit 1
fi

# Start the Panel app
echo "🚀 Starting VITA Assistant..."
panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
