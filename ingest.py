from utils.rag import build_kb_from_pdfs, save_chunks, compute_and_save_embeddings
import os

if __name__ == "__main__":
    pdf_dir = os.path.join("data", "pdfs")
    print(f"Looking for PDFs in: {pdf_dir}")
    chunks = build_kb_from_pdfs(pdf_dir)
    print(f"Extracted {len(chunks)} chunks.")
    save_chunks(chunks)
    compute_and_save_embeddings()
    print("Knowledge base ready: data/kb_chunks.jsonl + data/kb_embeddings.npy")
