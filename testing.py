import panel as pn

# Create the two columns
left_column = pn.Column('Left Content')
right_column = pn.Column('Right Content')

# Create the row with both columns
row = pn.Row(left_column, right_column, sizing_mode='stretch_width')

# Create the toggle button
toggle_button = pn.widgets.Button(name='Toggle Left Column')

# Callback function to show/hide the left column
def toggle_visibility(event):
    if left_column.visible:
        left_column.visible = False
        right_column.sizing_mode = 'stretch_width'  # Make right column take full width
    else:
        left_column.visible = True
        right_column.sizing_mode = 'fixed'  # Return to equal sizing
        left_column.sizing_mode = 'stretch_width'  # Ensure equal sizing when visible

# Link the button to the callback function
toggle_button.on_click(toggle_visibility)

# Display the layout
pn.Column(toggle_button, row).servable()