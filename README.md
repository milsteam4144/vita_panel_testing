# Vita Application

This repository contains the Vita Panel Demo, a Python application that uses Panel and Autogen to create an interactive chat interface for debugging and explaining code.

## Setup and Running

Follow these steps to set up and run the Vita Panel Demo:

1. **Clone the repository:**
   ```
   Open a terminal and cd into wherever you want your local repository to be.
   Run the commands below:

   git clone https://github.com/yourusername/vita-panel-demo.git <-- replace with YOUR github username
   cd vita-panel-demo
   ```

2. **Set up the Gitub OAuth environment variables (Optional):**

   By default, OAuth authentication is disabled for easier testing. To enable OAuth:
   
   **Windows:**
   ```
   set SKIP_OAUTH=False
   set GITHUB_CLIENT_ID=<your_key_here>
   set GITHUB_CLIENT_SECRET=<your_key_here>
   ```
   
   **Linux/macOS/GitHub Codespaces:**
   ```
   export SKIP_OAUTH=False
   export GITHUB_CLIENT_ID=<your_key_here>
   export GITHUB_CLIENT_SECRET=<your_key_here>
   ```
   
   Instructions on how to create your GitHub OAuth credentials can be found here:
   https://www.freecodecamp.org/news/how-to-set-up-a-github-oauth-application/#:~:text=Create%20Your%20Application,client%20secret%22%20to%20do%20so.
   
   Note: When SKIP_OAUTH is True (default), the app will start directly without login.

3. **Configure LLM Backend (Optional):**

   By default, VITA uses LM Studio for the local LLM. For Linux users, Ollama is also supported:
   
   **To use Ollama:**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the TinyLlama model
   ollama pull tinyllama
   
   # Set environment variables before running VITA
   export LLM_BACKEND="ollama"
   export OLLAMA_MODEL="tinyllama"  # or any model from 'ollama list'
   # export OLLAMA_URL="http://localhost:11434/api/chat"  # Optional: custom Ollama URL
   ```
   
   **To use LM Studio (default):**
   - Download and install LM Studio from https://lmstudio.ai/
   - Load the TinyLlama model in LM Studio
   - Start the local server in LM Studio (default port 1234)

4. **Run the program using a starter file**

   Ensure you are still in the vita_panel_testing directory...
   On a Windows machine, run the command: run_vita_app.bat
   On a Linus or MacOS, run the command: run_vita_app.sh

## Usage
- Log in with Github credentials
- Use the file uploader to upload a Python file for debugging.
- Click the "Debug the uploaded code" button to start a debugging session.
- Click the "Explain a concept" button to ask about programming concepts.
- Interact with the chat interface to debug your code or learn about programming concepts.

For any issues or questions, please open an issue in the GitHub repository.

