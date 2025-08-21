#!/usr/bin/env python3
"""
Quick test script for RAG integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the RAG functionality from the main app
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def test_rag():
    try:
        # Initialize RAG backend (same as in vita_app.py)
        data_path = "data/dummy_data.json"
        with open(data_path) as f:
            data = json.load(f)
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        texts = [d['student_question'] + " " + d['code_snippet'] for d in data]
        embeddings = model.encode(texts, convert_to_numpy=True)
        
        # Build FAISS index
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        
        # Test query function
        def query(question, k=1):
            user_emb = model.encode([question], convert_to_numpy=True)
            D, I = index.search(user_emb, k)
            results = []
            for idx in I[0]:
                match = data[idx]
                results.append({
                    "answer": match['teacher_response'],
                    "matched_assignment": match.get('assignment_id', None),
                    "matched_code": match.get('code_snippet', None),
                    "student_question": match.get('student_question', None)
                })
            return results
        
        # Test queries
        test_questions = [
            "How does factorial work?",
            "What does a for loop do?",
            "How do I add to a list?"
        ]
        
        print("🧪 Testing RAG queries:")
        for q in test_questions:
            results = query(q, k=1)
            print(f"\n❓ Question: {q}")
            print(f"📚 Best match: {results[0]['student_question']}")
            print(f"💡 Answer: {results[0]['answer'][:100]}...")
        
        print("\n✅ RAG integration test successful!")
        return True
        
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        return False

if __name__ == "__main__":
    test_rag()
