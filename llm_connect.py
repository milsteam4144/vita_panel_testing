
import requests
import os

def call_local_llm(user_input: str) -> str:
    # Check which LLM backend to use (default to LM Studio for backward compatibility)
    llm_backend = os.getenv("LLM_BACKEND", "lm-studio").lower()
    
    if llm_backend == "ollama":
        # Ollama API configuration
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
        model = os.getenv("OLLAMA_MODEL", "tinyllama")
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": user_input}],
            "stream": False
        }
    else:
        # LM Studio API configuration (default)
        url = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer lm-studio"
        }
        payload = {
            "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "stream": False,
            "messages": [{"role": "user", "content": user_input}]
        }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=500)
        response.raise_for_status()
        data = response.json()
        
        if llm_backend == "ollama":
            # Ollama returns the response in a different format
            return data["message"]["content"]
        else:
            # LM Studio format
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error from LLM ({llm_backend}): {e}"

def build_chat_callback(llm_function):
    import asyncio
    async def callback(user_input, user, instance):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, llm_function, user_input)
        instance.send(response, user="VITA", avatar="🧠", respond=False)
    return callback