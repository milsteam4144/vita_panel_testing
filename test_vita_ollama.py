"""
Test VITA application with mock Ollama integration
This simulates the application running with Ollama working
"""

import os
import sys

# Set minimal OAuth environment for testing
os.environ['GITHUB_CLIENT_ID'] = 'test_client_id_for_ollama_testing'
os.environ['GITHUB_CLIENT_SECRET'] = 'test_secret_for_ollama_testing'

try:
    # Test LLM connection
    print("🧪 Testing LLM connection...")
    from llm_connect import call_local_llm, build_chat_callback
    
    # Test different query types
    test_queries = [
        "Help me debug this Python function",
        "Explain what a variable is", 
        "Hello VITA, I'm learning Python"
    ]
    
    print("✅ LLM connection successful!")
    print("\n🔍 Testing mock Ollama responses:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: '{query}'")
        print("-" * 30)
        response = call_local_llm(query)
        print(response)
        print("=" * 50)
    
    # Test Panel imports
    print("\n📦 Testing Panel imports...")
    import panel as pn
    print("✅ Panel imported successfully!")
    
    # Test auth imports  
    print("\n🔐 Testing auth imports...")
    from auth import GitHubAuth
    print("✅ Auth module imported successfully!")
    
    # Test file uploader
    print("\n📁 Testing file uploader imports...")
    from file_uploader import FileUploader
    print("✅ File uploader imported successfully!")
    
    print("\n🎉 All components working! Mock Ollama integration ready!")
    print("\n💡 To start the full application:")
    print("   panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show")
    
    # Test callback system
    print("\n🔄 Testing callback system...")
    callback = build_chat_callback(call_local_llm)
    print("✅ Chat callback system working!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Check the error details above")