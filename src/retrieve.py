import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def retrieve_chunks(question, chunks, embeddings, model=None, top_k=3):
    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    scores = np.dot(embeddings, question_embedding)

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "page": chunks[index]["page"],
            "text": chunks[index]["text"],
            "score": float(scores[index])
        })

    return results