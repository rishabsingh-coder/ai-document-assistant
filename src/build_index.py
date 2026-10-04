import json
import numpy as np

from extract_text import extract_text_from_pdf
from chunk_text import create_chunks
from embed_chunks import create_embeddings


PDF_PATH = "data/document.pdf"

CHUNKS_PATH = "data/chunks.json"
EMBEDDINGS_PATH = "data/embeddings.npy"


if __name__ == "__main__":
    print("Loading document...")

    pages = extract_text_from_pdf(PDF_PATH)

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Saving chunks...")

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("Saving embeddings...")

    np.save(EMBEDDINGS_PATH, embeddings)

    print("\nIndex built successfully!")
    print("Chunks:", len(chunks))
    print("Embeddings shape:", embeddings.shape)