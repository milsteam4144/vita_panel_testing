"""
Simple VITA app without authentication - for testing RAG functionality
"""

import panel as pn
import os
import asyncio
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Import existing modules (except auth)
from llm_connect import call_local_llm
from file_uploader import FileUploader

# Load panel extension and custom CSS
pn.extension()
with open("user_interface/styles.css") as f:
    pn.config.raw_css.append(f.read())

# Global variables
test = ""

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

# Import the enhanced RAG backend
try:
    from rag_backend_enhanced import EnhancedRAGBackend
    USE_ENHANCED_RAG = True
except ImportError:
    print("Warning: Enhanced RAG backend not available, falling back to original")
    USE_ENHANCED_RAG = False

# Initialize RAG backend
try:
    print("🔍 Initializing RAG backend...")
    if USE_ENHANCED_RAG:
        rag_backend = EnhancedRAGBackend()
        print("✅ Enhanced RAG backend initialized successfully!")
    else:
        rag_backend = RAGBackend()
        print("✅ Basic RAG backend initialized successfully!")
except Exception as e:
    print(f"⚠️ RAG backend initialization failed: {e}")
    rag_backend = None

def setup_local_chat():
    # Create custom callback that uses RAG
    async def rag_enhanced_callback(user_input, user, instance):
        try:
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
                
                # Question is valid, proceed with RAG
                rag_results = rag_backend.query(user_input, k=2)  # Get top 2 matches
                
                # Debug: Print what context was found
                print(f"🔍 RAG Query: {user_input}")
                for i, result in enumerate(rag_results):
                    if hasattr(result, 'get') and result.get('source_file'):
                        # Enhanced RAG format
                        print(f"📄 Match {i+1}: {result['source_file']} | Content: {result['answer'][:50]}...")
                    elif hasattr(result, 'get') and result.get('matched_assignment'):
                        # Basic RAG format  
                        print(f"📄 Match {i+1}: {result['matched_assignment']} | Code: {result['matched_code'][:50]}...")
                
                # Build enhanced prompt with context
                context_parts = []
                document_sources = []
                for result in rag_results:
                    # Handle both enhanced and basic RAG result formats
                    if hasattr(result, 'get') and result.get('source_file'):
                        # Enhanced RAG format
                        document_sources.append(result['source_file'])
                        context_parts.append(f"Content: {result['answer']}")  # Enhanced backend uses 'answer' field
                    elif hasattr(result, 'get') and result.get('matched_assignment'):
                        # Basic RAG format
                        document_sources.append(result['matched_assignment'])
                        context_parts.append(f"Question: {result['student_question']}\nCode: {result['matched_code']}\nAnswer: {result['answer']}")
                
                context_text = "\n\n".join(context_parts)
                
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
                
                # Send to LLM with enhanced prompt
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, call_local_llm, enhanced_prompt)
                
                # Add document attribution if sources were found
                if document_sources:
                    unique_sources = list(set(document_sources))  # Remove duplicates
                    if len(unique_sources) == 1:
                        response += f"\n\n{unique_sources[0]} was considered relevant and used to generate this response."
                    else:
                        sources_text = ", ".join(unique_sources)
                        response += f"\n\n{sources_text} were considered relevant and used to generate this response."
                
                instance.send(response, user="VITA", avatar="🧠", respond=False)
            else:
                # RAG not available, use regular LLM call
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, call_local_llm, user_input)
                instance.send(response, user="VITA", avatar="🧠", respond=False)
            
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

def create_main_app():
    """Create the main VITA application without authentication"""
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
    
    # Setup chat interface
    chat_interface = setup_local_chat()
    
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
    
    # Header
    jpg_pane = pn.pane.Image('user_interface/logo.png', width=120, height=80)
    header = pn.Row(
        jpg_pane,
        pn.pane.Markdown("# VITA: Virtual Interactive Teaching Assistant (Test Mode)"),
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
            'maxHeight': '80vh',
            'padding': '10px',
        },
        sizing_mode='stretch_both',
    )

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

# Set up environment
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Create layout - simplified without authentication
layout = pn.Column(create_main_app())
layout.servable()
