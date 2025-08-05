# VITA Application

VITA (Virtual Interactive Teaching Assistant) is a Python application that uses Panel and Ollama to create an interactive chat interface for debugging and explaining Python code.

## Features
- Upload Python files for debugging and analysis
- Get AI-powered explanations of programming concepts
- Interactive chat interface for learning Python
- Access to instructor-created examples and guides
- Support for various Python topics including:
  - Input/Output operations
  - Data types and structures
  - Control flow (branching and loops)
  - Functions and modules

## Prerequisites

### Linux Systems
- Python 3.12 or higher
- Ollama installed and running
- Internet connection for downloading dependencies

### Ollama Setup
1. Install Ollama from https://ollama.ai
2. Pull the required model:
   ```bash
   ollama pull qwen3:0.6b
   ```
3. Ensure Ollama is running (default port: 11434)

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/milsteam4144/vita_panel_testing.git
cd vita_panel_testing
```

### 2. Linux/macOS Setup
```bash
# Make the script executable
chmod +x run_vita_app.sh

# Run the application
./run_vita_app.sh
```

The script will:
- Install required Python dependencies
- Start the Panel server on port 8501
- Open the application in your default browser

### 3. Windows Setup
```batch
# Run the batch file
run_vita_app.bat
```

## Usage

### Main Interface
1. **Upload Code**: Use the file uploader to select a `.py` file for debugging
2. **Debug Code**: Click "Debug the uploaded code" to analyze your Python file
3. **Learn Concepts**: 
   - Select a topic from the dropdown menu
   - Click "See AI Examples" for AI-generated explanations
   - Click "See Instructor Examples" for curated learning materials
4. **Chat Interface**: Interact with the AI assistant for help with Python programming

### Available Programming Concepts
- **Input/Output**: Print functions, user input
- **Data Types**: Strings, integers, floats, formatted strings
- **Mathematical Expressions**: Basic operations, division, exponents
- **Data Structures**: Lists, dictionaries
- **Branching**: If/else statements, elif statements
- **Loops**: For loops, while loops
- **Functions**: Defining, calling, and main functions

## Testing

Run the connectivity test to verify Ollama integration:
```bash
python3 test_connectivity.py
```

## Troubleshooting

### Ollama Connection Issues
- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Check available models: `ollama list`
- Ensure the correct model is installed: `ollama pull qwen3:0.6b`

### Dependency Installation Issues
- On managed Python environments, the script uses `--break-system-packages` flag
- Consider using a virtual environment for isolation
- For Debian/Ubuntu systems, install `python3-venv` if needed

### Port Conflicts
If port 8501 is in use, modify the port in `run_vita_app.sh`:
```bash
panel serve vita_app.py --port YOUR_PORT --allow-websocket-origin=localhost:YOUR_PORT
```

## Project Structure
```
vita_panel_testing/
├── vita_app.py              # Main application
├── llm_connect.py           # Ollama integration
├── file_uploader.py         # File upload handler
├── auth.py                  # Legacy OAuth (unused)
├── run_vita_app.sh          # Linux/macOS startup script
├── run_vita_app.bat         # Windows startup script
├── requirements.txt         # Python dependencies
├── test_connectivity.py     # Ollama connectivity test
├── user_interface/          # UI assets
│   ├── logo.png
│   └── styles.css
└── instructor_created_data/ # Learning materials
```

## Contributing
For issues, questions, or contributions, please open an issue in the GitHub repository.

## License
This project is part of an educational initiative to help students learn Python programming.