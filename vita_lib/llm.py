"""
LLM communication module for VITA application.

Handles communication with local LLM services.
"""

import asyncio
import requests


def call_local_llm(user_input: str) -> str:
    """
    Sends a non-streaming request to the local LM Studio server and returns the full response.
    
    Args:
        user_input: The user's input message
        
    Returns:
        The LLM's response text
    """
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lm-studio"
    }
    payload = {
        "model": "mistral-7b-instruct-v0.2",  # Adjust model if needed
        "stream": False,
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Error from LLM: {e}"


def build_chat_callback(llm_function):
    """
    Returns an async callback for use in a Panel ChatInterface, using the given LLM call function.
    
    Args:
        llm_function: The function to call for LLM responses
        
    Returns:
        An async callback function for Panel ChatInterface
    """
    async def callback(user_input, user, instance):
        # Let ChatInterface handle the user message (we won't send it manually)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, llm_function, user_input)
        instance.send(response, user="VITA", avatar="🧠", respond=False)

    return callback