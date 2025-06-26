"""
Authentication module for VITA application.

Handles GitHub OAuth authentication flow.
"""

import panel as pn
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session

from .config import Config


class GitHubAuth:
    """Handles GitHub OAuth authentication."""
    
    @staticmethod
    def get_authorization_url():
        """Generate GitHub OAuth authorization URL."""
        print(f"DEBUG: CLIENT_ID = {Config.CLIENT_ID}")
        print(f"DEBUG: REDIRECT_URI = {Config.REDIRECT_URI}")
        
        session = OAuth2Session(Config.CLIENT_ID, redirect_uri=Config.REDIRECT_URI, scope='user:email')
        uri, state = session.create_authorization_url(Config.AUTHORIZE_URL)
        
        print(f"DEBUG: Generated OAuth URL = {uri}")
        print("*** ABOUT TO REDIRECT TO GITHUB ***")
        
        pn.state.cache['oauth_state'] = state
        return uri
    
    @staticmethod
    def fetch_user_info(code, state):
        """Exchange authorization code for user information."""
        try:
            session = OAuth2Session(Config.CLIENT_ID, Config.CLIENT_SECRET, redirect_uri=Config.REDIRECT_URI)
            token = session.fetch_token(Config.TOKEN_URL, code=code)
            session.token = token
            resp = session.get(Config.USER_API_URL)
            return resp.json()
        except Exception as e:
            print(f"OAuth error: {e}")
            return None