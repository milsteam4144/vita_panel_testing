"""GitHub OAuth authentication module for VITA Panel application."""

import os
import base64
import requests
import panel as pn
from authlib.integrations.requests_client import OAuth2Session

# GitHub OAuth Configuration
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501/oauth_test2"

# OAuth endpoints for GitHub
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"


def fetch_avatar_as_base64(url):
    """Convert GitHub avatar URL to base64-encoded image string."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        b64 = base64.b64encode(response.content).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"⚠️ Failed to fetch avatar as base64: {e}")
        return "👨‍🎓"  # fallback emoji


class GitHubAuth:
    """Handles GitHub OAuth authentication operations."""
    
    @staticmethod
    def get_authorization_url():
        """Generate GitHub OAuth authorization URL."""
        print(f"DEBUG: CLIENT_ID = {CLIENT_ID}")
        print(f"DEBUG: REDIRECT_URI = {REDIRECT_URI}")
        session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope='user:email')
        uri, state = session.create_authorization_url(AUTHORIZE_URL)
        print(f"DEBUG: Generated OAuth URL = {uri}")
        print("*** ABOUT TO REDIRECT TO GITHUB ***")
        pn.state.cache['oauth_state'] = state
        return uri
    
    @staticmethod
    def fetch_user_info(code, state):
        """Exchange code for user info."""
        try:
            session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            token = session.fetch_token(TOKEN_URL, code=code)
            session.token = token
            resp = session.get(USER_API_URL)
            return resp.json()
            print("✅ Full GitHub user info:", resp.json())

        except Exception as e:
            print(f"OAuth error: {e}")
            return None