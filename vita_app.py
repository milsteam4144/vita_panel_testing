'''
VITA
'''


import panel as pn
import io
import os
import time
import asyncio
import param
import urllib.parse
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

from llm_connect import call_local_llm, build_chat_callback
from auth import GitHubAuth
from file_uploader import FileUploader



# Load panel extension and custom CSS from local file styles.css
pn.extension()
with open("user_interface/styles.css") as f:
    pn.config.raw_css.append(f.read())


# Global variables
test = ""
input_future = None
initiate_chat_task_created = False


# Import the enhanced RAG backend
try:
    from rag_backend_enhanced import EnhancedRAGBackend
    USE_ENHANCED_RAG = True
except ImportError:
    print("Warning: Enhanced RAG backend not available, falling back to original")
    USE_ENHANCED_RAG = False

# Keep original RAG backend for fallback
class RAGBackend:
    def __init__(self, data_path="data/dummy_data.json", embedding_model='all-MiniLM-L6-v2'):
        # Load data
        with open(data_path) as f:
            self.data = json.load(f)
        # Prepare model and embeddings
        self.model = SentenceTransformer(embedding_model)
        self.texts = [d['student_question'] + " " + d['code_snippet'] for d in self.data]
        self.embeddings = self.model.encode(self.texts, convert_to_numpy=True)
        # Build FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def query(self, question, k=1):
        """Return the best-matching data entries for the question."""
        user_emb = self.model.encode([question], convert_to_numpy=True)
        D, I = self.index.search(user_emb, k)
        results = []
        for idx in I[0]:
            match = self.data[idx]
            results.append({
                "answer": match['teacher_response'],
                "matched_assignment": match.get('assignment_id', None),
                "matched_code": match.get('code_snippet', None),
                "student_question": match.get('student_question', None)
            })
        return results


# Initialize RAG backend
try:
    print("Initializing RAG backend...")
    if USE_ENHANCED_RAG:
        rag_backend = EnhancedRAGBackend()
        print("Enhanced RAG backend initialized successfully!")
    else:
        rag_backend = RAGBackend()
        print("Original RAG backend initialized successfully!")
except Exception as e:
    print(f"Warning: RAG backend initialization failed: {e}")
    rag_backend = None


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
        
        # Setup local chat interface
        chat_interface = self.setup_local_chat()

        
        # Button event handlers
        def send_message(event):
            message = "Debug the uploaded code"
            if test != "":
                chat_interface.send(message, respond=False)
                chat_interface.send(f"```python\n{test}\n```", respond=True)
        
        def send_concept_message(event):
            message = f"Give me a brief overview of how to use {select.value} in Python"
            chat_interface.send(message, respond=True)
        
        def open_url(event):
            import webbrowser
            safe_value = select.value.lower().replace(' ', '-')
            webbrowser.open_new_tab(f'https://milsteam4144.github.io/python.html/{safe_value}.html')
        
        debug_button.param.watch(send_message, 'clicks')
        explain_button.param.watch(send_concept_message, 'clicks')
        open_url_button.on_click(open_url)
        

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
        jpg_pane = pn.pane.Image('user_interface/logo.png', width=120, height=80)

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
        chat_column = pn.Column(
            chat_interface,
            styles={
                'background': 'black',
                'overflowY': 'auto',
                'maxHeight': '80vh',  # Adjust height as needed
                'padding': '10px',
            },
            sizing_mode='stretch_both',
        )

        # Main layout with code snippet and chat side by side
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
    
    def setup_local_chat(self):
        # Create custom callback that uses RAG
        async def rag_enhanced_callback(user_input, user, instance):
            try:
                rag_results = []
                sources_used = []
                
                # Check if RAG backend is available
                if rag_backend is not None:
                    # First, check for common misconceptions
                    misconceptions = [
                        ("if else loop", "I notice you mentioned 'if else loop' - but there's no such thing! These are actually two separate concepts:\n\n• **IF statements** - make decisions (like choosing what to wear based on weather)\n• **LOOPS** - repeat actions (like counting from 1 to 10)\n\nWhat would you like to learn about - making decisions with IF statements, or repeating actions with loops?"),
                        ("for loop if", "I see you're mixing 'for loop' and 'if' - these are different concepts! Would you like to learn about FOR loops (which repeat actions) or IF statements (which make decisions)?"),
                        ("while if", "It looks like you're combining 'while' and 'if' concepts. Would you like to learn about WHILE loops (repeating until something changes) or IF statements (making one-time decisions)?")
                    ]
                    
                    user_input_lower = user_input.lower()
                    for misconception, correction in misconceptions:
                        if misconception in user_input_lower:
                            instance.send(correction, user="VITA", avatar="🧠", respond=False)
                            return
                    
                    # Expand mathematical symbols for better RAG matching
                    expanded_query = user_input
                    symbol_expansions = {
                        "//": "floor division operator double slash",
                        "/": "division operator slash",
                        "%": "modulo remainder operator percent",
                        "*": "multiplication operator asterisk",
                        "+": "addition operator plus",
                        "-": "subtraction operator minus",
                        "=": "assignment operator equals",
                        "==": "equality comparison operator",
                        "!=": "not equal comparison operator"
                    }
                    
                    for symbol, expansion in symbol_expansions.items():
                        if symbol in user_input:
                            expanded_query = f"{user_input} {expansion}"
                            break
                    
                    # Get relevant context from RAG backend
                    rag_results = rag_backend.query(expanded_query, k=3)  # Get top 3 matches
                    
                    # Debug: Print what context was found
                    print(f"🔍 RAG Query: {expanded_query}")
                    for i, result in enumerate(rag_results):
                        # Handle both enhanced and original RAG result formats
                        if 'source_file' in result:
                            distance = result.get('distance', 'N/A')
                            print(f"📄 Match {i+1}: {result['source_file']} (distance: {distance}, type: {result.get('chunk_type', 'unknown')})")
                        else:
                            # Original format
                            print(f"📄 Match {i+1}: {result.get('matched_assignment', 'N/A')} | Code: {str(result.get('matched_code', ''))[:50]}...")
                    
                    # Filter results for relevance (only show sources if distance < 1.2 for enhanced RAG)
                    relevant_results = []
                    for result in rag_results:
                        distance = result.get('distance', 0)
                        if distance is None or distance < 1.2:  # Consider relevant if distance is low
                            relevant_results.append(result)
                        elif result.get('source_type') == 'fallback_data':  # Always include fallback data
                            relevant_results.append(result)
                    
                    if relevant_results:
                        # Build enhanced prompt with context
                        context_parts = []
                        for i, result in enumerate(relevant_results):
                            # Handle both enhanced and original RAG result formats
                            if 'source_file' in result:
                                # Enhanced format
                                context_parts.append(f"""
Context {i+1} (from {result['source_file']}):
{result['answer']}
""")
                            else:
                                # Original format
                                context_parts.append(f"""
Context {i+1}:
Student Question: {result.get('student_question', '')}
Code: {result.get('matched_code', '')}
Teacher Response: {result.get('answer', '')}
""")
                        
                        context_text = "\n".join(context_parts)
                        
                        enhanced_prompt = f"""You are VITA, a virtual teaching assistant helping students discover answers through questions. DO NOT give direct tutorials or explanations.

Educational content:
{context_text}

Student question: "{user_input}"

Instead of explaining directly, help the student discover the answer by:
1. Asking guiding questions that lead them to think
2. Giving hints rather than answers
3. Using analogies from everyday life
4. Encouraging them to try things and see what happens

Example approach: "That's a great question! Before we dive in, let me ask you - what do you think happens when you need to make a choice in everyday life, like deciding whether to bring an umbrella? How is that different from doing the same action over and over, like brushing each tooth?"

Be encouraging and use simple language."""
                        
                        # Update sources_used with only relevant results
                        sources_used = []
                        for result in relevant_results:
                            if 'source_file' in result:
                                sources_used.append({
                                    'file': result['source_file'],
                                    'preview': result.get('content_preview', result.get('answer', '')[:100] + '...'),
                                    'type': result.get('chunk_type', 'unknown')
                                })
                            else:
                                sources_used.append({
                                    'file': 'data/dummy_data.json',
                                    'preview': result.get('answer', '')[:100] + '...',
                                    'type': 'fallback_qa'
                                })
                    else:
                        # No relevant content found - provide Python-focused response
                        enhanced_prompt = f"""You are VITA, a virtual teaching assistant for CTI-110 Python programming. A student asked: "{user_input}"

Since I don't have specific educational content about this topic, help the student discover the answer by:
1. Asking guiding questions about Python programming concepts
2. Encouraging them to experiment with Python code
3. Using simple analogies to explain programming concepts
4. Focusing on Python basics like operators, data types, loops, conditionals, and functions

Be encouraging and suggest they try things in Python to see what happens. Always keep responses focused on Python programming for beginners."""
                else:
                    enhanced_prompt = user_input
                
                # Send to LLM with enhanced prompt
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, call_local_llm, enhanced_prompt)
                instance.send(response, user="VITA", avatar="🧠", respond=False)
                
                # Add sources used display if any were found
                if sources_used:
                    sources_text = "**📚 Sources Used:**\n"
                    for i, source in enumerate(sources_used, 1):
                        sources_text += f"{i}. **{source['file']}** ({source['type']})\n"
                        sources_text += f"   _{source['preview']}_\n\n"
                    
                    instance.send(sources_text, user="System", avatar="📚", respond=False)
                
            except Exception as e:
                # Fallback to regular LLM call if RAG fails
                print(f"RAG error: {e}")
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, call_local_llm, user_input)
                instance.send(response, user="VITA", avatar="🧠", respond=False)

        # Create the chat interface
        chat = pn.chat.ChatInterface(
            callback=rag_enhanced_callback,
            user="Student",
            show_rerun=False,
            show_undo=False,
            show_clear=True,
        )
        
        welcome_message = "👋 Welcome! Ask me anything about Python or your CTI-110 course."
        if rag_backend is not None:
            welcome_message += " I have access to examples and documentation from your instructor."
        else:
            welcome_message += " (Note: Enhanced context features are currently unavailable)"
            
        chat.send(welcome_message, user="System", respond=False)
        return chat


# Set up environment
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Create the app instance
app = AuthenticatedVITA()

# Create layout - always start with login view
layout = pn.Column(app.login_view())
layout.servable()