#!/usr/bin/env python3
"""
Setup script for the Enhanced RAG Database
This script will extract content from instructor_created_data and populate ChromaDB.
"""

import os
import sys
from pathlib import Path
from rag_backend_enhanced import EnhancedRAGBackend

def main():
    print("🚀 VITA Enhanced RAG Database Setup")
    print("=" * 50)
    
    # Check if instructor_created_data exists
    if not Path("instructor_created_data").exists():
        print("❌ Error: instructor_created_data directory not found!")
        print("Please ensure you're running this from the project root directory.")
        return False
    
    try:
        # Initialize the enhanced RAG backend
        print("🔍 Initializing Enhanced RAG Backend...")
        rag = EnhancedRAGBackend()
        
        # Populate the database
        print("📚 Extracting and indexing content...")
        rag.populate_database(force_refresh=True)
        
        # Get and display statistics
        print("\n📊 Database Statistics:")
        stats = rag.get_database_stats()
        
        if 'error' in stats:
            print(f"❌ Error getting stats: {stats['error']}")
            return False
            
        print(f"  • Total content chunks: {stats.get('total_chunks', 0)}")
        print(f"  • Source files processed: {stats.get('total_source_files', 0)}")
        
        if 'chunk_types' in stats:
            print("  • Content types found:")
            for chunk_type, count in stats['chunk_types'].items():
                print(f"    - {chunk_type}: {count}")
        
        if 'source_files' in stats and stats['source_files']:
            print("  • Sample source files:")
            for file in stats['source_files'][:5]:  # Show first 5
                print(f"    - {file}")
        
        # Test with a sample query
        print("\n🧪 Testing with sample query...")
        test_results = rag.query("How do Python for loops work?", k=2)
        
        if test_results:
            print(f"✅ Query test successful! Found {len(test_results)} relevant matches:")
            for i, result in enumerate(test_results):
                print(f"  {i+1}. {result['source_file']} ({result.get('chunk_type', 'unknown')})")
                print(f"     Preview: {result['content_preview'][:100]}...")
        else:
            print("⚠️ Query test returned no results")
        
        print("\n🎉 RAG Database setup completed successfully!")
        print("You can now run the VITA app with enhanced RAG capabilities.")
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)