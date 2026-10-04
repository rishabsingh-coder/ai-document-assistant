import io
import numpy as np
import streamlit as st
from pypdf import PdfReader

from chunk_text import create_chunks
from embed_chunks import create_embeddings
from retrieve import retrieve_chunks
from qa_pipeline import generate_answer
from sentence_transformers import SentenceTransformer


st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide"
)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

st.title("📄 AI Document Assistant")
st.caption("Ask questions and get answers grounded in your uploaded document.")

st.sidebar.header("Document Assistant")

st.sidebar.write(
    "Upload a PDF and ask questions about its contents."
)

st.sidebar.markdown("---")

st.sidebar.subheader("How it works")
st.sidebar.write(
    "1. Upload a PDF\n"
    "2. The document is split into searchable chunks\n"
    "3. Relevant passages are retrieved\n"
    "4. The AI generates an answer using those passages"
)

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


@st.cache_data
def process_document(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    chunks = create_chunks(pages)
    embeddings = create_embeddings(chunks)

    return chunks, embeddings


if uploaded_file is not None:
    embedding_model = load_embedding_model()
    st.success(f"Loaded: {uploaded_file.name}")

    with st.spinner("Processing document..."):

        chunks, embeddings = process_document(
            uploaded_file.getvalue()
        )

    st.info(
        f"Document processed successfully — "
        f"{len(chunks)} searchable chunks created."
    )

    question = st.text_input(
        "Ask a question about the document:"
    )

    if st.button("Ask"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching the document..."):

                results = retrieve_chunks(
                    question,
                    chunks,
                    embeddings,
                    model=embedding_model,
                    top_k=3
                )

            with st.spinner("Generating answer..."):

                answer = generate_answer(
                    question,
                    results
                )

            st.subheader("Answer")

            st.markdown(answer)

            st.markdown("---")

            st.subheader("Sources")

            st.caption("The following passages were retrieved from your document.")

            for i, result in enumerate(results, start=1):

                with st.expander(
                    f"Source {i}  •  Page {result['page']}  •  "
                    f"Similarity {result['score']:.3f}"
                ):
                    st.write(result["text"])

else:

    st.info("Upload a PDF to get started.")