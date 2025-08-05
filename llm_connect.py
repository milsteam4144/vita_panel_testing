
import requests

def call_local_llm(user_input: str) -> str:
    url = "http://localhost:11434/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen3:0.6b",  # Using qwen3:0.6b model
        "messages": [{"role": "user", "content": user_input}],
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=500)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except Exception as e:
        return f"⚠️ Error from LLM: {e}"

def build_chat_callback(llm_function):
    import asyncio
    async def callback(user_input, user, instance):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, llm_function, user_input)
        instance.send(response, user="VITA", avatar="🧠", respond=False)
    return callback
