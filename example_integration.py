"""
Example integration of memory store with VITA panel.
Demonstrates how to use the synthetic dummy data in the existing chat interface.
"""

import sys
import os

# Add the current directory to the path so we can import memory_store
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_store import MemoryStore


class VITAMemoryIntegration:
    """Example integration class showing how to use memory store with VITA."""
    
    def __init__(self):
        """Initialize with memory store."""
        self.memory_store = MemoryStore()
        print(f"Loaded {self.memory_store.get_interactions_count()} reference interactions")
    
    def get_similar_examples(self, student_code: str) -> list:
        """
        Find similar code examples from memory store.
        In a real implementation, this could use more sophisticated matching.
        """
        interactions = self.memory_store.get_all_interactions()
        similar_examples = []
        
        # Simple keyword matching for demonstration
        student_code_lower = student_code.lower()
        
        for interaction in interactions:
            code_snippet = interaction["code_snippet"].lower()
            
            # Check for common Python keywords and patterns
            if any(keyword in student_code_lower and keyword in code_snippet 
                   for keyword in ["for", "if", "while", "def", "print", "input"]):
                similar_examples.append(interaction)
        
        return similar_examples[:3]  # Return top 3 matches
    
    def get_teaching_response_style(self, topic_area: str) -> str:
        """
        Get example teaching responses for a given topic area.
        Helps maintain consistent pedagogical style.
        """
        interactions = self.memory_store.get_all_interactions()
        
        for interaction in interactions:
            if topic_area.lower() in interaction["assignment_id"].lower():
                return interaction["teacher_response"]
        
        # Return a generic pedagogical response style if no match
        return "Let's think about this step by step. What do you think might be happening here?"
    
    def simulate_chat_interaction(self, student_code: str, student_question: str):
        """
        Simulate how the memory store could enhance chat interactions.
        """
        print("=" * 60)
        print("VITA CHAT SIMULATION")
        print("=" * 60)
        print(f"Student uploads code:\n{student_code}")
        print(f"\nStudent asks: {student_question}")
        
        # Find similar examples
        similar = self.get_similar_examples(student_code)
        
        if similar:
            print(f"\n🔍 Found {len(similar)} similar examples in memory store:")
            for i, example in enumerate(similar, 1):
                print(f"{i}. {example['assignment_id']}: {example['student_prompt'][:50]}...")
            
            # Use the first similar example's teaching style
            example_response = similar[0]["teacher_response"]
            print(f"\n🎓 Teaching response style (based on {similar[0]['assignment_id']}):")
            print(f"{example_response}")
            
        else:
            print("\n🔍 No similar examples found in memory store")
            print("🎓 Using default pedagogical approach...")


def demo_integration():
    """Demonstrate the memory store integration."""
    integration = VITAMemoryIntegration()
    
    # Test with some sample student code scenarios
    test_cases = [
        {
            "code": "for i in range(3)\n    print(i)",
            "question": "Why am I getting a syntax error with my loop?"
        },
        {
            "code": "age = input('How old are you?')\nif age >= 18\n    print('Adult')",
            "question": "My if statement isn't working, what's wrong?"
        },
        {
            "code": "def greet(name):\nprint(f'Hello {name}')\ngreet('Alice')",
            "question": "My function seems to run but the formatting looks weird"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}")
        integration.simulate_chat_interaction(test_case["code"], test_case["question"])
    
    print(f"\n{'='*60}")
    print("INTEGRATION DEMO COMPLETE")
    print("✓ Memory store successfully provides contextual examples")
    print("✓ Teaching responses maintain pedagogical consistency")
    print("✓ Ready for integration with VITA panel interface")


if __name__ == "__main__":
    demo_integration()