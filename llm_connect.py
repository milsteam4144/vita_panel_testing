
import requests

def call_local_llm(user_input: str) -> str:
    """
    Call Ollama API for local LLM inference
    Ollama must be running on localhost:11434
    """
    url = "http://localhost:11434/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama2",  # Default model - can be configured
        "stream": False,
        "messages": [{"role": "user", "content": user_input}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "❌ Ollama not running. Please start Ollama service on localhost:11434"
    except requests.exceptions.Timeout:
        return "⏱️ Ollama request timed out. Try again or check model availability."
    except Exception as e:
        return f"⚠️ Error from Ollama: {e}"

def build_chat_callback(llm_function):
    import asyncio
    async def callback(user_input, user, instance):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, llm_function, user_input)
        instance.send(response, user="VITA", avatar="🧠", respond=False)
    return callback