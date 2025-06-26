# VITA Library

This directory contains the modularized components of the VITA (Virtual Interactive Teaching Assistant) application.

## Modules

### `config.py`
- Handles environment variables and application configuration
- Contains the `Config` class with OAuth settings and validation methods

### `auth.py`
- Manages GitHub OAuth authentication flow
- Contains the `GitHubAuth` class with authorization and user info retrieval methods

### `llm.py`
- Handles communication with local LLM services
- Contains functions for calling the LLM and building chat callbacks

### `file_handler.py`
- Manages file upload and processing functionality
- Contains the `FileUploader` class for handling Python file uploads

### `main_app.py`
- Contains the main `AuthenticatedVITA` class that orchestrates the application
- Handles the login view and main application interface

## Usage

The library can be imported as a whole:

```python
from vita_lib import Config, GitHubAuth, AuthenticatedVITA, FileUploader
```

Or individual components can be imported:

```python
from vita_lib.auth import GitHubAuth
from vita_lib.config import Config
```

## Dependencies

This library requires:
- panel
- param  
- authlib
- requests
- webbrowser (standard library)
- asyncio (standard library)
- urllib.parse (standard library)