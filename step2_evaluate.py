# step2_evaluate.py - Answers ko evaluate karo

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import json

print("🚀 RAG Answer Evaluator Starting...\n")

# Step 1: Chapter text load karo
print("📖 Chapter text load kar rahe hain...")
with open("chapter_text.txt", "r", encoding="utf-8") as f:
    chapter_text = f.read()
print(f"✓ Chapter loaded ({len(chapter_text)} characters)\n")

# Step 2: Text ko chunks mein split karo
print("✂️ Text ko chunks mein split kar rahe hain...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_text(chapter_text)
print(f"✓ {len(chunks)} chunks create ho gaye\n")

# Step 3: Embeddings create karo
print("🤖 Embeddings model load kar rahe hain...")
print("⏳ (Pehli baar thoda time lagega - model download hoga ~500MB)")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)
print("✓ Embeddings model ready\n")

# Step 4: Vector database create karo
print("🗄️ Vector database create kar rahe hain...")
vector_store = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("✓ Vector database ready\n")

# Step 5: Student answers load karo
print("📝 Student answers load kar rahe hain...")
with open("student_answers.txt", "r", encoding="utf-8") as f:
    answers_text = f.read()

# Simple split (double newline se)
answers_list = [a.strip() for a in answers_text.split("\n\n") if a.strip() and len(a.strip()) > 20]
print(f"✓ {len(answers_list)} answers milein\n")

# Step 6: Har answer ko evaluate karo
print("🔍 Answers evaluate kar rahe hain...\n")
results = []

for i, answer in enumerate(answers_list, 1):
    print(f"Evaluating Answer {i}/{len(answers_list)}...")
    
    # Similar chunks dhundo
    similar_docs = vector_store.similarity_search_with_score(answer, k=5)
    
    # Scores calculate karo
    scores = [1 / (1 + distance) for _, distance in similar_docs]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Accuracy calculate karo (threshold 0.3)
    relevant_count = sum(1 for s in scores if s >= 0.3)
    accuracy = (relevant_count / len(scores)) * 100
    
    results.append({
        "question": i,
        "accuracy": round(accuracy, 2),
        "relevance": round(avg_score, 4)
    })
    
    print(f"  ✓ Accuracy: {accuracy:.2f}%\n")

# Step 7: Overall results calculate karo
overall_accuracy = sum(r['accuracy'] for r in results) / len(results) if results else 0

print("="*60)
print("📊 FINAL RESULTS")
print("="*60)
print(f"Total Questions: {len(results)}")
print(f"Overall Accuracy: {overall_accuracy:.2f}%\n")

for r in results:
    print(f"Question {r['question']}: {r['accuracy']}%")

# Save results
output = {
    "overall_accuracy": round(overall_accuracy, 2),
    "total_questions": len(results),
    "results": results
}

with open("results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n💾 Results saved to: results.json")
print("\n✅ EVALUATION COMPLETE!")
