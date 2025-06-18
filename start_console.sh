#!/bin/bash

# VITA Console Demo Startup Script
# This script activates the virtual environment and starts the console demo

set -e  # Exit on any error

echo "🚀 Starting VITA Console Demo..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created."
else
    echo "✅ Virtual environment found."
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY environment variable not set."
    echo "   You may need to set it for full functionality."
fi

# Start the console demo
echo "🎓 Starting VITA Console Demo..."
if [ -f "vita_console_demo.py" ]; then
    python vita_console_demo.py
elif [ -f "test.py" ]; then
    echo "📊 Running test.py instead..."
    panel serve test.py --autoreload
else
    echo "❌ Could not find console demo file to run."
    echo "Available Python files:"
    ls -la *.py
    exit 1
fi