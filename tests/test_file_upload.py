"""Test file upload functionality"""
import pytest
import param
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path to import test module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFileUploader:
    """Test the FileUploader class functionality"""
    
    def test_file_upload_initialization(self):
        """Test FileUploader initializes correctly"""
        # Import here to avoid running Panel extension during import
        from test import FileUploader
        
        uploader = FileUploader()
        assert uploader.file_content == "No file uploaded yet"
        assert uploader.uploaded_content is None
    
    def test_file_content_processing(self):
        """Test file content is processed correctly"""
        from test import FileUploader
        
        uploader = FileUploader()
        
        # Mock file upload event
        mock_event = Mock()
        mock_file_value = b'print("hello world")\nprint("test")'
        uploader.file_input.value = mock_file_value
        
        # Test upload processing
        uploader.upload_file(mock_event)
        
        expected_content = 'print("hello world")\nprint("test")'
        assert uploader.file_content == expected_content
        assert FileUploader.uploaded_content == expected_content
    
    def test_line_numbering_view(self):
        """Test that line numbers are added correctly"""
        from test import FileUploader
        
        uploader = FileUploader()
        uploader.file_content = 'print("hello")\nprint("world")'
        
        # Get the view (markdown pane)
        view = uploader.view()
        
        # Check that view contains line numbers
        assert "1    print" in str(view.object)
        assert "2    print" in str(view.object)
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        from test import FileUploader
        
        uploader = FileUploader()
        uploader.file_content = "No file uploaded yet"
        
        view = uploader.view()
        assert "No file uploaded yet" in str(view.object)