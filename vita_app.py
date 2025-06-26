"""
VITA (Virtual Interactive Teaching Assistant) - Main Application Entry Point

This is the main application file that orchestrates the VITA application using 
the modularized vita_lib components.

You MUST set the environment variables for GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET

Run the command below in the terminal to start the Panel server for this application:

panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
"""

import panel as pn

# Import modular components
from vita_lib import Config, AuthenticatedVITA

# Load panel extension and custom CSS from local file styles.css
pn.extension()
with open("user_interface/styles.css") as f:
    pn.config.raw_css.append(f.read())

# Set up environment
Config.setup_environment()

# Create layout - always start with login view
layout = pn.Column()

# Layout update callback
def update_layout(new_content):
    """Update the main layout with new content."""
    layout.clear()
    layout.append(new_content)

# Create the app instance with layout callback
app = AuthenticatedVITA(layout_callback=update_layout)

# Initialize with login view
layout.append(app.login_view())
layout.servable()