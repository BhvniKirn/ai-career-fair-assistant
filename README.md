

# ai-career-fair-assistant
An AI-powered chatbot and dashboard to help students navigate a university career fair.  
=======
>>>>>>> temp-fix
# AI-Powered Career Fair Assistant (Free & Open Source)

A lightweight Streamlit app that helps students navigate a university career fair: browse companies, search roles, and ask questions powered by simple RAG (retrieval-augmented generation) using free Hugging Face models (optional) and local retrieval.

**Why this is free-friendly?**
- UI with Streamlit (free)
- Local CSV + PDF ingestion (free)
- Optional Hugging Face Inference API (free tier) — otherwise graceful fallback to retrieval-only answers
- One-click deploy on Streamlit Community Cloud (free)

---

## Features
- **Company Browser**: filter by company, role, degree level, location, sponsorship.
- **Interview Prep**: curated tips and question bank.
- **Ask the Assistant (RAG)**: ask natural-language questions; the app retrieves relevant snippets from uploaded fair PDFs and company CSV; optionally lets a small HF chat model compose the answer.

---

## Project Structure
```
ai-career-fair-assistant/
├─ app.py                     # Chat experience (RAG + optional HF model)
├─ pages/
│  ├─ 1_Company_Browser.py    # Browse/search companies & roles
│  └─ 2_Interview_Prep.py     # Tips & sample questions
├─ utils/
│  ├─ rag.py                  # PDF parsing, chunking, embeddings, retrieval
│  └─ chat.py                 # HF Inference client wrapper (optional)
├─ data/
│  ├─ companies.csv           # Sample dataset
│  └─ kb_chunks.jsonl         # Built by `ingest.py` (after you add PDFs)
├─ ingest.py                  # Turn PDFs into retrievable chunks
├─ requirements.txt
├─ .streamlit/config.toml
└─ README.md
```

---

## Quickstart (Local)

1) **Install dependencies**
```bash
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) **(Optional) Set your HF token** for better answers
- Create a free account on Hugging Face.
- Get a token at https://huggingface.co/settings/tokens
- Set an environment variable:
```bash
# macOS/Linux
export HF_TOKEN=hf_your_token_here
# Windows (PowerShell)
setx HF_TOKEN "hf_your_token_here"
```

3) **(Optional) Add Career Fair PDFs**
- Put your fair brochures / employer lists into `data/pdfs/` (create this folder).
- Build the knowledge base (chunks + embeddings):
```bash
python ingest.py
```

4) **Run the app**
```bash
streamlit run app.py
```

---

## Deploy Free on Streamlit Community Cloud
1. Push this folder to a new public GitHub repo.
2. Go to https://share.streamlit.io , connect repo, pick `app.py` as the entry point.
3. (Optional) Add a secret `HF_TOKEN` in Streamlit → App settings → Secrets.

---

## LinkedIn Blurb
> Built an **AI Career Fair Assistant** for job‑seeking students using Streamlit + free Hugging Face models. Lets students browse companies & roles, search fair PDFs, and ask questions with retrieval‑augmented answers. Fully open source and deployable on free tiers.

---

## Notes
- Works even without an HF token (answers are extractive + templated from retrieved snippets).
- PDF ingestion uses CPU-friendly embeddings to keep things simple.
- Keep `companies.csv` updated with your university data.
<<<<<<< HEAD
=======
>>>>>>> 110af02 (Initial commit - AI Career Fair Assistant)

>>>>>>> temp-fix
