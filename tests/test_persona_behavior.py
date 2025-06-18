"""Test persona behavior validation using A/B test questions"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_manager import PersonaManager, PersonaConfig

class TestPersonaBehaviorValidation:
    """Test that personas respond with their characteristic language patterns"""
    
    @pytest.fixture
    def persona_manager(self):
        """Create persona manager instance"""
        return PersonaManager()
    
    def test_persona_loading(self, persona_manager):
        """Test that all expected personas are loaded"""
        personas = persona_manager.list_personas()
        expected_personas = ['vita', 'liza', 'circuit']
        
        for persona in expected_personas:
            assert persona in personas, f"Expected persona '{persona}' not found"
    
    def test_dr_liza_visual_metaphors(self, persona_manager):
        """Test that Dr. LIZA uses animation/visual metaphors in system prompts"""
        liza = persona_manager.get_persona('liza')
        assert liza is not None
        
        debugger_prompt = liza.roles['debugger'].system_prompt.lower()
        corrector_prompt = liza.roles['corrector'].system_prompt.lower()
        
        # Check for animation/visual keywords
        visual_keywords = ['animation', 'frame', 'visual', 'storyboard', 'artistic']
        
        found_in_debugger = any(keyword in debugger_prompt for keyword in visual_keywords)
        found_in_corrector = any(keyword in corrector_prompt for keyword in visual_keywords)
        
        assert found_in_debugger, f"Dr. LIZA debugger prompt missing visual metaphors: {debugger_prompt[:100]}..."
        assert found_in_corrector, f"Dr. LIZA corrector prompt missing visual metaphors: {corrector_prompt[:100]}..."
    
    def test_circuit_detective_language(self, persona_manager):
        """Test that Circuit uses detective/investigation language"""
        circuit = persona_manager.get_persona('circuit')
        assert circuit is not None
        
        debugger_prompt = circuit.roles['debugger'].system_prompt.lower()
        corrector_prompt = circuit.roles['corrector'].system_prompt.lower()
        
        # Check for detective keywords
        detective_keywords = ['detective', 'investigate', 'case', 'clues', 'evidence']
        
        found_in_debugger = any(keyword in debugger_prompt for keyword in detective_keywords)
        found_in_corrector = any(keyword in corrector_prompt for keyword in detective_keywords)
        
        assert found_in_debugger, f"Circuit debugger prompt missing detective language: {debugger_prompt[:100]}..."
        assert found_in_corrector, f"Circuit corrector prompt missing detective language: {corrector_prompt[:100]}..."
    
    def test_vita_educational_language(self, persona_manager):
        """Test that VITA uses educational/teaching language"""
        vita = persona_manager.get_persona('vita')
        assert vita is not None
        
        debugger_prompt = vita.roles['debugger'].system_prompt.lower()
        corrector_prompt = vita.roles['corrector'].system_prompt.lower()
        
        # Check for educational keywords
        educational_keywords = ['teach', 'learn', 'student', 'explain', 'understand', 'educational']
        
        found_in_debugger = any(keyword in debugger_prompt for keyword in educational_keywords)
        found_in_corrector = any(keyword in corrector_prompt for keyword in educational_keywords)
        
        assert found_in_debugger, f"VITA debugger prompt missing educational language: {debugger_prompt[:100]}..."
        assert found_in_corrector, f"VITA corrector prompt missing educational language: {corrector_prompt[:100]}..."

class TestPersonaCharacteristics:
    """Test specific persona characteristics and behavior patterns"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_liza_personality_traits(self, persona_manager):
        """Test Dr. LIZA has expected personality traits"""
        liza = persona_manager.get_persona('liza')
        
        debugger_traits = liza.roles['debugger'].personality_traits
        corrector_traits = liza.roles['corrector'].personality_traits
        
        # Check for animation/visual related traits
        expected_patterns = ['animation', 'visual', 'frame', 'artistic', 'storyboard']
        
        debugger_text = ' '.join(debugger_traits).lower()
        corrector_text = ' '.join(corrector_traits).lower()
        
        assert any(pattern in debugger_text for pattern in expected_patterns), f"Dr. LIZA debugger traits: {debugger_traits}"
        assert any(pattern in corrector_text for pattern in expected_patterns), f"Dr. LIZA corrector traits: {corrector_traits}"
    
    def test_circuit_personality_traits(self, persona_manager):
        """Test Circuit has expected personality traits"""
        circuit = persona_manager.get_persona('circuit')
        
        debugger_traits = circuit.roles['debugger'].personality_traits
        corrector_traits = circuit.roles['corrector'].personality_traits
        
        # Check for detective/investigation traits
        expected_patterns = ['detective', 'investigation', 'clues', 'evidence', 'case']
        
        debugger_text = ' '.join(debugger_traits).lower()
        corrector_text = ' '.join(corrector_traits).lower()
        
        assert any(pattern in debugger_text for pattern in expected_patterns), f"Circuit debugger traits: {debugger_traits}"
        assert any(pattern in corrector_text for pattern in expected_patterns), f"Circuit corrector traits: {corrector_traits}"
    
    def test_vita_personality_traits(self, persona_manager):
        """Test VITA has expected personality traits"""
        vita = persona_manager.get_persona('vita')
        
        debugger_traits = vita.roles['debugger'].personality_traits
        corrector_traits = vita.roles['corrector'].personality_traits
        
        # Check for educational traits
        expected_patterns = ['encouraging', 'educational', 'patient', 'simple', 'supportive']
        
        debugger_text = ' '.join(debugger_traits).lower()
        corrector_text = ' '.join(corrector_traits).lower()
        
        assert any(pattern in debugger_text for pattern in expected_patterns), f"VITA debugger traits: {debugger_traits}"
        assert any(pattern in corrector_text for pattern in expected_patterns), f"VITA corrector traits: {corrector_traits}"

class TestPersonaABQuestions:
    """A/B test questions to validate persona behavior patterns"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_syntax_error_response_style(self, persona_manager):
        """Test that each persona would approach syntax errors differently"""
        # Sample syntax error scenario
        error_code = "print('Hello World'"  # Missing closing parenthesis
        
        liza = persona_manager.get_persona('liza')
        circuit = persona_manager.get_persona('circuit')
        vita = persona_manager.get_persona('vita')
        
        # Test that their debugger prompts contain different approaches
        liza_approach = liza.roles['debugger'].system_prompt
        circuit_approach = circuit.roles['debugger'].system_prompt
        vita_approach = vita.roles['debugger'].system_prompt
        
        # LIZA should mention frames/animation
        assert 'frame' in liza_approach.lower() or 'animation' in liza_approach.lower()
        
        # Circuit should mention investigation/detective work
        assert 'investigate' in circuit_approach.lower() or 'clues' in circuit_approach.lower()
        
        # VITA should mention teaching/learning
        assert 'teach' in vita_approach.lower() or 'learn' in vita_approach.lower() or 'student' in vita_approach.lower()
    
    def test_correction_guidance_style(self, persona_manager):
        """Test that each persona provides corrections in their characteristic style"""
        liza = persona_manager.get_persona('liza')
        circuit = persona_manager.get_persona('circuit')
        vita = persona_manager.get_persona('vita')
        
        liza_correction = liza.roles['corrector'].system_prompt
        circuit_correction = circuit.roles['corrector'].system_prompt
        vita_correction = vita.roles['corrector'].system_prompt
        
        # LIZA should use storyboard/artistic metaphors
        assert 'storyboard' in liza_correction.lower() or 'artistic' in liza_correction.lower()
        
        # Circuit should use case/plan terminology
        assert 'case' in circuit_correction.lower() or 'plan' in circuit_correction.lower()
        
        # VITA should emphasize student understanding
        assert 'student' in vita_correction.lower() and 'understand' in vita_correction.lower()
    
    def test_avatar_consistency(self, persona_manager):
        """Test that each persona has appropriate avatars for their roles"""
        personas = ['liza', 'circuit', 'vita']
        
        for persona_name in personas:
            persona = persona_manager.get_persona(persona_name)
            
            # Each persona should have debugger and corrector roles with avatars
            assert 'debugger' in persona.roles
            assert 'corrector' in persona.roles
            
            debugger_avatar = persona.roles['debugger'].avatar
            corrector_avatar = persona.roles['corrector'].avatar
            
            # Avatars should not be empty
            assert debugger_avatar and debugger_avatar.strip()
            assert corrector_avatar and corrector_avatar.strip()
            
            # Should be emoji characters (simple check)
            assert len(debugger_avatar) <= 10  # Emojis are typically short
            assert len(corrector_avatar) <= 10

class TestPersonaCompatibility:
    """Test persona model compatibility settings"""
    
    @pytest.fixture
    def persona_manager(self):
        return PersonaManager()
    
    def test_model_compatibility_exists(self, persona_manager):
        """Test that all personas have model compatibility settings"""
        personas = ['liza', 'circuit', 'vita']
        
        for persona_name in personas:
            persona = persona_manager.get_persona(persona_name)
            
            # Should have model compatibility section
            assert 'tested_models' in persona.model_compatibility
            assert 'recommended_temperature' in persona.model_compatibility
            assert 'recommended_max_tokens' in persona.model_compatibility
            
            # Should have reasonable values
            temp = persona.model_compatibility['recommended_temperature']
            tokens = persona.model_compatibility['recommended_max_tokens']
            
            assert 0.0 <= temp <= 1.0, f"{persona_name} temperature {temp} out of range"
            assert 100 <= tokens <= 2000, f"{persona_name} max_tokens {tokens} out of range"
    
    def test_agent_config_creation(self, persona_manager):
        """Test that agent configurations can be created for each persona"""
        personas = ['liza', 'circuit', 'vita']
        
        for persona_name in personas:
            # Should be able to create config without errors
            try:
                config = persona_manager.create_agent_config(persona_name, "dolphin-2.1-mistral-7b")
                
                # Should have required sections
                assert 'persona' in config
                assert 'model' in config
                assert 'llm_config' in config
                assert 'display_info' in config
                
                # LLM config should have required fields
                llm_config = config['llm_config']
                assert 'config_list' in llm_config
                assert 'temperature' in llm_config
                assert 'max_tokens' in llm_config
                
            except Exception as e:
                pytest.fail(f"Failed to create config for {persona_name}: {e}")