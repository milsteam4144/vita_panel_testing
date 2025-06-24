# Link to A.N. VITA (backend)
# https://github.com/norrisaftcc/tool-vita

# Vita Panel Demo

This repository contains the Vita Panel Demo, a Python application that uses Panel and Autogen to create an interactive chat interface for debugging and explaining code.

## Setup and Running

Follow these steps to set up and run the Vita Panel Demo:

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/vita-panel-demo.git
   cd vita-panel-demo
   ```

2. **Set up the environment variable:**

   On a Windows machine, in the Windows search bar, search for "Edit the system environment variables
   Add User environment variables

   In a Github codespace, open a terminal and enter the environment variables using the Linux commands:
   export GITHUB_CLIENT_ID=""
   export GITHUB_CLIENT_SECRET=""


   

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

## RAG 
- for the backend rag stuff im using flask, json, sentence transformers, numpy, and faiss
-Had to make a virtual enviroment called env
- the file is rag_backend.py
