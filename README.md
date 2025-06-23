# VITA Panel Testing

Link to A.N. VITA backend: https://github.com/norrisaftcc/tool-vita

This repository contains the VITA Panel application, a modular Python application that uses Panel and AutoGen to create an interactive chat interface for debugging and explaining Python code with GitHub OAuth authentication.

## Architecture

The application has been refactored into a clean modular structure:

### Core Modules

- **`main.py`** - Main startup script and entry point
- **`vita_app.py`** - Main application logic and UI components  
- **`github_auth.py`** - GitHub OAuth authentication handling
- **`file_uploader.py`** - File upload and display functionality
- **`chat_agents.py`** - AutoGen chat agents and conversation management

### Module Dependencies

```
main.py
├── vita_app.py
│   ├── github_auth.py
│   ├── file_uploader.py  
│   └── chat_agents.py
```

## Setup and Running

### Prerequisites

1. **Environment Variables:**
   
   Set up your GitHub OAuth application and configure the following environment variables:
   
   ```bash
   export GITHUB_CLIENT_ID="your_github_client_id"
   export GITHUB_CLIENT_SECRET="your_github_client_secret"
   ```
   
   On Windows, use the Environment Variables dialog or set them in your terminal:
   ```cmd
   set GITHUB_CLIENT_ID=your_github_client_id
   set GITHUB_CLIENT_SECRET=your_github_client_secret
   ```

2. **Install Dependencies:**
   ```bash
   pip install panel pyautogen openai param authlib requests
   ```

### Running the Application

1. **Clone the repository:**
   ```bash
   git clone https://github.com/milsteam4144/vita_panel_testing.git
   cd vita_panel_testing
   ```

2. **Run the application:**
   ```bash
   panel serve main.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
   ```

3. **Access the application:**
   Open a web browser and go to `http://localhost:8501`

## Usage

1. **Authentication**: Log in with your GitHub account using OAuth
2. **File Upload**: Upload a Python (.py) file for analysis
3. **Debug Code**: Click "Debug the uploaded code" to get AI assistance with errors
4. **Learn Concepts**: Select programming concepts and get AI explanations
5. **Interactive Chat**: Engage with the AI tutors (Debugger and Corrector) for help

## Module Details

### `github_auth.py`
- `GitHubAuth` class for OAuth operations
- `fetch_avatar_as_base64()` for user avatar handling
- OAuth configuration and endpoints

### `file_uploader.py`  
- `FileUploader` class for handling Python file uploads
- Automatic line numbering and syntax highlighting
- Integration with global state management

### `chat_agents.py`
- `MyConversableAgent` custom AutoGen agent
- Chat interface integration
- Global state management for agent communication

### `vita_app.py`
- `AuthenticatedVITA` main application class
- OAuth callback handling and user session management
- UI layout and component creation
- AutoGen setup and configuration

### `main.py`
- Application entry point
- Layout initialization and Panel server configuration
- Minimal bootstrap code

## Development

The modular structure makes the codebase easier to:
- **Maintain**: Each module has a single responsibility
- **Test**: Individual components can be tested in isolation  
- **Extend**: New features can be added without affecting other modules
- **Debug**: Issues can be isolated to specific modules

For development, you can import and test individual modules:

```python
# Test authentication
from github_auth import GitHubAuth

# Test file upload
from file_uploader import FileUploader

# Test chat agents  
from chat_agents import MyConversableAgent

# Test main app
from vita_app import AuthenticatedVITA
```

## Troubleshooting

- Ensure GitHub OAuth environment variables are set correctly
- Check that all dependencies are installed
- Verify the Panel server is running on the correct port
- Check browser console for any JavaScript errors during OAuth flow

For any issues or questions, please open an issue in the GitHub repository.

