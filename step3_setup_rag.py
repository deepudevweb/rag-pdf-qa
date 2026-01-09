import faiss
import pickle
import os
import numpy as np

print("="*70)
print("STEP 3: SETUP VECTOR DATABASE")
print("="*70)

embeddings_file = r"C:\Users\sa\Desktop\rag-project\venv\output\embeddings.pkl"

if not os.path.exists(embeddings_file):
    print("ERROR: Embeddings not found!")
    print("Run step2_create_embeddings.py first")
    exit()

print("\nLoading embeddings...")
with open(embeddings_file, 'rb') as f:
    embeddings = pickle.load(f)

print(f"Loaded embeddings: {embeddings.shape}")

print("\nCreating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

print(f"Index dimension: {dimension}")

print("\nAdding embeddings to index...")
index.add(np.array(embeddings).astype('float32'))

print(f"Added {index.ntotal} vectors")

print("\nSaving index...")
output_dir = r"C:\Users\sa\Desktop\rag-project\venv\output"
faiss.write_index(index, os.path.join(output_dir, "faiss_index.bin"))

print("Index saved successfully!")

print("\n" + "="*70)
print("STEP 3 COMPLETE!")
print(f"Vector Database ready with {index.ntotal} indexed vectors!")
print("="*70)
