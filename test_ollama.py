#!/usr/bin/env python3
"""
Test script for Ollama integration with VITA.
Run this to verify Ollama is working correctly before starting VITA.
"""

import os
import sys
from llm_connect import call_local_llm

def test_ollama():
    print("🧪 Testing Ollama integration...")
    
    # Check if Ollama backend is configured
    backend = os.getenv("LLM_BACKEND", "lm-studio")
    print(f"   LLM Backend: {backend}")
    
    if backend == "ollama":
        model = os.getenv("OLLAMA_MODEL", "tinyllama")
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
        print(f"   Ollama Model: {model}")
        print(f"   Ollama URL: {url}")
    else:
        print("   ⚠️  LLM_BACKEND is not set to 'ollama'")
        print("   To test Ollama, run:")
        print("   export LLM_BACKEND=ollama")
        print("   export OLLAMA_MODEL=tinyllama")
        return
    
    # Test the connection
    print("\n📡 Testing LLM connection...")
    test_prompt = "Hello! Please respond with a short greeting."
    
    try:
        response = call_local_llm(test_prompt)
        print(f"\n✅ Success! LLM Response:\n{response}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Ollama is installed: curl -fsSL https://ollama.com/install.sh | sh")
        print("2. Ensure Ollama is running: ollama serve")
        print("3. Ensure model is pulled: ollama pull tinyllama")
        print("4. Check if Ollama is listening: curl http://localhost:11434/api/tags")
        sys.exit(1)

if __name__ == "__main__":
    test_ollama()