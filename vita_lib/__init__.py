"""
VITA (Virtual Interactive Teaching Assistant) Library

This package provides modular components for the VITA application:
- Authentication: GitHub OAuth handling
- LLM: Local LLM communication
- File handling: File upload and processing
- UI: User interface components
- Config: Configuration management
"""

__version__ = "1.0.0"
__author__ = "VITA Team"

# Import main components for easy access
try:
    from .auth import GitHubAuth
    from .llm import call_local_llm, build_chat_callback
    from .file_handler import FileUploader
    from .main_app import AuthenticatedVITA
    from .config import Config

    __all__ = [
        "GitHubAuth",
        "call_local_llm", 
        "build_chat_callback",
        "FileUploader",
        "AuthenticatedVITA",
        "Config"
    ]
except ImportError as e:
    # Handle case where dependencies are not available
    print(f"Warning: Some VITA components could not be imported: {e}")
    __all__ = []
