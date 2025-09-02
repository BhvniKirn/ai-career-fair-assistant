import os
import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

CHUNKS_PATH = os.path.join("data", "kb_chunks.jsonl")
EMB_PATH = os.path.join("data", "kb_embeddings.npy")

@dataclass
class Chunk:
    id: str
    source: str
    text: str

def _clean_text(t: str) -> str:
    return " ".join(t.split())

def pdf_to_text_chunks(pdf_path: str, max_chars: int = 900) -> List[Chunk]:
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        text.append(txt)
    full = _clean_text("\n".join(text))
    # simple fixed-size chunking
    chunks = []
    for i in range(0, len(full), max_chars):
        chunk_text = full[i:i+max_chars]
        if chunk_text.strip():
            chunks.append(Chunk(
                id=f"{os.path.basename(pdf_path)}#{i//max_chars}",
                source=os.path.basename(pdf_path),
                text=chunk_text.strip()
            ))
    return chunks

def build_kb_from_pdfs(pdf_dir: str = os.path.join("data","pdfs")) -> List[Chunk]:
    if not os.path.isdir(pdf_dir):
        return []
    all_chunks: List[Chunk] = []
    for fname in os.listdir(pdf_dir):
        if fname.lower().endswith(".pdf"):
            fpath = os.path.join(pdf_dir, fname)
            all_chunks.extend(pdf_to_text_chunks(fpath))
    return all_chunks

def save_chunks(chunks: List[Chunk], path: str = CHUNKS_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps({"id": ch.id, "source": ch.source, "text": ch.text}) + "\n")

def load_chunks(path: str = CHUNKS_PATH) -> List[Dict]:
    if not os.path.exists(path):
        return []
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items

def compute_and_save_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                                chunks_path: str = CHUNKS_PATH,
                                emb_path: str = EMB_PATH) -> None:
    chunks = load_chunks(chunks_path)
    if not chunks:
        np.save(emb_path, np.empty((0, 384), dtype=np.float32))
        return
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    X = model.encode(texts, normalize_embeddings=True)
    np.save(emb_path, X.astype(np.float32))

def retrieve(query: str, top_k: int = 5,
             chunks_path: str = CHUNKS_PATH, emb_path: str = EMB_PATH) -> List[Dict]:
    chunks = load_chunks(chunks_path)
    if not chunks:
        return []
    X = np.load(emb_path)
    if X.size == 0:
        return []
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    q = model.encode([query], normalize_embeddings=True)
    sims = cosine_similarity(q, X)[0]
    idx = np.argsort(-sims)[:top_k]
    results = []
    for i in idx:
        item = chunks[i].copy()
        item["score"] = float(sims[i])
        results.append(item)
    return results
