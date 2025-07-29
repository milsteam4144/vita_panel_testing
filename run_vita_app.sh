#!/bin/bash

# Set default for SKIP_OAUTH if not already set
export SKIP_OAUTH="${SKIP_OAUTH:-True}"

# LLM Backend Configuration (new options for Ollama support)
# Set LLM_BACKEND to "ollama" to use Ollama instead of LM Studio
# export LLM_BACKEND="ollama"
# export OLLAMA_URL="http://localhost:11434/api/chat"  # Default Ollama URL
# export OLLAMA_MODEL="tinyllama"  # Model name as shown in 'ollama list'

# Check for environment variables only if OAuth is not being skipped
if [[ "$SKIP_OAUTH" != "True" && "$SKIP_OAUTH" != "true" && "$SKIP_OAUTH" != "1" && "$SKIP_OAUTH" != "yes" ]]; then
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
else
    echo "🔓 OAuth authentication is disabled (SKIP_OAUTH=$SKIP_OAUTH)"
fi

# Check if we can use a virtual environment
if command -v python3 &> /dev/null; then
    # Try to create/use virtual environment
    if [[ ! -d "vita_venv" ]] || [[ ! -f "vita_venv/bin/activate" ]]; then
        echo "📦 Attempting to create virtual environment..."
        python3 -m venv vita_venv 2>/dev/null
        if [[ $? -ne 0 ]]; then
            echo "⚠️  Could not create virtual environment. This may require:"
            echo "   sudo apt install python3-venv"
            echo "   Continuing without virtual environment..."
            VENV_FAILED=true
        fi
    fi
    
    # Activate virtual environment if it exists
    if [[ -f "vita_venv/bin/activate" ]]; then
        echo "🔧 Activating virtual environment..."
        source vita_venv/bin/activate
    fi
fi

# Install dependencies
echo "📦 Installing dependencies..."

# Use Linux-specific requirements file if it exists, otherwise filter out Windows packages
if [[ -f "requirements-linux.txt" ]]; then
    REQUIREMENTS_FILE="requirements-linux.txt"
else
    # Create Linux requirements file by filtering out Windows-specific packages
    grep -v "pywin32" requirements.txt > requirements-linux.txt
    REQUIREMENTS_FILE="requirements-linux.txt"
fi

echo "   Using $REQUIREMENTS_FILE"

if [[ -z "$VIRTUAL_ENV" ]]; then
    # Not in virtual environment, try different approaches
    echo "   Installing to user directory (no virtual environment active)..."
    
    # First try with python3 -m pip
    python3 -m pip install --user -r "$REQUIREMENTS_FILE" 2>/dev/null
    
    if [[ $? -ne 0 ]]; then
        echo "   Standard install failed. Trying with --break-system-packages..."
        python3 -m pip install --user --break-system-packages -r "$REQUIREMENTS_FILE"
    fi
else
    # In virtual environment, install normally
    pip install -r "$REQUIREMENTS_FILE"
fi

if [[ $? -ne 0 ]]; then
    echo "❌ Failed to install dependencies."
    echo "   You may need to run: sudo apt install python3-venv"
    echo "   Or install packages manually."
    exit 1
fi

# Start the Panel app
echo "🚀 Starting VITA Assistant..."
python3 -m panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
