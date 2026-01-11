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

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com/keys))

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/rag-documentation-system.git
cd rag-documentation-system
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

---

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

## 💬 Example Queries

Try asking:

- _"What is a Python decorator and how do I use it?"_
- _"How do I create a FastAPI endpoint with path parameters?"_
- _"Explain LangChain chains"_
- _"What's the difference between VectorStoreIndex and ListIndex in LlamaIndex?"_

---

## 📁 Project Structure

```
rag_documentation_system/
├── app/
│   └── gradio_app.py          # Gradio UI
├── src/
│   ├── config.py              # Configuration
│   ├── scraper.py             # Web scraping
│   ├── indexer.py             # Vector store indexing
│   ├── query_engine.py        # RAG query logic
│   └── utils.py               # Utilities
├── scripts/
│   ├── scrape_docs.py         # Scrape documentation
│   ├── build_index.py         # Build vector store
│   └── run_app.py             # Launch application
├── data/
│   └── raw_docs/              # Scraped documents
├── vectorstore/               # ChromaDB storage
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Configuration

Edit `src/config.py` or use environment variables:

```python
# Model settings
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128
SIMILARITY_TOP_K = 3

# Paths
BASE_PATH = "./rag_project"
```

---

## 📊 Performance

- **Response Time**: ~2-3 seconds per query
- **Documents**: 120+ technical documentation pages
- **Vector Store Size**: ~50MB
- **Embedding Time**: 5-10 minutes (one-time)

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific module
pytest tests/test_query_engine.py -v
```

---

## 🔧 Troubleshooting

**Issue**: `GROQ_API_KEY not found`

- **Solution**: Ensure `.env` file exists with valid API key

**Issue**: Slow embedding creation

- **Solution**: Normal for first run. Subsequent runs load from disk.

**Issue**: Out of memory

- **Solution**: Reduce `CHUNK_SIZE` in config or process fewer documents

---

## 🚀 Deployment

### Hugging Face Spaces

1. Create new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Gradio** SDK
3. Add `GROQ_API_KEY` to Space secrets
4. Push code to Space repository

### Local Production

```bash
# Using gunicorn (recommended)
pip install gunicorn
gunicorn app.gradio_app:main --bind 0.0.0.0:7860
```

---

## 📈 Future Improvements

- [ ] Add more documentation sources
- [ ] Implement user feedback loop
- [ ] Add multi-language support
- [ ] Integrate document upload feature
- [ ] Add authentication
- [ ] Implement caching for common queries

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 👤 Author

**Your Name**

- GitHub: [islam9888]
  (https://github.com/islam9888)
- LinkedIn: [islam-khaled-129715367](www.linkedin.com/in/islam-khaled-129715367)

---

## 🙏 Acknowledgments

- [LlamaIndex](https://www.llamaindex.ai/) for the RAG framework
- [Groq](https://groq.com/) for fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector storage
- Official documentation sources: Python, FastAPI, LangChain, LlamaIndex

---

**⭐ If you find this project useful, please give it a star!**
