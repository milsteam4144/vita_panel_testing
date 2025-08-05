#!/bin/bash

# Install dependencies (with break-system-packages flag for VM environment)
echo "📦 Installing dependencies from requirements.txt..."
pip install --break-system-packages --user -r requirements.txt
if [[ $? -ne 0 ]]; then
    echo "❌ Failed to install dependencies. Aborting."
    exit 1
fi

# Start the Panel app
echo "🚀 Starting VITA Assistant..."
python3 -m panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
