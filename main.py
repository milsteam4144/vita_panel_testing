#!/usr/bin/env python3
"""
VITA Panel main startup script.

Usage:
    panel serve main.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev
"""

import panel as pn
from vita_app import AuthenticatedVITA, set_global_layout

# Create the app instance
app = AuthenticatedVITA()

# Create layout - always start with login view
layout = pn.Column(app.login_view())

# Set the global layout for the app to use
set_global_layout(layout)

# Make the layout servable
layout.servable()