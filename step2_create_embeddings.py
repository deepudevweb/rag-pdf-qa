import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

from sentence_transformers import SentenceTransformer
import pickle
import numpy as np

print("="*70)
print("STEP 2: CREATE EMBEDDINGS")
print("="*70)

print("\nLoading text file...")
text_file = r"C:\Users\sa\Desktop\rag-project\venv\output\chapter_text.txt"

if not os.path.exists(text_file):
    print("ERROR: File not found!")
    exit()

with open(text_file, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Text loaded: {len(text)} characters")

print("\nCreating chunks...")
words = text.split()
chunks = []

for i in range(0, len(words), 450):
    chunk = ' '.join(words[i:i + 500])
    if chunk.strip():
        chunks.append(chunk)

print(f"Created {len(chunks)} chunks")

print("\nLoading AI model (first time may take 1 minute)...")

try:
    import warnings
    warnings.filterwarnings('ignore')
    
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    print("Model loaded successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative method...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded with alternative method!")
    except:
        print("FAILED! Please reinstall sentence-transformers")
        exit()

print("\nGenerating embeddings (this takes 1-2 minutes)...")

try:
    embeddings = []
    for i, chunk in enumerate(chunks):
        emb = model.encode([chunk], convert_to_numpy=True)
        embeddings.append(emb[0])
        if (i+1) % 5 == 0:
            print(f"  Processed {i+1}/{len(chunks)} chunks...")
    
    embeddings = np.array(embeddings)
    print(f"\nEmbeddings created!")
    print(f"Shape: {embeddings.shape}")
    
except Exception as e:
    print(f"Error creating embeddings: {e}")
    exit()

print("\nSaving data...")
output_dir = r"C:\Users\sa\Desktop\rag-project\venv\output"

with open(os.path.join(output_dir, "chunks.pkl"), 'wb') as f:
    pickle.dump(chunks, f)

with open(os.path.join(output_dir, "embeddings.pkl"), 'wb') as f:
    pickle.dump(embeddings, f)

print("Data saved successfully!")
print("\n" + "="*70)
print("STEP 2 COMPLETE!")
print("="*70)
