# 🎓 RAG PDF Question Answering System

AI-powered system for answering questions from PDF documents using Retrieval-Augmented Generation (RAG).

## 🌟 Features

- ✅ Extract and process PDF documents
- ✅ AI-powered semantic search
- ✅ Fast vector search with FAISS
- ✅ Interactive Q&A system
- ✅ Works offline (no API keys needed)

## 🌐 Web Interface

Launch the web interface:

```bash
pip install gradio
python app.py


## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Extract text from PDF
python step1_extract_text.py

# Step 2: Create embeddings
python step2_create_embeddings.py

# Step 3: Setup RAG system
python step3_setup_rag.py

# Step 4: Start asking questions
python step4_query_system.py


📖 How It Works
Extract: PDF text extraction

Chunk: Split into segments

Embed: Convert to vector representations

Index: Store in FAISS database

Query: Ask questions

Retrieve: Get relevant answers

🛠️ Technologies
Python 3.8+

sentence-transformers

FAISS

PyPDF2

NumPy

Your Question: What is nationalism?

ANSWER:
Nationalism is a political ideology that emerged in 19th century 
Europe, representing the belief that nations should be self-governing...
