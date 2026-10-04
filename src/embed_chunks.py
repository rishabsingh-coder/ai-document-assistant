from sentence_transformers import SentenceTransformer
from extract_text import extract_text_from_pdf
from chunk_text import create_chunks

PDF_PATH = "data/document.pdf"
MODEL_NAME = "all-MiniLM-L6-v2"


def create_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    chunks = create_chunks(pages)

    embeddings = create_embeddings(chunks)

    print("Number of chunks:", len(chunks))
    print("Embedding shape:", embeddings.shape)

    print("\nFirst embedding (first 10 values):")
    print(embeddings[0][:10])