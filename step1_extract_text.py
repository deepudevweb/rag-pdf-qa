# -*- coding: utf-8 -*-
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    print("Step 1: Extracting text from PDF...")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            print(f"   Page {page_num + 1} extracted")
    
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "chapter_text.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Text extracted successfully!")
    print(f"Saved to: {output_file}")
    print(f"Total characters: {len(text)}")
    return text

if __name__ == "__main__":
    pdf_path = r"C:\Users\sa\Desktop\rag-project\venv\data\chapter.pdf"
    
    if not os.path.exists(pdf_path):
        print("ERROR: PDF file not found!")
        print(f"Looking for: {pdf_path}")
    else:
        extract_text_from_pdf(pdf_path)
