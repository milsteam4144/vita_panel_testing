#!/bin/bash

# VITA Enhanced RAG System - Linux Deployment Script
# This script sets up and runs the VITA application with enhanced RAG capabilities on Ubuntu/Linux

set -e  # Exit on any error

echo "=========================================="
echo "VITA Enhanced RAG System - Linux Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_error "This script is designed for Linux systems. Detected OS: $OSTYPE"
    exit 1
fi

# Check if Python 3.8+ is available
print_step "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_status "Found Python $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Install system dependencies for Python packages
print_step "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    git

print_status "System dependencies installed"

# Create and activate virtual environment
print_step "Setting up Python virtual environment..."
if [ ! -d "vita_venv" ]; then
    python3 -m venv vita_venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source vita_venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies first
print_step "Installing core dependencies..."
pip install \
    sentence-transformers==2.2.2 \
    faiss-cpu==1.7.4 \
    scikit-learn==1.6.1 \
    numpy==2.3.1

print_status "Core dependencies installed"

# Install content extraction dependencies
print_step "Installing content extraction dependencies..."
pip install \
    beautifulsoup4==4.12.3 \
    python-pptx==1.0.2 \
    lxml \
    nbformat

print_status "Content extraction dependencies installed"

# Try to install ChromaDB (may require additional system packages)
print_step "Installing ChromaDB..."
if ! pip install chromadb==0.5.23; then
    print_warning "ChromaDB installation failed. Installing additional build dependencies..."
    
    # Install additional build tools that might be needed
    sudo apt-get install -y \
        cmake \
        g++ \
        gcc \
        libc6-dev \
        make \
        pkg-config
    
    # Try ChromaDB again
    if pip install chromadb==0.5.23; then
        print_status "ChromaDB installed successfully after installing build tools"
    else
        print_warning "ChromaDB installation failed. The app will run with fallback RAG system."
    fi
else
    print_status "ChromaDB installed successfully"
fi

# Install remaining requirements
print_step "Installing remaining requirements..."
if [ -f "requirements.txt" ]; then
    # Install requirements but skip the ones we already installed
    pip install -r requirements.txt || print_warning "Some packages from requirements.txt may have failed to install"
    print_status "Requirements installation completed"
else
    print_warning "requirements.txt not found. Installing essential packages manually..."
    pip install \
        panel==1.7.1 \
        param==2.2.1 \
        pydantic \
        requests \
        asyncio
fi

# Test content extraction
print_step "Testing content extraction..."
if python3 -c "
from content_extractor import ContentExtractor
extractor = ContentExtractor()
chunks = extractor.extract_all_content()
print(f'Successfully extracted {len(chunks)} content chunks')
if chunks:
    print(f'Sample: {chunks[0][\"source_file\"]} - {chunks[0][\"chunk_type\"]}')
" 2>/dev/null; then
    print_status "Content extraction test passed"
else
    print_warning "Content extraction test failed, but app may still work with basic RAG"
fi

# Test RAG backend
print_step "Testing RAG backend..."
if python3 -c "
from vita_app import rag_backend
if rag_backend:
    results = rag_backend.query('test', k=1)
    print(f'RAG backend working: {len(results)} results')
else:
    print('RAG backend not initialized')
" 2>/dev/null; then
    print_status "RAG backend test passed"
else
    print_warning "RAG backend test failed"
fi

# Setup enhanced RAG database (if ChromaDB is available)
print_step "Setting up enhanced RAG database..."
if python3 -c "import chromadb" 2>/dev/null; then
    print_status "ChromaDB available, setting up enhanced RAG database..."
    if python3 setup_rag_database.py; then
        print_status "Enhanced RAG database setup completed"
    else
        print_warning "Enhanced RAG database setup failed, falling back to basic RAG"
    fi
else
    print_warning "ChromaDB not available, using basic RAG system"
fi

# Check if instructor_created_data exists
if [ ! -d "instructor_created_data" ]; then
    print_warning "instructor_created_data directory not found."
    print_warning "Enhanced RAG features will not be available."
    print_warning "Please ensure this directory contains your educational content."
fi

# Final system test
print_step "Running final system test..."
if python3 test_enhanced_rag.py 2>/dev/null; then
    print_status "System test passed"
else
    print_warning "System test had some failures, but app may still work"
fi

print_step "Deployment completed!"
echo ""
echo "=========================================="
echo "VITA System Ready!"
echo "=========================================="
echo ""
print_status "To start the VITA application:"
echo ""
echo "  1. Ensure you're in the project directory"
echo "  2. Activate the virtual environment:"
echo "     source vita_venv/bin/activate"
echo ""
echo "  3. Start the application:"
echo "     python3 vita_app.py"
echo ""
echo "  4. Or use the provided scripts:"
echo "     chmod +x run_vita_app.sh"
echo "     ./run_vita_app.sh"
echo ""

if python3 -c "import chromadb" 2>/dev/null; then
    print_status "Enhanced RAG with ChromaDB is available"
else
    print_warning "Using fallback RAG system (basic functionality)"
fi

echo ""
print_status "The application will be available at the configured host/port"
print_status "Check the application logs for the exact URL"
echo ""

# Optional: Run the app immediately
read -p "Would you like to start the VITA application now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting VITA application..."
    python3 vita_app.py
fi

print_status "Deployment script completed successfully!"