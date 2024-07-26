import panel as pn

# Step 1: Define the global variable
current_file_contents = "Mallory"

# Step 2: Create the FileInput widget
file_input = pn.widgets.FileInput(accept='.py')

# Step 3: Create the Markdown pane to display file contents
file_contents_pane = pn.pane.Markdown('Upload a .py file to see its contents here.')

# Step 4: Define a callback function
def update_file_contents(event):
    global current_file_contents  # Declare the variable as global to modify it
    # Check if a file has been uploaded
    if file_input.value is not None:
        # Decode the file contents with utf-8
        current_file_contents = file_input.value.decode('utf-8')
        # Update the Markdown pane with the new contents
        file_contents_pane.object = f"```\n{current_file_contents}\n```"
        #display to terminal the current_file_contents
        #print_current_file_contents()

# Example: Accessing the global variable outside the function
def print_current_file_contents(event):
    return(current_file_contents)



# Step 5: Link the FileInput widget to the callback function
file_input.param.watch(update_file_contents, 'value')
file_input.param.watch(print_current_file_contents, 'value')

# Layout
layout = pn.Column(file_input, file_contents_pane)

# Display the layout
layout.servable()

print("\n\nLastly, the file contents are", current_file_contents)



