"""
File handler module for VITA application.

Handles file upload and processing functionality.
"""

import panel as pn
import param


class FileUploader(param.Parameterized):
    """Handles file upload and display functionality."""
    
    file_input = pn.widgets.FileInput(accept='.py', name='Upload .py file')
    file_content = param.String(default="No file uploaded yet")
    uploaded_content = None

    def __init__(self, **params):
        super().__init__(**params)
        self.file_input.styles = {'background': 'white'}
        self.file_input.param.watch(self.upload_file, 'value')

    @param.depends('file_content')
    def view(self):
        """Generate a view of the uploaded file with line numbers."""
        lines = self.file_content.split('\n')
        new_code = ""
        
        if lines[0] != 'No file uploaded yet':
            for line_index, line in enumerate(lines, start=1):
                new_code += (f"{line_index:<4} {line}\n")
        else:
            new_code = self.file_content
            
        return pn.pane.Markdown(f"```python\n{new_code}\n```", 
                               sizing_mode='stretch_both', css_classes=['no-margin'])

    def upload_file(self, event):
        """Handle file upload event."""
        # Global variable for backward compatibility
        global test
        
        if self.file_input.value:
            FileUploader.uploaded_content = self.file_input.value.decode('utf-8')
            self.file_content = FileUploader.uploaded_content
            test = FileUploader.uploaded_content