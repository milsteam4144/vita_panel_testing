"""
Basic JSON-based memory store for VITA panel testing.
Handles storage and retrieval of student interaction data.
"""

import json
import os
from typing import Dict, List, Optional


class MemoryStore:
    """Simple JSON-based memory store for student interactions."""
    
    def __init__(self, data_file: str = "data/dummy_data.json"):
        """Initialize the memory store with a data file path."""
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data file {self.data_file}: {e}")
                return {"interactions": []}
        else:
            return {"interactions": []}
    
    def save_data(self) -> bool:
        """Save current data to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving data file {self.data_file}: {e}")
            return False
    
    def get_all_interactions(self) -> List[Dict]:
        """Get all stored interactions."""
        return self.data.get("interactions", [])
    
    def get_interaction_by_id(self, assignment_id: str) -> Optional[Dict]:
        """Get a specific interaction by assignment ID."""
        for interaction in self.data.get("interactions", []):
            if interaction.get("assignment_id") == assignment_id:
                return interaction
        return None
    
    def add_interaction(self, interaction: Dict) -> bool:
        """Add a new interaction to the store."""
        if "interactions" not in self.data:
            self.data["interactions"] = []
        
        # Validate required fields
        required_fields = ["assignment_id", "code_snippet", "student_prompt", "teacher_response"]
        if not all(field in interaction for field in required_fields):
            print(f"Missing required fields. Required: {required_fields}")
            return False
        
        self.data["interactions"].append(interaction)
        return self.save_data()
    
    def get_interactions_count(self) -> int:
        """Get the number of stored interactions."""
        return len(self.data.get("interactions", []))


def test_memory_store():
    """Simple test function for the memory store."""
    store = MemoryStore()
    print(f"Loaded {store.get_interactions_count()} interactions")
    
    if store.get_interactions_count() > 0:
        first_interaction = store.get_all_interactions()[0]
        print(f"First interaction ID: {first_interaction.get('assignment_id')}")
        print(f"Student prompt: {first_interaction.get('student_prompt')[:100]}...")


if __name__ == "__main__":
    test_memory_store()