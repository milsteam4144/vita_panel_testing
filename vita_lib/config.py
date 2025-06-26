"""
Configuration module for VITA application.

Handles environment variables and application configuration.
"""

import os


class Config:
    """Configuration class for VITA application settings."""
    
    # GitHub OAuth Configuration
    CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:8501/vita_app"
    
    # OAuth endpoints for GitHub
    AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_API_URL = "https://api.github.com/user"
    
    # Application settings
    PORT = 8501
    HOST = "localhost"
    
    # Docker settings
    AUTOGEN_USE_DOCKER = "False"
    
    @classmethod
    def validate_oauth_config(cls):
        """Validate that required OAuth environment variables are set."""
        missing = []
        if not cls.CLIENT_ID:
            missing.append("GITHUB_CLIENT_ID")
        if not cls.CLIENT_SECRET:
            missing.append("GITHUB_CLIENT_SECRET")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables for the application."""
        os.environ["AUTOGEN_USE_DOCKER"] = cls.AUTOGEN_USE_DOCKER