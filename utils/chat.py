import os
from typing import List, Dict, Optional
from huggingface_hub import InferenceClient

DEFAULT_MODEL = "HuggingFaceH4/zephyr-7b-beta"  # free endpoint, but requires token

def compose_answer(query: str, contexts: List[Dict], max_tokens: int = 256) -> str:
    """If HF token available, ask a small chat model to write an answer using the contexts."""
    token = os.getenv("HF_TOKEN")
    if not token:
        # Fallback: simple extractive answer
        joined = "\n\n".join([c.get("text","") for c in contexts])
        return (f"I couldn't access a chat model (no HF token set), but here are the most relevant details I found:\n\n"
                f"{joined}\n\n"
                f"(Tip: set an HF_TOKEN for a fluent answer.)")
    client = InferenceClient(model=DEFAULT_MODEL, token=token, timeout=60)
    system = "You are a concise assistant for a university career fair. Use the provided context snippets only."
    context_block = "\n\n".join([f"[{i+1}] {c.get('text','')}" for i, c in enumerate(contexts)])
    user = f"Question: {query}\n\nContext:\n{context_block}\n\nWrite a helpful, accurate answer grounded in the context. If unknown, say so."
    try:
        # new chat.completions API style (mirrors OpenAI)
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # graceful fallback
        joined = "\n\n".join([c.get("text","") for c in contexts])
        return (f"(Chat model unavailable: {e})\n\n"
                f"Here are relevant snippets:\n\n{joined}")
