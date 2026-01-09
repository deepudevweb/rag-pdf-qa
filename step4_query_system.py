import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("RAG SYSTEM - QUESTION ANSWERING BOT")
print("The Rise of Nationalism in Europe")
print("="*70)

print("\nInitializing RAG System...")

output_dir = r"C:\Users\sa\Desktop\rag-project\venv\output"

print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

print("Loading text chunks...")
with open(os.path.join(output_dir, "chunks.pkl"), 'rb') as f:
    chunks = pickle.load(f)

print("Loading vector database...")
index = faiss.read_index(os.path.join(output_dir, "faiss_index.bin"))

print(f"\nRAG System ready!")
print(f"Total knowledge chunks: {len(chunks)}")
print()

# Demo questions
questions = [
    "What year marks the beginning of nationalism in Europe?",
    "Who held power before the French Revolution?",
    "What is the Napoleonic Code?"
]

print("="*70)
print("DEMO MODE - Sample Questions")
print("="*70)

for i, question in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"QUESTION {i}: {question}")
    print('='*70)
    
    q_emb = model.encode([question], convert_to_numpy=True)
    distances, indices = index.search(q_emb.astype('float32'), 2)
    
    print("\nANSWER (Based on Chapter):")
    print("-"*70)
    
    for j, idx in enumerate(indices[0]):
        chunk = chunks[idx]
        print(f"\n{chunk}")
    
    print("\n" + "="*70)
    
    if i < len(questions):
        input("\nPress Enter for next question...")

print("\n" + "="*70)
print("DEMO COMPLETE! Now entering interactive mode...")
print("="*70)

# Interactive mode
print("\nYou can now ask your own questions!")
print("Type 'quit' or 'exit' to stop.\n")

while True:
    user_q = input("Your Question: ")
    
    if user_q.lower() in ['quit', 'exit', 'q', '']:
        print("\nThank you for using RAG System!")
        print("="*70)
        break
    
    print("\n" + "-"*70)
    print("ANSWER:")
    print("-"*70)
    
    try:
        q_emb = model.encode([user_q], convert_to_numpy=True)
        distances, indices = index.search(q_emb.astype('float32'), 2)
        
        for idx in indices[0]:
            print(f"\n{chunks[idx]}")
        
        print("\n" + "-"*70 + "\n")
        
    except Exception as e:
        print(f"Error: {e}\n")
