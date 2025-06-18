"""Test VITA Trio multi-agent functionality"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_manager import PersonaManager

class TestVitaTrioConfiguration:
    """Test VITA Trio persona configuration"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_vita_trio_loading(self, persona_manager):
        """Test that VITA Trio persona loads correctly"""
        trio = persona_manager.get_persona('vita_trio')
        assert trio is not None
        assert trio.display_name == "VITA Trio"
        assert trio.description == "Three-agent team optimized for engaging student support: Coder finds technical issues, Cheerleader provides motivation, Coordinator orchestrates helpful responses"
    
    def test_trio_agent_roles(self, persona_manager):
        """Test that all three agents are defined with correct roles"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Check agent definitions in JSON structure
        assert 'coder' in trio.metadata or hasattr(trio, 'agents'), "Trio should define individual agents"
        
        # Check main role definitions
        assert 'debugger' in trio.roles
        assert 'corrector' in trio.roles
        assert 'student_proxy' in trio.roles
        
        # Check role avatars include trio elements
        debugger_avatar = trio.roles['debugger'].avatar
        assert '💻' in debugger_avatar or '🔍' in debugger_avatar or '🎉' in debugger_avatar or '🎯' in debugger_avatar
    
    def test_coordinator_conversation_management(self, persona_manager):
        """Test that coordinator focuses on conversation flow"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Look for coordinator-specific language in the configuration
        trio_data = str(trio.__dict__)  # Convert to string to search through all data
        
        # Should mention conversation flow concepts
        flow_keywords = ['conversation', 'flow', 'check', 'satisfaction', 'session']
        found_flow_concepts = any(keyword in trio_data.lower() for keyword in flow_keywords)
        
        assert found_flow_concepts, "VITA Trio should include conversation flow management concepts"
    
    def test_coder_technical_focus(self, persona_manager):
        """Test that coder agent focuses on technical issues"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Check debugger role for technical language
        debugger_prompt = trio.roles['debugger'].system_prompt.lower()
        
        technical_keywords = ['technical', 'error', 'syntax', 'line', 'code', 'debug']
        found_technical = any(keyword in debugger_prompt for keyword in technical_keywords)
        
        assert found_technical, f"VITA Trio debugger should focus on technical issues: {debugger_prompt[:100]}..."
    
    def test_cheerleader_motivation_focus(self, persona_manager):
        """Test that cheerleader concepts are present"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Look through all configuration for motivation/encouragement concepts
        trio_data = str(trio.__dict__).lower()
        
        motivation_keywords = ['encourage', 'motivat', 'positive', 'support', 'cheer']
        found_motivation = any(keyword in trio_data for keyword in motivation_keywords)
        
        assert found_motivation, "VITA Trio should include motivation/encouragement concepts"

class TestVitaTrioModelCompatibility:
    """Test VITA Trio model requirements and performance"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_small_model_optimization(self, persona_manager):
        """Test that VITA Trio is optimized for small models like dolphin"""
        trio = persona_manager.get_persona('vita_trio')
        
        model_compat = trio.model_compatibility
        
        # Should be optimized for dolphin
        optimized_models = model_compat.get('optimized_for', [])
        tested_models = model_compat.get('tested_models', [])
        
        dolphin_optimized = any('dolphin' in model.lower() for model in optimized_models + tested_models)
        assert dolphin_optimized, "VITA Trio should be optimized for dolphin models"
        
        # Should have reasonable token limits for small models
        max_tokens = model_compat.get('recommended_max_tokens', 1000)
        assert max_tokens <= 500, f"VITA Trio should use small token limits for efficiency: {max_tokens}"
    
    def test_response_time_targets(self, persona_manager):
        """Test that VITA Trio has realistic response time targets"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Look for timing information in the configuration
        trio_data = str(trio.__dict__).lower()
        
        # Should mention reasonable timing (10-20 seconds, not minutes)
        timing_indicators = ['10-20 seconds', 'second', 'fast', 'efficient']
        found_timing = any(indicator in trio_data for indicator in timing_indicators)
        
        # Should NOT mention long delays
        slow_indicators = ['minute', '59 second', 'slow', 'experimental']
        found_slow = any(indicator in trio_data for indicator in slow_indicators)
        
        assert found_timing, "VITA Trio should mention reasonable response times"
        assert not found_slow, "VITA Trio should not mention slow response times"

class TestVitaTrioWorkflow:
    """Test VITA Trio workflow and coordination patterns"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_autogen_group_chat_config(self, persona_manager):
        """Test that VITA Trio is configured for AutoGen group chat"""
        trio = persona_manager.get_persona('vita_trio')
        
        trio_data = str(trio.__dict__).lower()
        
        # Should mention AutoGen or group chat concepts
        autogen_keywords = ['autogen', 'group', 'chat', 'coordination', 'agent']
        found_autogen = any(keyword in trio_data for keyword in autogen_keywords)
        
        assert found_autogen, "VITA Trio should be configured for AutoGen group chat"
    
    def test_role_separation(self, persona_manager):
        """Test that VITA Trio has clear role separation"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Each agent should have distinct personality traits
        debugger_traits = trio.roles['debugger'].personality_traits
        corrector_traits = trio.roles['corrector'].personality_traits
        
        # Should have multiple distinct traits
        assert len(debugger_traits) >= 2, "Debugger should have multiple personality traits"
        assert len(corrector_traits) >= 2, "Corrector should have multiple personality traits"
        
        # Traits should be different (not identical)
        assert debugger_traits != corrector_traits, "Debugger and corrector should have different traits"

class TestVitaTrioIntegration:
    """Test VITA Trio integration readiness"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_persona_manager_integration(self, persona_manager):
        """Test that VITA Trio integrates with persona manager"""
        # Should be able to create agent config
        try:
            config = persona_manager.create_agent_config("vita_trio", "dolphin-2.1-mistral-7b")
            
            assert 'persona' in config
            assert 'model' in config
            assert 'llm_config' in config
            
            # LLM config should be ready for AutoGen
            llm_config = config['llm_config']
            assert 'config_list' in llm_config
            assert 'temperature' in llm_config
            
        except Exception as e:
            pytest.fail(f"Failed to create VITA Trio config: {e}")
    
    def test_conversation_readiness(self, persona_manager):
        """Test that VITA Trio is ready for conversation testing"""
        trio = persona_manager.get_persona('vita_trio')
        
        # Should have conversation settings
        conv_settings = trio.conversation_settings
        assert conv_settings is not None
        
        # Should have termination phrases
        termination = conv_settings.get('termination_phrases', [])
        assert len(termination) > 0, "Should have termination phrases defined"
        
        # Should have reasonable timeout
        timeout = conv_settings.get('timeout_seconds', 0)
        assert 60 <= timeout <= 300, f"Should have reasonable timeout: {timeout}"