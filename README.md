## <img width="2156" height="1937" alt="rag_architecture_diagram" src="https://github.com/user-attachments/assets/8d81fcd4-be84-42a0-8fa5-983cacf68d83" />
🤖 Production RAG Documentation Assistant


A production-oriented Retrieval-Augmented Generation (RAG) system for technical documentation — built with hybrid retrieval, an evaluation pipeline, and full deployment on HuggingFace Spaces.

> **Live Demo:** [https://huggingface.co/spaces/islam9889/rag-docs-assistant]

---

## 🚀 Overview

This project indexes 120+ technical documentation pages and provides grounded conversational answers with source citations. It goes beyond a standard tutorial RAG chatbot by adding hybrid retrieval reranking, latency tracking, and a retrieval evaluation framework.

**Docs indexed:**
- Python standard library & tutorial (40 pages)
- FastAPI documentation (30 pages)
- LangChain documentation (30 pages)
- LlamaIndex documentation (20 pages)

---

## 🏗️ System Architecture

```text
┌─────────────────────┐
│  Technical Documents │  (120+ pages: Python, FastAPI, LangChain, LlamaIndex)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Chunking Pipeline   │  (~512 token chunks, 128 token overlap)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  BGE Embeddings      │  (BAAI/bge-small-en-v1.5)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ChromaDB Vector DB  │  (Persistent, pre-built index)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Semantic Retrieval  │  (Top-K similarity search)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Hybrid Reranking    │  (Semantic score + keyword overlap)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Groq LLM Generation │  (Llama 3.3 70B, low-latency inference)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Gradio Chat UI      │  (Source citations, chat history export)
└─────────────────────┘
```

---

## ✨ Key Features

### 🔍 Hybrid Retrieval
Standard RAG uses pure vector similarity search, which can miss exact keyword matches. This system combines:
- **Semantic search** — BGE embeddings find conceptually similar content
- **Keyword reranking** — boosts chunks with direct term overlap

Result: better retrieval on specific technical queries (function names, method signatures, library-specific terminology).

### 📊 Evaluation Pipeline
Built a lightweight evaluation framework (`evaluation.py`) that measures retrieval quality without requiring human labels:
- **Relevance score** — keyword overlap between question and retrieved chunks (0.0–1.0)
- **Latency tracking** — end-to-end response time per query

This allows objective comparison of retrieval strategies, not just subjective "does it look right" testing.

### 📚 Source-Grounded Responses
Every answer includes the source documents used for generation — enabling answer verification and reducing blind trust in LLM outputs.

```
📚 Sources:
1. fastapi_tutorial_endpoints.txt
2. python_decorators.txt
3. llamaindex_retrieval.txt
```

### ⚡ Low-Latency Inference
Groq-hosted Llama 3.3 70B delivers sub-second generation. Average end-to-end latency across evaluation set: **0.66s**.

---

## 📊 Evaluation Results

Evaluation run on 5 held-out questions not seen during indexing:

| Question | Relevance Score | Latency |
|---|---|---|
| What is a Python decorator? | 0.67 | 1.39s |
| What is FastAPI? | 1.00 | 0.25s |
| What is RAG in LLMs? | 0.67 | 0.34s |
| How do I create a POST endpoint? | 0.83 | 0.52s |
| What are LangChain chains? | 0.72 | 0.80s |
| **Average** | **0.78** | **0.66s** |

> **Relevance score** = keyword overlap ratio between the question terms and retrieved source chunks. A score of 1.0 means all question keywords appeared in retrieved documents.

---

## 📈 How This Differs From a Tutorial RAG

| Feature | Tutorial RAG | This Project |
|---|---|---|
| Retrieval | Pure vector similarity | Hybrid (semantic + keyword) |
| Evaluation | None | Automated relevance + latency scoring |
| Source attribution | Optional | Built-in, every response |
| Deployment | Local notebook | HuggingFace Spaces |
| Vector store | In-memory | Persistent ChromaDB |
| Architecture | Single script | Modular (app, evaluation, vectorstore) |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq + Llama 3.3 70B |
| RAG Framework | LlamaIndex |
| Vector Database | ChromaDB (persistent) |
| Embeddings | BAAI/bge-small-en-v1.5 |
| UI | Gradio |
| Deployment | HuggingFace Spaces |
| Language | Python 3.10+ |

---

## 📂 Project Structure

```
.
├── app.py              # Gradio UI + RAG query logic
├── evaluation.py       # Retrieval evaluation pipeline
├── requirements.txt    # Dependencies
├── vectorstore/        # Pre-built ChromaDB index
│   ├── chroma.sqlite3
│   └── ...
└── README.md
```

---

## ▶️ Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY=your_api_key_here

# Run the app
python app.py
```

---

## 🧪 Running the Evaluation

```bash
python evaluation.py
```

Output:
```
Q: What is a Python decorator?
Score: 0.67 | Latency: 1.39s

====== FINAL RESULTS ======
Avg Score: 0.78
Avg Latency: 0.66s
```

---

## 🔮 Future Improvements

- Cross-encoder reranking (e.g. `bge-reranker-base`)
- Multi-query retrieval for complex questions
- Streaming responses
- LangSmith tracing and observability
- Dockerized deployment
- Conversation memory across sessions

---

## 👨‍💻 Author

**Islam Khaled** — ML Engineer, NLP & Generative AI
[LinkedIn](https://www.linkedin.com/in/islam-khaled-129715367) · [HuggingFace](https://huggingface.co/islam9889)
