import json
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from content_extractor import ContentExtractor

class EnhancedRAGBackend:
    """Enhanced RAG backend using ChromaDB for instructor-created content."""
    
    def __init__(self, 
                 db_path: str = "./chroma_db", 
                 collection_name: str = "instructor_content",
                 embedding_model: str = 'all-MiniLM-L6-v2',
                 fallback_data_path: str = "data/dummy_data.json"):
        
        self.db_path = db_path
        self.collection_name = collection_name
        self.fallback_data_path = fallback_data_path
        
        # Initialize embedding model
        print("🔍 Loading embedding model...")
        self.model = SentenceTransformer(embedding_model)
        print("✅ Embedding model loaded")
        
        # Initialize ChromaDB
        print("🔍 Initializing ChromaDB...")
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
            print(f"✅ Connected to existing collection '{collection_name}'")
        except:
            self.collection = self.client.create_collection(collection_name)
            print(f"✅ Created new collection '{collection_name}'")
            
        # Load fallback data for compatibility
        self.fallback_data = self._load_fallback_data()
        
    def _load_fallback_data(self) -> List[Dict]:
        """Load the original dummy data as fallback."""
        try:
            with open(self.fallback_data_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load fallback data: {e}")
            return []
    
    def populate_database(self, force_refresh: bool = False) -> None:
        """Extract content from instructor_created_data and populate ChromaDB."""
        
        # Check if database already has content
        existing_count = self.collection.count()
        if existing_count > 0 and not force_refresh:
            print(f"📚 Database already contains {existing_count} documents. Use force_refresh=True to rebuild.")
            return
            
        if force_refresh and existing_count > 0:
            print("🔄 Clearing existing collection...")
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)
        
        print("📚 Extracting content from instructor_created_data...")
        extractor = ContentExtractor()
        chunks = extractor.extract_all_content()
        
        if not chunks:
            print("⚠️ No content extracted. Check instructor_created_data directory.")
            return
            
        print(f"🔍 Processing {len(chunks)} content chunks...")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk['content'])
            metadatas.append({
                'source_file': chunk['source_file'],
                'chunk_type': chunk['chunk_type'],
                'chunk_id': chunk['chunk_id'],
                'metadata': json.dumps(chunk['metadata'])  # Store as JSON string
            })
            ids.append(f"chunk_{i}")
        
        # Add to ChromaDB in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                ids=batch_ids
            )
            
        print(f"✅ Successfully added {len(documents)} documents to ChromaDB")
        
    def query(self, question: str, k: int = 3) -> List[Dict[str, Any]]:
        """Query the enhanced RAG system for relevant content."""
        
        # First try ChromaDB
        chroma_results = self._query_chromadb(question, k)
        
        # If ChromaDB has good results, use those
        if chroma_results:
            return chroma_results
            
        # Fallback to original dummy data
        print("🔄 Falling back to original dummy data...")
        return self._query_fallback(question, k)
    
    def _query_chromadb(self, question: str, k: int) -> List[Dict[str, Any]]:
        """Query ChromaDB for relevant content."""
        try:
            db_count = self.collection.count()
            if db_count == 0:
                print("📚 ChromaDB is empty. Try running populate_database() first.")
                return []
                
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[question],
                n_results=min(k, db_count)
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    metadata = results['metadatas'][0][i]
                    
                    # Extract a preview of the content
                    content = results['documents'][0][i]
                    preview = content[:200] + "..." if len(content) > 200 else content
                    
                    result = {
                        'answer': content,  # Full content for LLM
                        'content_preview': preview,  # Preview for display
                        'source_file': metadata['source_file'],
                        'chunk_type': metadata['chunk_type'],
                        'chunk_id': metadata['chunk_id'],
                        'distance': results['distances'][0][i] if results['distances'] else None,
                        'source_type': 'instructor_content'
                    }
                    formatted_results.append(result)
                    
            return formatted_results
            
        except Exception as e:
            print(f"⚠️ Error querying ChromaDB: {e}")
            return []
    
    def _query_fallback(self, question: str, k: int) -> List[Dict[str, Any]]:
        """Query the original dummy data as fallback."""
        try:
            if not self.fallback_data:
                return []
                
            # Simple embedding-based search on fallback data
            texts = [d['student_question'] + " " + d.get('code_snippet', '') for d in self.fallback_data]
            
            if not texts:
                return []
                
            # Get embeddings
            user_emb = self.model.encode([question])
            text_embs = self.model.encode(texts)
            
            # Calculate similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(user_emb, text_embs)[0]
            
            # Get top k matches
            top_indices = similarities.argsort()[-k:][::-1]
            
            results = []
            for idx in top_indices:
                match = self.fallback_data[idx]
                results.append({
                    "answer": match['teacher_response'],
                    "content_preview": match['teacher_response'][:200] + "..." if len(match['teacher_response']) > 200 else match['teacher_response'],
                    "source_file": "data/dummy_data.json",
                    "matched_assignment": match.get('assignment_id', None),
                    "matched_code": match.get('code_snippet', None),
                    "student_question": match.get('student_question', None),
                    "source_type": "fallback_data"
                })
            return results
            
        except Exception as e:
            print(f"⚠️ Error in fallback query: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the current database."""
        try:
            count = self.collection.count()
            
            # Get sample of metadata to understand content types
            if count > 0:
                sample = self.collection.get(limit=min(10, count))
                chunk_types = {}
                source_files = set()
                
                for meta in sample['metadatas']:
                    chunk_type = meta.get('chunk_type', 'unknown')
                    chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
                    source_files.add(meta.get('source_file', 'unknown'))
                
                return {
                    'total_chunks': count,
                    'chunk_types': chunk_types,
                    'source_files': list(source_files)[:10],  # Show first 10
                    'total_source_files': len(source_files)
                }
            else:
                return {'total_chunks': 0}
                
        except Exception as e:
            return {'error': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced RAG backend
    rag = EnhancedRAGBackend()
    
    # Populate database
    rag.populate_database()
    
    # Get stats
    stats = rag.get_database_stats()
    print(f"\nDatabase stats: {stats}")
    
    # Test query
    results = rag.query("How do I use for loops in Python?")
    print(f"\nQuery results: {len(results)} matches found")
    for i, result in enumerate(results[:2]):
        print(f"\nMatch {i+1}:")
        print(f"File: {result['source_file']}")
        print(f"Preview: {result['content_preview']}")