# Design Decisions

## 1. Document Processing

The system processes one PDF document and extracts its text
page by page using `pypdf`.

Keeping the page number with each extracted section allows
the final answer to show where the information came from.

---

## 2. Chunking Experiment

I tested two chunking configurations.

### Configuration A — Baseline

- Chunk size: 500 characters
- Overlap: 0 characters
- Number of chunks: 13

### Configuration B — Overlapping Chunks

- Chunk size: 500 characters
- Overlap: 100 characters
- Number of chunks: 16

### Why test overlapping chunks?

Without overlap, an important piece of information can be
split between two neighboring chunks.

Using overlap allows some context from the end of one chunk
to appear at the beginning of the next chunk.

---

## 3. Retrieval Comparison

I tested Configuration B using several questions.

| Question | Top Page | Score | Relevant? |
|---|---:|---:|---|
| What are the opening hours of the Student Support Desk? | 1 | 0.7447 | Yes |
| What broad areas does GDG On Campus USAR organize learning activities in? | 1 | 0.8033 | Yes |
| Does attending a workshop automatically provide a certificate? | 1 | 0.7449 | Yes |
| What should a project repository include according to the handbook? | 2 | 0.5827 | Yes |
| Who is the current community lead? | 2 | 0.4152 | No answer in document |

The answerable questions retrieved passages containing
information relevant to the questions.

The unanswerable question produced a low similarity score
and the system responded that the answer could not be found
in the document.

---

## 4. Chunking Decision

I selected the overlapping configuration for the current
version of the project:

- 500-character chunks
- 100-character overlap

The main reason is that overlapping chunks preserve some
context between neighboring chunks and performed well on the
tested questions.

I did not select the configuration based only on similarity
scores. I also checked whether the retrieved passages actually
contained information relevant to the question.

---

## 5. Embedding Model

I used `all-MiniLM-L6-v2` to convert document chunks and
questions into numerical embeddings.

The embeddings are then compared using cosine-style similarity
through normalized vectors and a dot product.

---

## 6. Grounding

The LLM receives only the retrieved document passages as
context.

The prompt explicitly instructs the model:

- Use only the provided document context.
- Do not use outside knowledge.
- Do not make up information.
- State when the answer cannot be found.

This reduces the risk of unsupported answers.

---

## 7. Source Handling

Each retrieved chunk keeps its original PDF page number.

The final output displays:

- source page
- similarity score
- retrieved passage

This makes the answer easier to verify.

---