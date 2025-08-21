"""
VITA - Minimal test version focusing on Ollama integration
"""

import panel as pn
from llm_connect import call_local_llm, build_chat_callback

# Load panel extension
pn.extension()

def create_minimal_test():
    """Create minimal test interface"""
    
    # Welcome message
    welcome = pn.pane.Markdown("""
    # VITA - Ollama Integration Test
    
    **Testing Mock Ollama Integration**
    
    Try these test queries:
    - "Help me debug Python code"
    - "Explain what a variable is"  
    - "Hello VITA"
    """)
    
    # Chat interface with Ollama integration
    chat_interface = pn.chat.ChatInterface(
        callback=build_chat_callback(call_local_llm),
        callback_user="User",
        height=500,
        placeholder_text="Ask me about Python programming..."
    )
    
    # Test buttons
    debug_btn = pn.widgets.Button(name="Test: Debug Query", button_type="primary")
    concept_btn = pn.widgets.Button(name="Test: Concept Query", button_type="success") 
    hello_btn = pn.widgets.Button(name="Test: Hello Query", button_type="default")
    
    def send_debug_query(event):
        chat_interface.send("Help me debug this Python function", user="Test", respond=True)
    
    def send_concept_query(event):
        chat_interface.send("Explain what a for loop is", user="Test", respond=True)
    
    def send_hello_query(event):
        chat_interface.send("Hello VITA, I'm learning Python", user="Test", respond=True)
    
    debug_btn.on_click(send_debug_query)
    concept_btn.on_click(send_concept_query)
    hello_btn.on_click(send_hello_query)
    
    # Layout
    return pn.Column(
        welcome,
        pn.Row(debug_btn, concept_btn, hello_btn),
        chat_interface,
        sizing_mode="stretch_width"
    )

# For direct testing
if __name__ == "__main__":
    print("Creating minimal VITA test app...")
    app = create_minimal_test()
    print("App created! Ready to test Ollama integration.")
    print("Run: panel serve vita_test_minimal.py --show --dev")