# 🤖 RAG Documentation System

A production-ready **Retrieval-Augmented Generation (RAG)** system for querying technical documentation. Built with LlamaIndex, ChromaDB, and Groq LLM.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Features

- **Multi-Source Documentation**: Queries Python, FastAPI, LangChain, and LlamaIndex docs
- **Persistent Vector Store**: ChromaDB for fast retrieval
- **Context-Aware Responses**: Chat history integration
- **Interactive UI**: Clean Gradio interface
- **Source Attribution**: Automatic citation of relevant documents
- **Export Functionality**: Save conversations for reference

---

## 🏗️ Architecture

```
User Question → Query Engine → Vector Store → LLM → Response + Sources
                                    ↓
                            120+ Embedded Documents
```

**Tech Stack:**

- **LLM**: Groq Llama 3.3 70B (fast inference)
- **Embeddings**: BGE-small-en-v1.5 (efficient & accurate)
- **Vector DB**: ChromaDB (persistent storage)
- **Framework**: LlamaIndex (orchestration)
- **UI**: Gradio (interactive chat)


## 🚀 Usage

### Option 1: Quick Start (Use Pre-scraped Docs)

If you already have the scraped documents:

```bash
# Build the vector store (5-10 minutes, one-time)
python scripts/build_index.py

# Launch the app
python app/gradio_app.py
```

Open browser at `http://localhost:7860`

### Option 2: Scrape Fresh Documentation

```bash
# Scrape documentation (20-30 minutes)
python scripts/scrape_docs.py

# Build index
python scripts/build_index.py

# Launch app
python app/gradio_app.py
```

---


## 📊 Performance

- **Response Time**: ~2-3 seconds per query
- **Documents**: 120+ technical documentation pages
- **Vector Store Size**: ~50MB
- **Embedding Time**: 5-10 minutes (one-time)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Your Name**

- GitHub: [islam9888]
  (https://github.com/islam9888)
- LinkedIn: [islam-khaled-129715367]
   (www.linkedin.com/in/islam-khaled-129715367)

---

## 🙏 Acknowledgments

- [LlamaIndex](https://www.llamaindex.ai/) for the RAG framework
- [Groq](https://groq.com/) for fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector storage
- Official documentation sources: Python, FastAPI, LangChain, LlamaIndex

---

**⭐ If you find this project useful, please give it a star!**
