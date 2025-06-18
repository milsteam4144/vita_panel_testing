# Vita Panel Demo

This repository contains the Vita Panel Demo, a Python application that uses Panel and Autogen to create an interactive chat interface for debugging and explaining code.

## Setup and Running

Follow these steps to set up and run the Vita Panel Demo:

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/vita-panel-demo.git
   cd vita-panel-demo
   ```

2. **Choose your AI model setup:**

   **Option A: Local LM Studio (Recommended for MVP Demo)**
   
   1. Download and install [LM Studio](https://lmstudio.ai/)
   2. Load a compatible model (e.g., Llama 3.1, Mistral, etc.)
   3. Start the local server in LM Studio (default: http://localhost:1234)
   4. Set environment variables:
   
   For Linux/macOS:
   ```
   export USE_LOCAL_MODEL=true
   export LOCAL_MODEL_NAME="your-model-name"
   export LOCAL_MODEL_URL="http://localhost:1234/v1"
   ```

   For Windows (Command Prompt):
   ```
   set USE_LOCAL_MODEL=true
   set LOCAL_MODEL_NAME=your-model-name
   set LOCAL_MODEL_URL=http://localhost:1234/v1
   ```

   **Option B: OpenAI API**
   
   For Linux/macOS:
   ```
   export USE_LOCAL_MODEL=false
   export OPENAI_API_KEY='your_api_key_here'
   ```

   For Windows (Command Prompt):
   ```
   set USE_LOCAL_MODEL=false
   set OPENAI_API_KEY=your_api_key_here
   ```

3. **Install dependencies:**
   ```
   pip install panel pyautogen openai
   ```

4. **Run the application:**
   ```
   panel serve panel_test.py
   ```

5. **Access the application:**
   Open a web browser and go to `http://localhost:5006`

## Usage

- Use the file uploader to upload a Python file for debugging.
- Click the "Debug the uploaded code" button to start a debugging session.
- Click the "Explain a concept" button to ask about programming concepts.
- Interact with the chat interface to debug your code or learn about programming concepts.

For any issues or questions, please open an issue in the GitHub repository.

