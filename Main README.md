# 🎓 RAG PDF Question Answering System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

AI-powered PDF Question Answering using RAG (Retrieval-Augmented Generation).

## 🌟 Features

- ✅ Extract text from any PDF
- ✅ AI semantic search with sentence-transformers
- ✅ Fast FAISS vector search
- ✅ Interactive Q&A system
- ✅ Works offline (no API keys)

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/deepudevweb/rag-pdf-qa.git
cd rag-pdf-qa

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Add your PDF
cp your_file.pdf data/chapter.pdf

# Run system
python step1_extract_text.py
python step2_create_embeddings.py
python step3_setup_rag.py
python step4_query_system.py
