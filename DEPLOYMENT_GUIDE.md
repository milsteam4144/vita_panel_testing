# VITA Enhanced RAG System - Deployment Guide

## Overview

This guide covers deploying the VITA (Virtual Interactive Teaching Assistant) application with enhanced RAG (Retrieval Augmented Generation) capabilities on Linux systems.

## System Architecture

### Enhanced RAG Components

1. **Content Extraction** (`content_extractor.py`)
   - Processes Jupyter notebooks (.ipynb) by cells
   - Extracts HTML content by sections
   - Handles JSON Q&A files
   - Reads PowerPoint slides (.pptx format)
   - Smart chunking for better relevance

2. **Vector Database** (`rag_backend_enhanced.py`)
   - Primary: ChromaDB (persistent local storage)
   - Fallback: Original FAISS-based system
   - Automatic fallback handling

3. **Enhanced UI** (`vita_app.py`)
   - Displays "Sources Used" after responses
   - Shows filename + content preview
   - Backward compatible with existing setup

## Quick Deployment (Linux)

### Prerequisites
- Ubuntu 18.04+ or compatible Linux distribution
- Python 3.8 or higher
- Internet connection for package installation
- 2GB+ RAM recommended

### One-Command Deployment
```bash
chmod +x deploy_vita_linux.sh
./deploy_vita_linux.sh
```

## Manual Deployment Steps

### 1. System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv build-essential libssl-dev libffi-dev python3-setuptools git cmake g++ gcc libc6-dev make pkg-config
```

### 2. Virtual Environment
```bash
python3 -m venv vita_venv
source vita_venv/bin/activate
pip install --upgrade pip
```

### 3. Core Dependencies
```bash
# Essential ML packages
pip install sentence-transformers==2.2.2 faiss-cpu==1.7.4 scikit-learn==1.6.1 numpy==2.3.1

# Content extraction
pip install beautifulsoup4==4.12.3 python-pptx==1.0.2 lxml nbformat

# Vector database (may require build tools)
pip install chromadb==0.5.23

# Web framework and UI
pip install panel==1.7.1 param==2.2.1 pydantic requests
```

### 4. Application Setup
```bash
# Setup enhanced RAG database
python3 setup_rag_database.py

# Test the system
python3 test_enhanced_rag.py

# Start the application
python3 vita_app.py
```

## Tested Configurations

### Working Components ✅
- Content extraction from instructor_created_data
- Original RAG system (FAISS + dummy data)
- VITA application startup
- Fallback mechanisms
- Source display functionality

### Known Limitations ⚠️
- PowerPoint .ppt files (old format) not supported - only .pptx
- ChromaDB requires build tools on some systems
- Windows compatibility issues with build dependencies

## System Behavior

### With ChromaDB Available
- Full enhanced RAG with instructor content
- 200+ content chunks from educational materials
- Source attribution for each response
- Advanced semantic search

### Fallback Mode (Without ChromaDB)
- Uses original dummy data (9 Q&A pairs)
- Basic FAISS-based similarity search
- Limited but functional RAG capabilities
- Graceful degradation

## File Structure

```
vita_panel_testing/
├── vita_app.py                 # Main application
├── rag_backend_enhanced.py     # Enhanced RAG system
├── content_extractor.py        # Multi-format content extraction
├── setup_rag_database.py       # Database setup script
├── test_enhanced_rag.py        # System testing
├── deploy_vita_linux.sh        # Linux deployment script
├── instructor_created_data/    # Educational content
│   ├── HTML_Guides_byModule/   # Jupyter notebooks & HTML
│   ├── Python_Slides/          # PowerPoint presentations
│   ├── HTML_Slides/           # HTML-related slides
│   └── Q.As/                  # Q&A JSON files
├── data/dummy_data.json        # Fallback Q&A data
├── requirements.txt            # Python dependencies
└── chroma_db/                 # ChromaDB storage (created at runtime)
```

## Content Sources

The enhanced RAG system processes content from:

1. **Jupyter Notebooks** - Python programming tutorials by module
2. **HTML Guides** - Web development learning materials  
3. **JSON Q&A Files** - Question-answer pairs
4. **PowerPoint Slides** - Course presentations (.pptx only)

Total: ~250 content chunks from educational materials

## Troubleshooting

### ChromaDB Installation Issues
```bash
# Install additional build dependencies
sudo apt-get install -y cmake g++ gcc libc6-dev make pkg-config

# Or use conda if available
conda install chromadb
```

### PowerPoint Files Not Loading
- Only .pptx format supported
- Convert .ppt files to .pptx if needed
- Or exclude PowerPoint processing if not critical

### Memory Issues
- Ensure 2GB+ RAM available
- Reduce batch_size in database population
- Use smaller embedding models if needed

### Network Issues During Setup
- Ensure internet connectivity for package downloads
- Consider offline installation if needed
- Cache packages for repeated deployments

## Performance Optimization

### For Production Deployment
1. Use optimized embedding models
2. Configure ChromaDB for production
3. Implement caching strategies
4. Monitor resource usage
5. Set up proper logging

### For Development
1. Use smaller test datasets
2. Enable debug mode
3. Use local model servers
4. Implement hot reloading

## Security Considerations

- Virtual environment isolation
- No external API dependencies (local LLM)
- Local vector database storage
- Standard web application security practices

## Support

For issues specific to:
- **Content Extraction**: Check file formats and permissions
- **RAG System**: Verify database initialization and model loading
- **VITA App**: Check Panel framework and UI dependencies
- **Deployment**: Review system dependencies and Python environment

## Version Information

- **VITA Core**: Compatible with existing Panel-based UI
- **Enhanced RAG**: New ChromaDB integration with fallback
- **Content Processing**: Multi-format extraction system
- **Python**: 3.8+ required, tested on 3.12
- **Linux**: Ubuntu 18.04+ recommended