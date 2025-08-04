'''
VITA
'''


import panel as pn
import io
import os
import time
import asyncio
import param
import json

from llm_connect import call_local_llm, build_chat_callback
from file_uploader import FileUploader


# Load panel extension and custom CSS from local file styles.css
pn.extension()
with open("user_interface/styles.css") as f:
    pn.config.raw_css.append(f.read())


# Global variables
test = ""
input_future = None
initiate_chat_task_created = False


class VITAApp(param.Parameterized):

    def __init__(self, **params):
        super().__init__(**params)
    
    def user_header(self):
        """User info header - now empty since no login"""
        return pn.pane.HTML("")

    def create_main_app(self):
        """Create the main VITA application"""
        # File uploader
        uploader = FileUploader()
        
        # Buttons
        debug_button = pn.widgets.Button(name='Debug the uploaded code', button_type='success')
        explain_button = pn.widgets.Button(name='See AI Examples', button_type='primary')
        open_url_button = pn.widgets.Button(name='See Instructor Examples', button_type='primary')
        toggle_button = pn.widgets.Button(name="Show/Hide Uploaded Code", button_type="primary")
        
        # Dropdown
        select = pn.widgets.Select(
            name='Programming Concepts', 
            groups={
                'Input/Output': ['Print Function', 'Get User Input'], 
                'Data Types': ['Strings', 'Integers', 'Floats', 'Formatted Strings'],
                'Mathematical Expressions': ['Add, Subtract, Multiply', 'Division', 'Exponents'],
                'Data Structures': ['Lists', 'Dictionaries'],
                'Branching': ['If/Else Statements', 'Elif Statements'],
                'Loops': ['For Loops', 'While Loops'],
                'Functions': ['Defining Functions', 'Calling Functions', 'Main Function'],
            })
        select.styles = {'background': 'white'}
        
        # Setup local chat interface
        chat_interface = self.setup_local_chat()

        
        # Button event handlers
        def send_message(event):
            message = "Debug the uploaded code"
            if test != "":
                chat_interface.send(message, respond=False)
                chat_interface.send(f"```python\n{test}\n```", respond=True)
        
        def send_concept_message(event):
            message = f"Give me a brief overview of how to use {select.value} in Python"
            chat_interface.send(message, respond=True)
        
        def open_url(event):
            import webbrowser
            safe_value = select.value.lower().replace(' ', '-')
            webbrowser.open_new_tab(f'https://milsteam4144.github.io/python.html/{safe_value}.html')
        
        debug_button.param.watch(send_message, 'clicks')
        explain_button.param.watch(send_concept_message, 'clicks')
        open_url_button.on_click(open_url)

        # Header with just logo and title (no user info / logout)
        jpg_pane = pn.pane.Image('user_interface/logo.png', width=120, height=80)

        header = pn.Row(
            jpg_pane,
            pn.pane.Markdown("# VITA: Virtual Interactive Teaching Assistant"),
            pn.Spacer(),
            align='center',
            margin=(10, 0, 20, 10),
            sizing_mode='stretch_width'
        )
        
        # Layout
        top_row = pn.Row(
            toggle_button, uploader.file_input, debug_button,
            pn.Spacer(sizing_mode='stretch_width'),
            select, explain_button, open_url_button,
            sizing_mode='stretch_width'
        )
        
        file_preview = pn.Row(uploader.view)
        code_snippet_column = pn.Column(file_preview, css_classes=['code_bg'], scroll=True)
        chat_column = pn.Column(
            chat_interface,
            styles={
                'background': 'black',
                'overflowY': 'auto',
                'maxHeight': '80vh',  # Adjust height as needed
                'padding': '10px',
            },
            sizing_mode='stretch_both',
        )

        # Main layout with code snippet and chat side by side
        main_row = pn.Row(code_snippet_column, pn.layout.Spacer(width=20), chat_column)
        
        def toggle_pane(event):
            if code_snippet_column.visible:
                code_snippet_column.visible = False
                toggle_button.name = "Show Code"
            else:
                code_snippet_column.visible = True
                toggle_button.name = "Hide Code"
        
        toggle_button.on_click(toggle_pane)
        
        return pn.Column(header, top_row, main_row)
    
    def setup_local_chat(self):
        callback = build_chat_callback(call_local_llm)

        # Create the chat interface
        chat = pn.chat.ChatInterface(
            callback=callback,
            user="Student",
            show_rerun=False,
            show_undo=False,
            show_clear=True,
        )
        chat.send("👋 Welcome! Ask me anything about Python.", user="System", respond=False)
        return chat


# Set up environment
os.environ["AUTOGEN_USE_DOCKER"] = "False"

# Create the app instance
app = VITAApp()

# Create layout - directly start with main app view (no login)
layout = pn.Column(app.create_main_app())
layout.servable()
