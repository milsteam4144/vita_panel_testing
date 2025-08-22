import os
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://172.20.134.66:5006/vita_app")
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

class GitHubAuth:
    @staticmethod
    def get_authorization_url():
        session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope='user:email')
        uri, state = session.create_authorization_url(AUTHORIZE_URL)
        return uri

    @staticmethod
    def fetch_user_info(code, state):
        try:
            session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            token = session.fetch_token(TOKEN_URL, code=code)
            session.token = token
            resp = session.get(USER_API_URL)
            return resp.json()
        except Exception as e:
            print(f"OAuth error: {e}")
            return None