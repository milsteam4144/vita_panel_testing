import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGBackend:
    def __init__(self, data_path="dummy_data.json", embedding_model='all-MiniLM-L6-v2'):
        # Load data
        with open(data_path) as f:
            self.data = json.load(f)
        # Prepare model and embeddings
        self.model = SentenceTransformer(embedding_model)
        self.texts = [d['student_question'] + " " + d['code_snippet'] for d in self.data]
        self.embeddings = self.model.encode(self.texts, convert_to_numpy=True)
        # Build FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def query(self, question, k=1):
        """Return the best-matching data entries for the question."""
        user_emb = self.model.encode([question], convert_to_numpy=True)
        D, I = self.index.search(user_emb, k)
        results = []
        for idx in I[0]:
            match = self.data[idx]
            results.append({
                "answer": match['teacher_response'],
                "matched_assignment": match.get('assignment_id', None),
                "matched_code": match.get('code_snippet', None),
                "student_question": match.get('student_question', None)
            })
        return results

# Example usage (uncomment to test directly):
# if __name__ == "__main__":
#     rag = RAGBackend("dummy_data.json")
#     user_q = "How does the factorial code work?"
#     print(rag.query(user_q))