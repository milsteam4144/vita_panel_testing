"""
VITA - Simplified test version with OAuth stubbed out
Focus: Test Ollama integration without OAuth complexity
"""

import panel as pn
import param
from llm_connect import call_local_llm, build_chat_callback
from file_uploader import FileUploader

# Load panel extension and basic config
pn.extension()

class VITATestApp(param.Parameterized):
    """Simplified VITA app without OAuth for testing"""
    
    def __init__(self, **params):
        super().__init__(**params)
        self.file_uploader = FileUploader()
    
    def create_app(self):
        """Create the main application interface"""
        
        # Welcome message
        welcome = pn.pane.Markdown("""
        # VITA - Test Mode (OAuth Stubbed)
        ## Testing Ollama Integration
        
        **Available Features:**
        - Upload Python files for debugging
        - Ask programming questions
        - Get concept explanations
        
        *Note: This is a test version with OAuth authentication disabled*
        """)
        
        # File uploader section
        upload_section = pn.Column(
            pn.pane.Markdown("### Upload Python File"),
            self.file_uploader.file_input,
            self.file_uploader.view,
            margin=(10, 10)
        )
        
        # Debug button
        debug_button = pn.widgets.Button(
            name="Debug Uploaded Code", 
            button_type="primary",
            margin=(10, 10)
        )
        debug_button.on_click(self.debug_uploaded_file)
        
        # Concept explanation button  
        concept_button = pn.widgets.Button(
            name="Explain Programming Concepts",
            button_type="success", 
            margin=(10, 10)
        )
        concept_button.on_click(self.explain_concepts)
        
        # Chat interface
        chat_interface = pn.chat.ChatInterface(
            callback=build_chat_callback(call_local_llm),
            callback_user="User",
            height=400,
            margin=(10, 10)
        )
        
        # Test queries section
        test_section = pn.Column(
            pn.pane.Markdown("### Quick Test Queries"),
            pn.widgets.Button(name="Test: Debug Query", button_type="outline"),
            pn.widgets.Button(name="Test: Concept Query", button_type="outline"),
            pn.widgets.Button(name="Test: General Query", button_type="outline"),
            margin=(10, 10)
        )
        
        # Wire up test buttons
        test_section[1].on_click(lambda event: self.send_test_query(chat_interface, "Help me debug this Python function"))
        test_section[2].on_click(lambda event: self.send_test_query(chat_interface, "Explain what a for loop is"))
        test_section[3].on_click(lambda event: self.send_test_query(chat_interface, "Hello VITA, I'm learning Python"))
        
        # Layout
        return pn.template.FastListTemplate(
            title="VITA Test - Ollama Integration",
            sidebar=[upload_section, debug_button, concept_button, test_section],
            main=[welcome, chat_interface],
            header_background='#2596be',
        )
    
    def debug_uploaded_file(self, event):
        """Handle debug button click"""
        if self.file_uploader.uploaded_content:
            # Send uploaded code to LLM for debugging
            debug_prompt = f"Please debug this Python code:\n\n```python\n{self.file_uploader.uploaded_content}\n```"
            response = call_local_llm(debug_prompt)
            print("Debug response:", response[:100], "...")
        else:
            print("No file uploaded yet")
    
    def explain_concepts(self, event):
        """Handle concept explanation button"""
        response = call_local_llm("Explain basic Python programming concepts")
        print("Concept response:", response[:100], "...")
    
    def send_test_query(self, chat_interface, query):
        """Send a test query to the chat"""
        chat_interface.send(query, user="TestUser", respond=True)

# Create and serve the app
def create_test_app():
    app = VITATestApp()
    return app.create_app()

if __name__ == "__main__":
    # For testing
    print("Creating VITA test app...")
    test_app = create_test_app()
    print("Test app created successfully!")
    print("Run with: panel serve vita_test_simple.py --show")