from extract_text import extract_text_from_pdf

PDF_PATH = "data/document.pdf"


def create_chunks(pages, chunk_size=500, overlap=100):
    chunks = []

    for page in pages:
        text = page["text"]

        start = 0

        while start < len(text):
            chunk_text = text[start:start + chunk_size]

            chunks.append({
                "page": page["page"],
                "text": chunk_text
            })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    chunks = create_chunks(pages)

    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks[:5], start=1):
        print(f"\n--- Chunk {i} | Page {chunk['page']} ---")
        print(chunk["text"])