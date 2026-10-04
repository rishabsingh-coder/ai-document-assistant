import os
import json
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI

from retrieve import retrieve_chunks


CHUNKS_PATH = "data/chunks.json"
EMBEDDINGS_PATH = "data/embeddings.npy"

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(
        f"[Page {chunk['page']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the document context below.

If the answer cannot be found in the provided context, say:
"I could not find the answer in the document."

Do not use outside knowledge.
Do not make up information.

Give a concise final answer.

Document context:
{context}

User question:
{question}
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("Loading saved index...")

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = np.load(EMBEDDINGS_PATH)

    print("Index loaded successfully!")
    print("Chunks:", len(chunks))
    print("Embeddings shape:", embeddings.shape)

    question = input("\nAsk a question about the document: ")

    print("\nSearching the document...")

    results = retrieve_chunks(
        question,
        chunks,
        embeddings,
        top_k=3
    )

    print("\nGenerating answer...\n")

    answer = generate_answer(question, results)

    print("ANSWER:")
    print(answer)

    print("\nSOURCES:")

    for i, result in enumerate(results, start=1):
        print(
            f"\nSource {i} — Page {result['page']} "
            f"(score: {result['score']:.4f})"
        )
        print(result["text"])