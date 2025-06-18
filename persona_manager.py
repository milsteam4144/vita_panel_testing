"""
Persona Management System for VITA
Handles loading and managing different AI personalities with independent model selection
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    name: str
    base_url: str
    api_key: str
    temperature: float = 0.1
    max_tokens: int = 500
    provider: str = "lmstudio"  # lmstudio, openai, etc.

@dataclass
class VoiceConfig:
    """Voice configuration for future TTS integration"""
    enabled: bool = False
    language: str = "en-US"
    voice_type: str = "female"
    speech_rate: str = "normal"
    tone: str = "friendly"

@dataclass
class RoleConfig:
    """Configuration for a specific agent role"""
    name: str
    avatar: str
    system_prompt: str
    personality_traits: List[str]

@dataclass
class PersonaConfig:
    """Complete persona configuration"""
    name: str
    display_name: str
    full_name: str
    gender: str
    personality: str
    description: str
    roles: Dict[str, RoleConfig]
    voice_settings: VoiceConfig
    teaching_style: Dict[str, str]
    conversation_settings: Dict[str, Any]
    model_compatibility: Dict[str, Any]
    metadata: Dict[str, str]

class PersonaManager:
    """Manages persona loading and model configuration"""
    
    def __init__(self, personas_dir: str = "personas"):
        self.personas_dir = Path(personas_dir)
        self.available_personas: Dict[str, PersonaConfig] = {}
        self.available_models: Dict[str, ModelConfig] = {}
        self._load_personas()
        self._setup_default_models()
    
    def _load_personas(self):
        """Load all persona configurations from JSON files"""
        if not self.personas_dir.exists():
            print(f"Warning: Personas directory {self.personas_dir} not found")
            return
            
        for persona_file in self.personas_dir.glob("*.json"):
            try:
                with open(persona_file, 'r') as f:
                    data = json.load(f)
                
                persona = self._parse_persona_config(data)
                self.available_personas[persona.name.lower()] = persona
                print(f"Loaded persona: {persona.display_name}")
                
            except Exception as e:
                print(f"Error loading persona from {persona_file}: {e}")
    
    def _parse_persona_config(self, data: Dict) -> PersonaConfig:
        """Parse JSON data into PersonaConfig object"""
        
        # Parse roles
        roles = {}
        for role_name, role_data in data.get("roles", {}).items():
            roles[role_name] = RoleConfig(
                name=role_data["name"],
                avatar=role_data["avatar"],
                system_prompt=role_data["system_prompt"],
                personality_traits=role_data.get("personality_traits", [])
            )
        
        # Parse voice settings
        voice_data = data.get("voice_settings", {})
        voice_config = VoiceConfig(
            enabled=voice_data.get("enabled", False),
            language=voice_data.get("language", "en-US"),
            voice_type=voice_data.get("voice_type", "female"),
            speech_rate=voice_data.get("speech_rate", "normal"),
            tone=voice_data.get("tone", "friendly")
        )
        
        return PersonaConfig(
            name=data["name"],
            display_name=data["display_name"],
            full_name=data["full_name"],
            gender=data["gender"],
            personality=data["personality"],
            description=data["description"],
            roles=roles,
            voice_settings=voice_config,
            teaching_style=data.get("teaching_style", {}),
            conversation_settings=data.get("conversation_settings", {}),
            model_compatibility=data.get("model_compatibility", {}),
            metadata=data.get("metadata", {})
        )
    
    def _setup_default_models(self):
        """Setup default model configurations"""
        
        # LM Studio models
        self.available_models["dolphin-2.1-mistral-7b"] = ModelConfig(
            name="dolphin-2.1-mistral-7b",
            base_url="http://localhost:1234/v1",
            api_key="lm-studio",
            temperature=0.1,
            max_tokens=500,
            provider="lmstudio"
        )
        
        self.available_models["phi-4-mini-reasoning"] = ModelConfig(
            name="microsoft/phi-4-mini-reasoning",
            base_url="http://localhost:1234/v1", 
            api_key="lm-studio",
            temperature=0.05,  # Lower for reasoning model
            max_tokens=800,    # Higher for detailed reasoning
            provider="lmstudio"
        )
        
        # OpenAI models
        self.available_models["gpt-4o"] = ModelConfig(
            name="gpt-4o",
            base_url="https://api.openai.com/v1",
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            temperature=0.1,
            max_tokens=500,
            provider="openai"
        )
    
    def get_persona(self, persona_name: str = "vita") -> Optional[PersonaConfig]:
        """Get persona configuration by name"""
        return self.available_personas.get(persona_name.lower())
    
    def get_model(self, model_name: str) -> Optional[ModelConfig]:
        """Get model configuration by name"""
        return self.available_models.get(model_name)
    
    def list_personas(self) -> List[str]:
        """List all available persona names"""
        return list(self.available_personas.keys())
    
    def list_models(self) -> List[str]:
        """List all available model names"""
        return list(self.available_models.keys())
    
    def create_agent_config(self, persona_name: str = "vita", model_name: str = "dolphin-2.1-mistral-7b") -> Dict:
        """Create agent configuration combining persona and model"""
        
        persona = self.get_persona(persona_name)
        if not persona:
            raise ValueError(f"Persona '{persona_name}' not found. Available: {self.list_personas()}")
        
        model = self.get_model(model_name)
        if not model:
            raise ValueError(f"Model '{model_name}' not found. Available: {self.list_models()}")
        
        # Create config_list for AutoGen
        config_list = [{
            'model': model.name,
            'base_url': model.base_url,
            'api_key': model.api_key,
        }]
        
        # Apply persona-specific model settings if available
        model_compat = persona.model_compatibility
        temperature = model_compat.get("recommended_temperature", model.temperature)
        max_tokens = model_compat.get("recommended_max_tokens", model.max_tokens)
        
        llm_config = {
            "config_list": config_list,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "seed": 53
        }
        
        return {
            "persona": persona,
            "model": model,
            "llm_config": llm_config,
            "display_info": {
                "title": f"{persona.display_name} with {model.name}",
                "description": persona.description,
                "personality": persona.personality
            }
        }
    
    def add_custom_model(self, name: str, base_url: str, api_key: str = "lm-studio", 
                        temperature: float = 0.1, max_tokens: int = 500, provider: str = "lmstudio"):
        """Add a custom model configuration"""
        self.available_models[name] = ModelConfig(
            name=name,
            base_url=base_url, 
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=provider
        )
        print(f"Added custom model: {name}")
    
    def get_persona_info(self, persona_name: str = "vita") -> str:
        """Get formatted information about a persona"""
        persona = self.get_persona(persona_name)
        if not persona:
            return f"Persona '{persona_name}' not found"
        
        info = f"""
{persona.display_name} ({persona.full_name})
{'-' * len(persona.display_name)}
Description: {persona.description}
Personality: {persona.personality}
Gender: {persona.gender}

Roles:
"""
        for role_name, role in persona.roles.items():
            info += f"  {role.avatar} {role.name}: {', '.join(role.personality_traits)}\n"
        
        info += f"\nTeaching Style: {persona.teaching_style.get('approach', 'Not specified')}"
        info += f"\nCompatible Models: {', '.join(persona.model_compatibility.get('tested_models', []))}"
        
        return info

# Global instance for easy access
persona_manager = PersonaManager()

def get_default_config() -> Dict:
    """Get default Vita configuration with dolphin model"""
    return persona_manager.create_agent_config("vita", "dolphin-2.1-mistral-7b")

def get_experimental_config() -> Dict:
    """Get experimental Vita configuration with phi-4 model"""
    return persona_manager.create_agent_config("vita", "phi-4-mini-reasoning")