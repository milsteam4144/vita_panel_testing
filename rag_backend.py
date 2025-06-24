from flask import Flask, request, jsonify
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load data
with open('data/sample_rag_data.json') as f:
    data = json.load(f)

# Prepare model and embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
texts = [d['student_question'] + " " + d['code_snippet'] for d in data]
embeddings = model.encode(texts, convert_to_numpy=True)

# Setup FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

app = Flask(__name__)

@app.route('/rag/ask', methods=['POST'])
def ask():
    user_q = request.json['question']
    user_emb = model.encode([user_q], convert_to_numpy=True)
    D, I = index.search(user_emb, k=1)
    match = data[I[0][0]]
    return jsonify({
        "answer": match['teacher_response'],
        "matched_assignment": match['assignment_id']
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
