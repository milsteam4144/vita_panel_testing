"""
VITA Core Logic - UI-agnostic agent orchestration
Extracted from test.py for reusability in console and Panel versions
"""
import os
import asyncio
import autogen
from typing import Optional, Callable, List, Dict, Any

class VitaCore:
    """Core VITA functionality without UI dependencies"""
    
    def __init__(self, message_callback: Optional[Callable] = None):
        """
        Initialize VITA core
        
        Args:
            message_callback: Function to call when agents send messages
                            Signature: callback(sender_name: str, content: str, avatar: str)
        """
        self.message_callback = message_callback or self._default_message_callback
        self.conversation_active = False
        self.uploaded_file_content = ""
        
        # Setup agents
        self._setup_configuration()
        self._setup_agents()
        
    def _setup_configuration(self):
        """Setup model configuration based on environment"""
        use_local = os.environ.get("USE_LOCAL_MODEL", "true").lower() == "true"
        
        if use_local:
            self.config_list = [{
                'model': os.environ.get("LOCAL_MODEL_NAME", "dolphin-2.1-mistral-7b"),
                'base_url': os.environ.get("LOCAL_MODEL_URL", "http://localhost:1234/v1"),
                'api_key': "lm-studio",
            }]
        else:
            self.config_list = [{
                'model': 'gpt-4o',
                'api_key': os.environ.get("OPENAI_API_KEY"),
            }]
            
        self.llm_config = {
            "config_list": self.config_list, 
            "temperature": 0, 
            "seed": 53
        }
        
    def _setup_agents(self):
        """Setup AutoGen agents"""
        
        # Custom agent for human input handling
        class VitaConversableAgent(autogen.ConversableAgent):
            def __init__(self, vita_core, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.vita_core = vita_core
                
            async def a_get_human_input(self, prompt: str) -> str:
                return await self.vita_core._get_human_input(prompt)
        
        # Student agent (human proxy)
        self.user_proxy = VitaConversableAgent(
            self,
            name="Student",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
            system_message="""A human student that is learning to code in Python. Interact with the corrector to discuss the plan to fix any errors in the code. 
The plan to fix the errors in the code needs to be approved by this admin.""",
            code_execution_config=False,
            human_input_mode="ALWAYS",
        )
        
        # Debugger agent
        self.debugger = autogen.AssistantAgent(
            name="Debugger",
            human_input_mode="NEVER",
            llm_config=self.llm_config,
            system_message="""Debugger. You inspect Python code. You find any syntax errors in the code. 
You explain each error as simply as possible in plain English and what line the error occurs on. 
You don't write code. You never show the corrected code.""",
        )
        
        # Corrector agent  
        self.corrector = autogen.AssistantAgent(
            name="Corrector",
            human_input_mode="NEVER",
            system_message="""Corrector. Suggest a plan to fix each syntax error. 
Explain how to correct the error as simply as possible using non-technical jargon. 
You never show the corrected code. However, you may show an example of similar code. Any code that you 
provide must not be the corrected code to the code you were given. It can only be examples of the same 
concept, but must use different content as to not give the student the corrected version of their code.
Revise the plan based on feedback from Student until Student agrees that the correction has 
successfully fixed their code. If Student does not agree that the correction is sufficient,
work with the Student to suggest a different solution.""",
            llm_config=self.llm_config,
        )
        
        # Group chat setup
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.debugger, self.corrector], 
            messages=[], 
            max_round=20
        )
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat, 
            llm_config=self.llm_config
        )
        
        # Register message callbacks
        self._register_message_handlers()
        
    def _register_message_handlers(self):
        """Register message handling for all agents"""
        avatars = {
            "Student": "👨‍💼", 
            "Debugger": "👩‍💻", 
            "Corrector": "🛠"
        }
        
        def message_handler(recipient, messages, sender, config):
            if not messages:
                return False, None
                
            content = messages[-1].get('content', '')
            
            # Issue #001 Fix: Filter empty messages
            if not content or content.isspace():
                print(f"[DEBUG] Skipping empty message from {sender.name}")
                return False, None
                
            sender_name = messages[-1].get('name', sender.name)
            avatar = avatars.get(sender_name, "🤖")
            
            # Don't echo Student messages
            if sender_name != "Student":
                self.message_callback(sender_name, content, avatar)
                
            return False, None
        
        # Register for all agents
        for agent in [self.user_proxy, self.debugger, self.corrector]:
            agent.register_reply([autogen.Agent, None], reply_func=message_handler, config={"callback": None})
    
    def _default_message_callback(self, sender_name: str, content: str, avatar: str):
        """Default message callback - just print to console"""
        print(f"\n{avatar} {sender_name}:")
        print(content)
        print("-" * 50)
    
    async def _get_human_input(self, prompt: str) -> str:
        """Handle human input requests from agents"""
        print(f"\n🤔 {prompt}")
        # In console mode, this will be overridden
        # In Panel mode, this will use the async input system
        return "Approved"  # Default response
    
    def process_file(self, file_content: str) -> str:
        """Process uploaded file content and add line numbers"""
        if not file_content or file_content.isspace():
            return "No file content provided"
            
        lines = file_content.split('\n')
        numbered_lines = []
        
        for line_index, line in enumerate(lines, start=1):
            numbered_lines.append(f"{line_index:<4} {line}")
            
        self.uploaded_file_content = file_content
        return '\n'.join(numbered_lines)
    
    async def start_debug_session(self, file_content: str) -> bool:
        """
        Start a debugging session with the provided code
        
        Returns:
            bool: True if session started successfully, False if error
        """
        if self.conversation_active:
            self.message_callback("System", "⚠️ Please wait for the current conversation to complete.", "⚠️")
            return False
            
        if not file_content or file_content.isspace():
            self.message_callback("System", "⚠️ Please provide some code to debug.", "⚠️")
            return False
            
        self.conversation_active = True
        
        try:
            # Format the code for debugging
            code_block = f"```python\n{file_content}\n```"
            
            # Start the conversation
            await self.user_proxy.a_initiate_chat(
                self.manager, 
                message=code_block
            )
            
            return True
            
        except Exception as e:
            print(f"Error connecting to AI service: {e}")
            self.message_callback("System", "⚠️ AI service temporarily unavailable. Please ensure LM Studio is running and try again.", "⚠️")
            return False
        finally:
            self.conversation_active = False
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_active = False
        self.groupchat.messages = []
        self.uploaded_file_content = ""