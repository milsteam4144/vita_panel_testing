"""Test console demo functionality"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestVitaCore:
    """Test the extracted core logic"""
    
    def test_core_initialization(self):
        """Test VitaCore initializes correctly"""
        from vita_core import VitaCore
        
        # Mock the message callback
        mock_callback = Mock()
        core = VitaCore(message_callback=mock_callback)
        
        # Check agents are created
        assert core.user_proxy.name == "Student"
        assert core.debugger.name == "Debugger" 
        assert core.corrector.name == "Corrector"
        assert core.message_callback == mock_callback
    
    def test_file_processing(self):
        """Test file content processing with line numbers"""
        from vita_core import VitaCore
        
        core = VitaCore()
        
        # Test normal file processing
        content = 'print("hello")\nprint("world")'
        result = core.process_file(content)
        
        assert "1    print(\"hello\")" in result
        assert "2    print(\"world\")" in result
        assert core.uploaded_file_content == content
    
    def test_empty_file_processing(self):
        """Test handling of empty files"""
        from vita_core import VitaCore
        
        core = VitaCore()
        
        # Test empty content
        result = core.process_file("")
        assert result == "No file content provided"
        
        # Test whitespace-only content
        result = core.process_file("   \n\t  ")
        assert result == "No file content provided"
    
    def test_configuration_local_model(self):
        """Test local model configuration"""
        with patch.dict('os.environ', {'USE_LOCAL_MODEL': 'true'}):
            from vita_core import VitaCore
            
            core = VitaCore()
            config = core.config_list[0]
            
            assert 'base_url' in config
            assert config['base_url'] == 'http://localhost:1234/v1'
            assert 'dolphin' in config['model']
    
    def test_configuration_openai_model(self):
        """Test OpenAI model configuration"""
        with patch.dict('os.environ', {'USE_LOCAL_MODEL': 'false', 'OPENAI_API_KEY': 'test-key'}):
            from vita_core import VitaCore
            
            core = VitaCore()
            config = core.config_list[0]
            
            assert config['model'] == 'gpt-4o'
            assert config['api_key'] == 'test-key'

class TestConsoleDemo:
    """Test console demo functionality"""
    
    def test_console_initialization(self):
        """Test console demo initializes correctly"""
        with patch('vita_core.VitaCore'):
            from vita_console_demo import VitaConsole
            
            console = VitaConsole()
            assert console.vita is not None
    
    def test_display_message(self):
        """Test message display formatting"""
        with patch('vita_core.VitaCore'), patch('builtins.print') as mock_print:
            from vita_console_demo import VitaConsole
            
            console = VitaConsole()
            console.display_message("TestAgent", "Test message", "🤖")
            
            # Check that print was called multiple times for formatting
            assert mock_print.call_count >= 3
    
    def test_file_processing_integration(self):
        """Test file processing through console interface"""
        with patch('vita_core.VitaCore'):
            from vita_console_demo import VitaConsole
            
            console = VitaConsole()
            
            # Mock the core's process_file method
            console.vita.process_file = Mock(return_value="1    test code")
            
            with patch('builtins.print'):
                console.display_file_with_numbers("test code")
                
            console.vita.process_file.assert_called_once_with("test code")

class TestProtocolIntegration:
    """Test that our test protocol works end-to-end"""
    
    def test_sample_files_exist(self):
        """Test that our test data files exist and are readable"""
        test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        
        # Check required test files exist
        files = ['valid_code.py', 'syntax_error.py', 'empty_file.py']
        for filename in files:
            filepath = os.path.join(test_data_dir, filename)
            assert os.path.exists(filepath), f"Test data file missing: {filename}"
            
        # Check we can read the files
        valid_file = os.path.join(test_data_dir, 'valid_code.py')
        with open(valid_file, 'r') as f:
            content = f.read()
            assert 'print' in content  # Should contain some Python code
    
    def test_syntax_validation(self):
        """Test that our main modules have valid syntax"""
        import py_compile
        import tempfile
        
        # Test main modules compile without syntax errors
        modules = ['test.py', 'main_test.py', 'vita_core.py', 'vita_console_demo.py']
        
        for module in modules:
            module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), module)
            if os.path.exists(module_path):
                try:
                    py_compile.compile(module_path, doraise=True)
                except py_compile.PyCompileError as e:
                    pytest.fail(f"Syntax error in {module}: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])