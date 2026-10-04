from pypdf import PdfReader

PDF_PATH = "data/document.pdf"


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


if __name__ == "__main__":
    pages = extract_text_from_pdf(PDF_PATH)

    print(f"Total pages with text: {len(pages)}")

    for page in pages:
        print("\n--- Page", page["page"], "---")
        print(page["text"])