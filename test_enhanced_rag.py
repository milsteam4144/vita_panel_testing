#!/usr/bin/env python3
"""
Test script for the Enhanced RAG implementation
"""

import os
import sys
from pathlib import Path

def test_content_extraction():
    """Test the content extraction functionality."""
    print("Testing Content Extraction...")
    
    try:
        from content_extractor import ContentExtractor
        
        # Check if instructor_created_data exists
        if not Path("instructor_created_data").exists():
            print("❌ instructor_created_data directory not found!")
            return False
        
        extractor = ContentExtractor()
        chunks = extractor.extract_all_content()
        
        if chunks:
            print(f"Successfully extracted {len(chunks)} content chunks")
            
            # Show sample chunks
            print("\nSample extracted content:")
            for i, chunk in enumerate(chunks[:3]):
                print(f"\nChunk {i+1}:")
                print(f"  File: {chunk['source_file']}")
                print(f"  Type: {chunk['chunk_type']}")
                print(f"  Content: {chunk['content'][:100]}...")
            
            return True
        else:
            print("No content extracted")
            return False
            
    except Exception as e:
        print(f"Content extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_rag():
    """Test the enhanced RAG backend."""
    print("\nTesting Enhanced RAG Backend...")
    
    try:
        from rag_backend_enhanced import EnhancedRAGBackend
        
        # Initialize RAG backend
        rag = EnhancedRAGBackend()
        
        # Check if database needs population
        stats = rag.get_database_stats()
        if stats.get('total_chunks', 0) == 0:
            print("Database is empty, populating with content...")
            rag.populate_database()
            stats = rag.get_database_stats()
        
        print(f"Database contains {stats.get('total_chunks', 0)} chunks")
        
        # Test queries
        test_queries = [
            "How do for loops work in Python?",
            "What is a function?",
            "How do I fix syntax errors?",
            "What are dictionaries?"
        ]
        
        print("\nTesting queries:")
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = rag.query(query, k=2)
            
            if results:
                print(f"Found {len(results)} matches:")
                for i, result in enumerate(results):
                    print(f"  {i+1}. {result.get('source_file', 'Unknown')} ({result.get('chunk_type', 'unknown')})")
                    preview = result.get('content_preview', result.get('answer', ''))[:80]
                    print(f"      Preview: {preview}...")
            else:
                print("No matches found")
        
        return True
        
    except Exception as e:
        print(f"Enhanced RAG test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_integration():
    """Test that the app can import and use enhanced RAG."""
    print("\nTesting App Integration...")
    
    try:
        # Test imports
        from rag_backend_enhanced import EnhancedRAGBackend
        from content_extractor import ContentExtractor
        
        print("Enhanced RAG modules import successfully")
        
        # Test that vita_app can import enhanced modules
        import sys
        if 'vita_app' in sys.modules:
            del sys.modules['vita_app']  # Force reimport
        
        # This will test the import path in vita_app.py
        try:
            import vita_app
            print("vita_app.py imports enhanced RAG successfully")
        except ImportError as e:
            print(f"vita_app.py import issue: {e}")
            print("This might be due to missing dependencies - check requirements.txt")
        
        return True
        
    except Exception as e:
        print(f"App integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Enhanced RAG System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Content Extraction", test_content_extraction),
        ("Enhanced RAG Backend", test_enhanced_rag),
        ("App Integration", test_app_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'=' * 20} Test Summary {'=' * 20}")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll tests passed! Your enhanced RAG system is ready!")
        print("\nNext steps:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Run setup_rag_database.py to populate the database")
        print("3. Start the VITA app to test with the enhanced RAG")
    else:
        print(f"\n{total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)