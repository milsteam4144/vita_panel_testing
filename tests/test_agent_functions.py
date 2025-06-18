"""Test agent functionality without requiring LM Studio"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAgentConfiguration:
    """Test agent setup and configuration"""
    
    def test_agent_system_messages(self):
        """Test that agents have proper system messages"""
        # Import with mocked Panel to avoid UI initialization
        with patch('panel.extension'):
            from test import debugger, corrector, user_proxy
            
            # Test Debugger system message
            assert "Debugger" in debugger.system_message
            assert "syntax errors" in debugger.system_message
            assert "don't write code" in debugger.system_message
            
            # Test Corrector system message
            assert "Corrector" in corrector.system_message
            assert "plan to fix" in corrector.system_message
            assert "never show the corrected code" in corrector.system_message
            
            # Test Student system message
            assert "student" in user_proxy.system_message.lower()
    
    def test_agent_configuration(self):
        """Test agent configuration settings"""
        with patch('panel.extension'):
            from test import debugger, corrector, user_proxy
            
            # Test agent names
            assert debugger.name == "Debugger"
            assert corrector.name == "Corrector"
            assert user_proxy.name == "Student"
            
            # Test human input modes
            assert debugger.human_input_mode == "NEVER"
            assert corrector.human_input_mode == "NEVER"
            assert user_proxy.human_input_mode == "ALWAYS"

class TestMessageFiltering:
    """Test the critical message filtering fix"""
    
    def test_empty_message_filtering(self):
        """Test that empty messages are filtered (Issue #001 fix)"""
        with patch('panel.extension'):
            from test import print_messages
            
            # Mock objects
            mock_recipient = Mock()
            mock_recipient.name = "TestRecipient"
            mock_sender = Mock()
            mock_sender.name = "TestSender"
            
            # Test empty content message
            empty_message = [{'content': '', 'name': 'TestAgent', 'role': 'assistant'}]
            
            # Should return False, None and not send to chat
            result = print_messages(mock_recipient, empty_message, mock_sender, {})
            assert result == (False, None)
            
            # Test whitespace-only message
            whitespace_message = [{'content': '   \n\t  ', 'name': 'TestAgent', 'role': 'assistant'}]
            result = print_messages(mock_recipient, whitespace_message, mock_sender, {})
            assert result == (False, None)
    
    def test_valid_message_processing(self):
        """Test that valid messages are processed"""
        with patch('panel.extension'):
            with patch('test.chat_interface') as mock_chat:
                from test import print_messages
                
                mock_recipient = Mock()
                mock_recipient.name = "TestRecipient"
                mock_sender = Mock()
                mock_sender.name = "TestSender"
                
                # Test valid message (use valid agent name from avatar dict)
                valid_message = [{'content': 'This is a valid message', 'name': 'Debugger', 'role': 'assistant'}]
                
                result = print_messages(mock_recipient, valid_message, mock_sender, {})
                assert result == (False, None)
                # Chat interface should be called for valid messages
                mock_chat.send.assert_called()

class TestConfigurationHandling:
    """Test configuration and environment handling"""
    
    def test_local_model_config(self):
        """Test local model configuration"""
        with patch('panel.extension'):
            with patch.dict('os.environ', {'USE_LOCAL_MODEL': 'true'}):
                # Re-import to get updated config
                import importlib
                import test
                importlib.reload(test)
                
                from test import config_list
                
                # Should use local configuration
                assert config_list[0]['base_url'] == 'http://localhost:1234/v1'
                assert 'dolphin' in config_list[0]['model']
    
    def test_openai_model_config(self):
        """Test OpenAI model configuration"""
        with patch('panel.extension'):
            with patch.dict('os.environ', {'USE_LOCAL_MODEL': 'false', 'OPENAI_API_KEY': 'test-key'}):
                import importlib
                import test
                importlib.reload(test)
                
                from test import config_list
                
                # Should use OpenAI configuration
                assert config_list[0]['model'] == 'gpt-4o'
                assert config_list[0]['api_key'] == 'test-key'