#!/usr/bin/env python3
"""Test script to verify Ollama connectivity and basic functionality"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("Testing Ollama connectivity...")
    
    try:
        # Test API endpoint
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} model(s):")
            for model in models:
                print(f"   - {model['name']}")
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to Ollama: {e}")
        return False
    
    return True

def test_llm_request():
    """Test making a request to the LLM"""
    print("\nTesting LLM request...")
    
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "qwen3:0.6b",
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "No response")
        print(f"✅ LLM Response: {answer[:100]}...")  # First 100 chars
        return True
    except Exception as e:
        print(f"❌ LLM request failed: {e}")
        return False

def test_python_code_debug():
    """Test debugging Python code with the LLM"""
    print("\nTesting Python code debugging...")
    
    code = """
def add_numbers(a, b):
    return a + b
    
result = add_numbers(5, "3")
print(result)
"""
    
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "qwen3:0.6b",
        "messages": [{"role": "user", "content": f"Debug this Python code and explain any issues:\n```python\n{code}\n```"}],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "No response")
        print(f"✅ Debug response received ({len(answer)} chars)")
        print(f"   Preview: {answer[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Debug request failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("VITA Panel - Ollama Integration Test")
    print("=" * 50)
    
    all_tests_pass = True
    
    # Run tests
    all_tests_pass &= test_ollama_connection()
    all_tests_pass &= test_llm_request()
    all_tests_pass &= test_python_code_debug()
    
    print("\n" + "=" * 50)
    if all_tests_pass:
        print("✅ All tests passed! Ollama integration is working.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 50)