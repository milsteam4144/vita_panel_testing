"""Chat agents and AutoGen configuration for VITA Panel application."""

import os
import asyncio
import autogen

# Set up environment
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Global variables for chat interface communication
input_future = None
chat_interface = None


class MyConversableAgent(autogen.ConversableAgent):
    """Custom ConversableAgent that integrates with Panel chat interface."""
    
    async def a_get_human_input(self, prompt: str) -> str:
        """Get human input through the Panel chat interface."""
        global input_future, chat_interface
        chat_interface.send(prompt, user="System", respond=False)
        if input_future is None or input_future.done():
            input_future = asyncio.Future()
        await input_future
        input_value = input_future.result()
        input_future = None
        return input_value


def set_chat_interface(interface):
    """Set the global chat interface for agent communication."""
    global chat_interface
    chat_interface = interface


def set_input_future(future):
    """Set the global input future for agent communication."""
    global input_future
    input_future = future


def get_input_future():
    """Get the current input future."""
    return input_future