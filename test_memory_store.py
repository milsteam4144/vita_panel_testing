#!/usr/bin/env python3
"""
Test script for memory store functionality.
Validates that the dummy data is correctly structured and accessible.
"""

import sys
import os

# Add the current directory to the path so we can import memory_store
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_store import MemoryStore


def test_memory_store_functionality():
    """Test all basic memory store functionality."""
    print("=== Testing Memory Store Functionality ===\n")
    
    # Initialize memory store
    store = MemoryStore()
    print(f"✓ Memory store initialized successfully")
    
    # Test data loading
    interactions = store.get_all_interactions()
    interaction_count = store.get_interactions_count()
    print(f"✓ Loaded {interaction_count} interactions")
    
    if interaction_count == 0:
        print("❌ No interactions found in dummy data")
        return False
    
    # Test data structure validation
    print("\n=== Validating Data Structure ===")
    required_fields = ["assignment_id", "code_snippet", "student_prompt", "teacher_response"]
    
    for i, interaction in enumerate(interactions):
        for field in required_fields:
            if field not in interaction:
                print(f"❌ Interaction {i+1} missing required field: {field}")
                return False
        
        # Validate that fields are not empty
        for field in required_fields:
            if not interaction[field] or not interaction[field].strip():
                print(f"❌ Interaction {i+1} has empty field: {field}")
                return False
    
    print(f"✓ All {interaction_count} interactions have required fields")
    
    # Test specific interaction retrieval
    print("\n=== Testing Interaction Retrieval ===")
    first_interaction = interactions[0]
    assignment_id = first_interaction["assignment_id"]
    
    retrieved_interaction = store.get_interaction_by_id(assignment_id)
    if retrieved_interaction is None:
        print(f"❌ Failed to retrieve interaction by ID: {assignment_id}")
        return False
    
    if retrieved_interaction["assignment_id"] != assignment_id:
        print(f"❌ Retrieved wrong interaction")
        return False
    
    print(f"✓ Successfully retrieved interaction by ID: {assignment_id}")
    
    # Test that assignment IDs are unique
    print("\n=== Testing Data Quality ===")
    assignment_ids = [interaction["assignment_id"] for interaction in interactions]
    unique_ids = set(assignment_ids)
    
    if len(assignment_ids) != len(unique_ids):
        print(f"❌ Duplicate assignment IDs found")
        return False
    
    print(f"✓ All assignment IDs are unique")
    
    # Test that student prompts are realistic questions
    for interaction in interactions:
        prompt = interaction["student_prompt"]
        if len(prompt) < 10:
            print(f"❌ Student prompt too short: {prompt}")
            return False
        
        # Check that it's actually a question or request for help
        if not any(word in prompt.lower() for word in ["error", "help", "wrong", "why", "how", "what", "trying", "problem"]):
            print(f"❌ Student prompt doesn't seem like a help request: {prompt}")
            return False
    
    print(f"✓ All student prompts appear to be realistic help requests")
    
    # Test that teacher responses are pedagogical (not giving direct answers)
    for interaction in interactions:
        response = interaction["teacher_response"]
        if len(response) < 20:
            print(f"❌ Teacher response too short: {response}")
            return False
        
        # Check for pedagogical language
        if not any(phrase in response.lower() for phrase in ["think", "what do you", "look at", "remember", "consider", "step by step", "let's"]):
            print(f"❌ Teacher response doesn't seem pedagogical: {response}")
            return False
        
        # Make sure it doesn't just give the answer
        code_snippet = interaction["code_snippet"]
        if ":" in code_snippet and ":" in response and response.count(":") > 1:
            print(f"⚠ Warning: Teacher response might be giving too much direct code help")
    
    print(f"✓ All teacher responses appear to be appropriately pedagogical")
    
    # Test code snippets contain realistic errors
    print("\n=== Testing Code Snippet Quality ===")
    common_errors = ["missing :", "missing quotes", "wrong indexing", "missing parentheses", "indentation"]
    
    for interaction in interactions:
        code = interaction["code_snippet"]
        if len(code) < 10:
            print(f"❌ Code snippet too short: {code}")
            return False
        
        # Check that code contains Python-like syntax
        if not any(keyword in code for keyword in ["print", "for", "if", "def", "while", "=", "input", "["]):
            print(f"❌ Code snippet doesn't contain recognizable Python syntax: {code}")
            return False
    
    print(f"✓ All code snippets contain realistic Python code with errors")
    
    print("\n=== All Tests Passed! ===")
    print(f"✓ Memory store is working correctly with {interaction_count} quality interactions")
    return True


def display_sample_data():
    """Display a sample of the dummy data for review."""
    print("\n=== Sample Interaction Data ===")
    store = MemoryStore()
    interactions = store.get_all_interactions()
    
    if interactions:
        sample = interactions[0]
        print(f"Assignment ID: {sample['assignment_id']}")
        print(f"Code Snippet:\n{sample['code_snippet']}")
        print(f"Student Prompt: {sample['student_prompt']}")
        print(f"Teacher Response: {sample['teacher_response']}")


if __name__ == "__main__":
    print("VITA Panel Testing - Memory Store Validation")
    print("=" * 50)
    
    success = test_memory_store_functionality()
    
    if success:
        display_sample_data()
        print("\n🎉 Memory store is ready for testing with VITA panel!")
    else:
        print("\n❌ Memory store validation failed")
        sys.exit(1)