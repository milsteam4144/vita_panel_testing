"""
Simple test of VITA LLM integration
"""

def mock_ollama_response(user_input: str) -> str:
    """Simple mock that avoids Unicode issues on Windows"""
    
    if "debug" in user_input.lower():
        return "I can help debug your Python code! Please share the code and I'll analyze it for errors."
    elif "concept" in user_input.lower() or "explain" in user_input.lower():
        return "I'd be happy to explain programming concepts! What would you like to learn about?"
    else:
        return f"Hello! I'm VITA. You asked: '{user_input}' - How can I help you with Python programming?"

# Test the function
if __name__ == "__main__":
    print("Testing simple mock responses...")
    
    test_cases = [
        "Help me debug this function",
        "Explain what a loop is", 
        "Hello VITA"
    ]
    
    for test in test_cases:
        print(f"\nInput: {test}")
        print(f"Output: {mock_ollama_response(test)}")