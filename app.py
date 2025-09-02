import os
import streamlit as st
from utils.rag import retrieve, load_chunks
from utils.chat import compose_answer

st.set_page_config(page_title="AI Career Fair Assistant", page_icon="🎓", layout="wide")
st.title("🎓 AI Career Fair Assistant")

st.markdown("""Ask about companies, roles, locations, sponsorship, or interview tips.
If you add PDFs to `data/pdfs/` and run `python ingest.py`, the assistant will search them too.
""")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top-K context", 1, 10, 5)
    use_chat = st.toggle("Use HF chat model (requires HF_TOKEN)", value=True)
    st.caption("If disabled or no token set, the app falls back to extractive snippets.")

query = st.text_input("Your question:", placeholder="e.g., Which companies hire MS students and sponsor visas?")
if st.button("Ask") and query.strip():
    contexts = retrieve(query, top_k=top_k)
    if not contexts:
        st.warning("No knowledge base yet. Add PDFs in data/pdfs/ and run ingest.py")
    else:
        if use_chat:
            answer = compose_answer(query, contexts)
        else:
            answer = compose_answer(query, contexts)  # will fallback if token missing
        st.subheader("Answer")
        st.write(answer)
        with st.expander("Sources"):
            for c in contexts:
                st.write(f"• {c.get('source','unknown')} — score {c.get('score',0):.3f}")
                st.write(c.get("text","")[:500] + ("..." if len(c.get("text",""))>500 else ""))

st.markdown("---")
st.caption("Tip: Keep `companies.csv` updated. Add PDFs → run `python ingest.py` → ask questions.")
