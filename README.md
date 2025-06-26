# VITA Application

This repository contains VITA (Virtual Interactive Teaching Assistant), a modular Python application that uses Panel and Autogen to create an interactive chat interface for debugging and explaining code.

## 🏗️ Architecture

VITA has been modularized into a clean library structure for better maintainability and extensibility:

### Main Application
- `vita_app.py` - Main application entry point (now streamlined to ~37 lines)
- `vita_app_original.py` - Original monolithic version (backup)

### VITA Library (`vita_lib/`)
- `__init__.py` - Library initialization and exports
- `config.py` - Configuration management and environment variables
- `auth.py` - GitHub OAuth authentication handling
- `llm.py` - Local LLM communication functions
- `file_handler.py` - File upload and processing functionality  
- `main_app.py` - Main application UI and orchestration logic
- `README.md` - Library documentation

### User Interface
- `user_interface/` - CSS styles and assets

## Setup and Running

Follow these steps to set up and run the Vita Panel Demo:

1. **Clone the repository:**
   ```
   Open a terminal and cd into wherever you want your local repository to be.
   Run the commands below:

   git clone https://github.com/yourusername/vita-panel-demo.git <-- replace with YOUR github username
   cd vita-panel-demo
   ```

2. **Set up the Gitub OAuth environment variables:**

   Instructions on how to create your Gitub OAuth credentials can be found here:
   https://www.freecodecamp.org/news/how-to-set-up-a-github-oauth-application/#:~:text=Create%20Your%20Application,client%20secret%22%20to%20do%20so.

   On a Windows machine, open a terminal and run the following commands:
   set GITHUB_CLIENT_ID=<your_key_here>
   set GITHUB_CLIENT_SECRET=<your_key_here>

   In a Github codespace, open a terminal and enter the environment variables using the Linux commands:
   export GITHUB_CLIENT_ID=<your_key_here>
   export GITHUB_CLIENT_SECRET=<your_key_here>

3. **Run the program using a starter file**

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

