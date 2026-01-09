import gradio as gr
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Load system
print("🚀 Loading RAG system...")
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

with open(r"..\output\chunks.pkl", 'rb') as f:
    chunks = pickle.load(f)

index = faiss.read_index(r"..\output\faiss_index.bin")
print(f"✅ System ready! Loaded {len(chunks)} chunks")

def answer_question(question, num_results=2):
    if not question.strip():
        return "⚠️ Please enter a question."
    
    # Search
    q_emb = model.encode([question])
    distances, indices = index.search(q_emb, num_results)
    
    # Get best distance
    best_distance = float(distances[0][0])
    
    # Relevance threshold (ADJUST THIS!)
    THRESHOLD = 1.2  # Lower = stricter, Higher = more lenient
    
    # Check if question is relevant
    if best_distance > THRESHOLD:
        return f"""
# ❌ Cannot Answer This Question

**Sorry, this question doesn't seem to be related to the content in the document.**

---

### 📊 Technical Details:
- **Distance Score:** {best_distance:.3f}
- **Threshold:** {THRESHOLD}
- **Status:** Question is too far from document content

---

### 💡 Suggestions:

**Try asking questions about topics IN the document, such as:**

✅ What is nationalism?  
✅ Explain the French Revolution  
✅ Who was Giuseppe Mazzini?  
✅ What happened in 1848?  
✅ What is the Napoleonic Code?  

---

### 🔍 Why did this happen?

Your question **"{question}"** doesn't match any content in the uploaded PDF. 
This system only answers questions based on the document content.
"""
    
    # Good question - provide answer
    relevance_score = max(0, 100 - (best_distance * 50))
    
    answer = f"# 🎯 Question: {question}\n\n"
    answer += f"**Confidence:** {relevance_score:.1f}% | **Distance:** {best_distance:.3f}\n\n"
    answer += "="*70 + "\n\n"
    
    for i, idx in enumerate(indices[0]):
        dist = float(distances[0][i])
        rel_score = max(0, 100 - (dist * 50))
        
        answer += f"## 📄 Result {i+1}\n"
        answer += f"**Relevance:** {rel_score:.1f}%\n\n"
        answer += chunks[idx]
        answer += "\n\n" + "="*70 + "\n\n"
    
    return answer

# Create beautiful interface
with gr.Blocks(theme=gr.themes.Soft(), title="RAG PDF Q&A") as demo:
    
    gr.Markdown("""
    # 🎓 RAG PDF Question Answering System
    
    **Ask questions about the uploaded document!** The system will only answer 
    questions related to the content in the PDF.
    
    ⚠️ **Note:** Off-topic questions will be rejected to prevent wrong answers.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="📝 Your Question",
                placeholder="Example: What is nationalism?",
                lines=3
            )
            
            with gr.Accordion("⚙️ Settings", open=False):
                num_results = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=2,
                    step=1,
                    label="Number of results"
                )
            
            with gr.Row():
                submit_btn = gr.Button("🔍 Submit", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", size="lg")
        
        with gr.Column(scale=2):
            answer_output = gr.Markdown(
                value="""
# 👋 Welcome!

Enter your question on the left and click **Submit** to get started.

### 📚 About This System:
- Uses AI to search through your PDF document
- Returns relevant passages as answers
- Rejects off-topic questions
- Shows confidence scores

**Try an example question below!**
                """,
                label="Answer"
            )
    
    gr.Markdown("### 💡 Example Questions:")
    gr.Examples(
        examples=[
            ["What is nationalism?"],
            ["Explain the French Revolution"],
            ["Who was Giuseppe Mazzini?"],
            ["What happened in 1848?"],
            ["What is the Napoleonic Code?"]
        ],
        inputs=question_input
    )
    
    # Button actions
    submit_btn.click(
        fn=answer_question,
        inputs=[question_input, num_results],
        outputs=answer_output
    )
    
    question_input.submit(
        fn=answer_question,
        inputs=[question_input, num_results],
        outputs=answer_output
    )
    
    clear_btn.click(
        fn=lambda: ("", "👋 Question cleared! Enter a new question."),
        outputs=[question_input, answer_output]
    )
    
    gr.Markdown("""
    ---
    
    **Built with:** Gradio 🔥 | **Powered by:** sentence-transformers + FAISS
    
    [GitHub](https://github.com/deepudevweb/rag-pdf-qa) | 
    [Report Issue](https://github.com/deepudevweb/rag-pdf-qa/issues)
    """)

print("\n" + "="*70)
print("🌐 Starting web server...")
print("="*70 + "\n")

demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
