# panel serve oauth_test2.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev

import panel as pn
import autogen
import io
import openai
import os
import time
import asyncio
from autogen import ConversableAgent
import param
import requests
from authlib.integrations.requests_client import OAuth2Session
import urllib.parse
import base64


import base64

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

    

# GitHub OAuth Configuration
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501/oauth_test2"

# OAuth endpoints for GitHub
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

# CSS with additional styles for login
css = """
body {
    background-color: #f1b825;
    margin: 0;
    padding: 0;
}

.bk-input {
    background-color: white !important;
}
                         
.no-margin {
    margin: 0 !important;
    padding: 0 !important;
}

.code_bg {
    background: rgb(38, 50, 56);
}

.login-container {
    text-align: center;
    padding: 50px;
    background: white;
    border-radius: 10px;
    margin: 50px auto;
    max-width: 400px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: white;
    border-radius: 5px;
    margin: 5px 0;
}
"""

pn.extension(raw_css=[css])

# Global variables
test = ""
input_future = None
initiate_chat_task_created = False

class GitHubAuth:
    @staticmethod
    def get_authorization_url():
        print(f"DEBUG: CLIENT_ID = {CLIENT_ID}")
        print(f"DEBUG: REDIRECT_URI = {REDIRECT_URI}")
        session = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope='user:email')
        uri, state = session.create_authorization_url(AUTHORIZE_URL)
        print(f"DEBUG: Generated OAuth URL = {uri}")
        print("*** ABOUT TO REDIRECT TO GITHUB ***")  # Add this line
        pn.state.cache['oauth_state'] = state
        return uri
    
    @staticmethod
    def fetch_user_info(code, state):
        """Exchange code for user info"""
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

class AuthenticatedVITA(param.Parameterized):
    user_info = param.Dict(default={})
    is_logged_in = param.Boolean(default=False)
    callback_stopped = False  # Add this line
    
    def __init__(self, **params):
        super().__init__(**params)
        pn.state.add_periodic_callback(self.check_oauth_callback, period=100, count=10)
    
    def check_oauth_callback(self):
        # Stop if already processed
        if self.callback_stopped:
            return
        
        try:
            # Check for OAuth parameters
            if hasattr(pn.state, 'location') and pn.state.location and pn.state.location.search:
                search_params = pn.state.location.search
                print(f"*** OAuth callback detected: {search_params[:50]}...")
                
                # Parse URL parameters
                query_string = search_params.lstrip('?')
                params = urllib.parse.parse_qs(query_string)
                
                # Check for OAuth code
                if 'code' in params and params['code']:
                    code = params['code'][0]
                    state = params.get('state', [None])[0]
                    
                    # Exchange code for user info
                    user_info = GitHubAuth.fetch_user_info(code, state)
                    if user_info:
                        # Set login state
                        self.user_info = user_info
                        self.is_logged_in = True
                        self.callback_stopped = True
                        
                        print(f"✅ Login successful: {user_info.get('login')}")
                        
                        # update the layout directly
                        global layout
                        layout.clear()
                        layout.append(self.create_main_app())

                        return
                    else:
                        print("❌ Failed to fetch user info")
                
                elif 'error' in params:
                    print(f"❌ OAuth error: {params['error'][0]}")
                    
        except Exception as e:
            print(f"❌ Callback error: {e}")
    
    def login_view(self):
        """Login screen"""
        auth_url = GitHubAuth.get_authorization_url()
        
        # Add JavaScript to help detect OAuth callback
        callback_detector = pn.pane.HTML("""
            <script>
            // Check for OAuth parameters on page load
            window.addEventListener('load', function() {
                const urlParams = new URLSearchParams(window.location.search);
                const code = urlParams.get('code');
                if (code) {
                    console.log('OAuth callback detected by JavaScript:', code.substring(0, 10) + '...');
                    // Trigger a Panel event or refresh
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                }
            });
            </script>
        """)
        
        login_content = pn.Column(
            callback_detector,  # Add the JavaScript detector
            pn.pane.Markdown("# 🔐 Login to VITA"),
            pn.pane.Markdown("Please log in with your GitHub account to continue."),
            pn.pane.HTML(f'''
                <div class="login-container">
                    <h3>Welcome to VITA!</h3>
                    <p>Your Virtual Interactive Teaching Assistant</p>
                    <a href="{auth_url}" style="
                        display: inline-block;
                        padding: 12px 24px;
                        background-color: #24292e;
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: bold;
                        margin: 20px 0;
                    ">🔐 Login with GitHub</a>
                    <p><small>You'll be redirected to GitHub to authorize this app</small></p>
                    <div id="debug-info">
                        <p><small>Debug info:</small></p>
                        <p><small>Login status: {self.is_logged_in}</small></p>
                        <p><small>User info: {bool(self.user_info)}</small></p>
                    </div>
                </div>
            '''),
            sizing_mode='stretch_width'
        )
        return login_content
    
    def user_header(self):
        """User info header"""
        if not self.is_logged_in:
            return pn.pane.HTML("")
        
        logout_button = pn.widgets.Button(name="🚪 Logout", button_type="light")
        
        def handle_logout(event):
            self.user_info = {}
            self.is_logged_in = False
            # Force page refresh
            pn.state.location.reload = True
        
        logout_button.on_click(handle_logout)
        
        return pn.Row(
            pn.pane.HTML(f'''
                <div class="user-info">
                    <img src="{self.user_info.get('avatar_url', '')}" 
                         width="40" height="40" style="border-radius: 20px;">
                    <span><strong>{self.user_info.get('login', 'User')}</strong></span>
                </div>
            '''),
            pn.Spacer(),
            logout_button,
            sizing_mode='stretch_width'
        )
    
    def create_main_app(self):
        """Create the main VITA application"""
        # File uploader
        uploader = FileUploader()
        
        # Buttons
        debug_button = pn.widgets.Button(name='Debug the uploaded code', button_type='success')
        explain_button = pn.widgets.Button(name='See AI Examples', button_type='primary')
        open_url_button = pn.widgets.Button(name='See Instructor Examples', button_type='primary')
        toggle_button = pn.widgets.Button(name="Show/Hide Uploaded Code", button_type="primary")
        
        # Dropdown
        select = pn.widgets.Select(
            name='Programming Concepts', 
            groups={
                'Input/Output': ['Print Function', 'Get User Input'], 
                'Data Types': ['Strings', 'Integers', 'Floats', 'Formatted Strings'],
                'Mathematical Expressions': ['Add, Subtract, Multiply', 'Division', 'Exponents'],
                'Data Structures': ['Lists', 'Dictionaries'],
                'Branching': ['If/Else Statements', 'Elif Statements'],
                'Loops': ['For Loops', 'While Loops'],
                'Functions': ['Defining Functions', 'Calling Functions', 'Main Function'],
            })
        select.styles = {'background': 'white'}
        
        # Setup AutoGen with user's avatar
        chat_interface = self.setup_autogen()
        
        # Button event handlers
        def send_message(event):
            message = "Debug the uploaded code"
            if test != "":
                chat_interface.send(message, user="Student", respond=False)
                chat_interface.send(f"```python\n{test}\n```", user="Student", respond=True)
        
        def send_concept_message(event):
            message = f"Give me a brief overview of how to use {select.value} in Python"
            chat_interface.send(message, user="Student", respond=True)
        
        def open_url(event):
            import webbrowser
            safe_value = select.value.lower().replace(' ', '-')
            webbrowser.open_new_tab(f'https://milsteam4144.github.io/python.html/{safe_value}.html')
        
        debug_button.param.watch(send_message, 'clicks')
        explain_button.param.watch(send_concept_message, 'clicks')
        open_url_button.on_click(open_url)
        
        # Header with logo, title, and user info all on one line
        jpg_pane = pn.pane.Image('logo.png', width=120, height=80)

        # Create logout button
        logout_button = pn.widgets.Button(name="🚪 Logout", button_type="light")
        def handle_logout(event):
            self.user_info = {}
            self.is_logged_in = False
            global layout
            layout.clear()
            layout.append(self.login_view())
        logout_button.on_click(handle_logout)

        # Header with stacked user info/logout on left, then logo and title
        jpg_pane = pn.pane.Image('logo.png', width=120, height=80)

        # Create logout button with black border
        logout_button = pn.widgets.Button(name="🚪 Logout", button_type="light")
        logout_button.styles = {'border': '2px solid black'}

        def handle_logout(event):
            self.user_info = {}
            self.is_logged_in = False
            global layout
            layout.clear()
            layout.append(self.login_view())
        logout_button.on_click(handle_logout)

        # Stacked user info and logout button
        user_stack = pn.Column(
            pn.pane.HTML(f'''
                <div class="user-info" style="border: 2px solid black;">
                    <img src="{self.user_info.get('avatar_url', '')}" 
                        width="40" height="40" style="border-radius: 20px;">
                    <span><strong>{self.user_info.get('login', 'User')}</strong></span>
                </div>
            '''),
            logout_button,
            width=150,  # Fixed width for the stack
            margin=(5, 10, 5, 5)
        )

        # Single row header: [user stack] [logo] [title] [spacer]
        header = pn.Row(
            user_stack,
            jpg_pane,
            pn.pane.Markdown("# VITA: Virtual Interactive Teaching Assistant"),
            pn.Spacer(),
            align='center',
            margin=(10, 0, 20, 10),
            sizing_mode='stretch_width'
        )
        
        # Layout
        top_row = pn.Row(
            toggle_button, uploader.file_input, debug_button,
            pn.Spacer(sizing_mode='stretch_width'),
            select, explain_button, open_url_button,
            sizing_mode='stretch_width'
        )
        
        file_preview = pn.Row(uploader.view)
        code_snippet_column = pn.Column(file_preview, css_classes=['code_bg'], scroll=True)
        chat_column = pn.Column(chat_interface, sizing_mode='stretch_both')
        chat_column.styles = {'background': 'black'}
        
        main_row = pn.Row(code_snippet_column, pn.layout.Spacer(width=20), chat_column)
        
        def toggle_pane(event):
            if code_snippet_column.visible:
                code_snippet_column.visible = False
                toggle_button.name = "Show Code"
            else:
                code_snippet_column.visible = True
                toggle_button.name = "Hide Code"
        
        toggle_button.on_click(toggle_pane)
        
        return pn.Column(header, top_row, main_row)
    
    def setup_autogen(self):
        global input_future, initiate_chat_task_created, chat_interface

        config_list = [{
            "model": "lmstudio-community/qwen2.5-7b-instruct",
            "base_url": "http://localhost:1234/v1",
            "api_key": "lm-studio",
            "api_type": "open_ai",
        }]

        gpt4_config = {
            "config_list": config_list,
            "temperature": 0,
            "seed": 53
        }

        user_proxy = MyConversableAgent(
            name="Student",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
            system_message="""A human student learning Python. Interact with tutors to fix code errors.""",
            code_execution_config=False,
            human_input_mode="ALWAYS",
            llm_config=False,
        )

        debugger = autogen.AssistantAgent(
            name="Debugger",
            human_input_mode="NEVER",
            llm_config=gpt4_config,
            system_message="""Find and explain Python syntax errors simply in plain English.""",
        )

        corrector = autogen.AssistantAgent(
            name="Corrector",
            human_input_mode="NEVER",
            llm_config=gpt4_config,
            system_message="""Suggest simple plans to fix syntax errors without showing corrected code.""",
        )

        groupchat = autogen.GroupChat(agents=[user_proxy, debugger, corrector], messages=[], max_round=20)
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config, system_message="You are a helpful assistant that helps route questions to Debugger or Corrector.")

                # 👨‍🎓 Use emoji avatars instead of GitHub profile pics
        avatar_map = {
            user_proxy.name: "👨‍🎓",
            "User": "👨‍🎓",
            "Student": "👨‍🎓",
            debugger.name: "👩‍💻",
            corrector.name: "🛠"
        }


        def print_messages(recipient, messages, sender, config):
            content = messages[-1]['content']
            sender_name = messages[-1].get('name', sender.name if sender else 'Student')
            sender_avatar = avatar_map.get(sender_name, "👨‍🎓")
            chat_interface.send(content, user=sender_name, avatar=sender_avatar, respond=False)
            return False, None

        #user_proxy.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})
        debugger.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})
        corrector.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})

        async def delayed_initiate_chat(agent, recipient, message):
            global initiate_chat_task_created
            initiate_chat_task_created = True
            await asyncio.sleep(2)
            print("Sending to debugger:", message)
            await agent.a_send(message, debugger)


        async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
            global initiate_chat_task_created, input_future
            if not initiate_chat_task_created:
                asyncio.create_task(delayed_initiate_chat(user_proxy, manager, contents))
            else:
                if input_future and not input_future.done():
                    input_future.set_result(contents)

        # ✅ Use the actual base64 GitHub avatar here
        chat_interface = pn.chat.ChatInterface(
            callback=callback,
            user="Student",
        )

        #chat_interface.send("What would you like to ask VITA?", user="System", respond=False)
        return chat_interface

        

# File uploader class
class FileUploader(param.Parameterized):
    file_input = pn.widgets.FileInput(accept='.py', name='Upload .py file')
    file_input.styles = {'background': 'white'}
    file_content = param.String(default="No file uploaded yet")
    uploaded_content = None

    def __init__(self, **params):
        super().__init__(**params)
        self.file_input.param.watch(self.upload_file, 'value')

    @param.depends('file_content')
    def view(self):
        lines = self.file_content.split('\n')
        new_code = ""
        
        if lines[0] != 'No file uploaded yet':
            for line_index, line in enumerate(lines, start=1):
                new_code += (f"{line_index:<4} {line}\n")
        else:
            new_code = self.file_content
            
        return pn.pane.Markdown(f"```python\n{new_code}\n```", 
                               sizing_mode='stretch_both', css_classes=['no-margin'])

    def upload_file(self, event):
        global test
        if self.file_input.value:
            FileUploader.uploaded_content = self.file_input.value.decode('utf-8')
            self.file_content = FileUploader.uploaded_content
            test = FileUploader.uploaded_content

# Custom agent class
class MyConversableAgent(autogen.ConversableAgent):
    async def a_get_human_input(self, prompt: str) -> str:
        global input_future, chat_interface
        chat_interface.send(prompt, user="System", respond=False)
        if input_future is None or input_future.done():
            input_future = asyncio.Future()
        await input_future
        input_value = input_future.result()
        input_future = None
        return input_value

# Set up environment
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Create the app instance
app = AuthenticatedVITA()

# Create layout - always start with login view
layout = pn.Column(app.login_view())
layout.servable()