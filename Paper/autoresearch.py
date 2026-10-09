"""
Gradient Relativity Autoresearch System
========================================
Retrieves relevant document chunks from the database and feeds them to the LLM
for research assistance.

Usage:
    python3 autoresearch.py "What does the theory say about black holes?"
    python3 autoresearch.py "Fix the equations in the draft" --model 27b
    python3 autoresearch.py "Compare to DESI dark energy data" --top-k 5
    python3 autoresearch.py "Outline the Big Crunch implications" --verbose
"""
import os
import sys
import json
import math
import sqlite3
import struct
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Configuration
DB_PATH = os.path.expanduser("~/.gradient_research/docs.db")
VECTOR_DIM = 1536

# LLM servers
VLLM_BASE = "http://192.168.50.203:8000/v1"
LLAMA_BASE = "http://192.168.50.201:9931/v1"

# Models
MODEL_27B = "Qwen3.8-27B-FP8"
MODEL_35B = "Qwen3.6-35B-A3B-MTP-GGUF"


# --- Document Database ---

def simple_embed(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """Deterministic hash-based embedding."""
    seed = int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)
    state = seed
    embedding = []
    for _ in range(dim):
        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        val = (state / (1 << 64)) * 2 - 1
        embedding.append(val)
    magnitude = math.sqrt(sum(v * v for v in embedding))
    if magnitude > 0:
        embedding = [v / magnitude for v in embedding]
    return embedding


def search_documents(db_path: str, query: str, top_k: int = 5) -> List[Dict]:
    """Search documents using text-based relevance scoring."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, title, content, metadata FROM documents")
    rows = cursor.fetchall()
    conn.close()
    
    query_lower = query.lower()
    query_words = query_lower.split()
    
    scored = []
    for row in rows:
        doc_id, source, title, content, metadata = row
        score = 0.0
        title_lower = title.lower()
        content_lower = content.lower()
        
        for word in query_words:
            if word in title_lower:
                score += 3.0
            if word in content_lower:
                score += 1.0
        
        if query_lower in content_lower:
            score += 5.0
        
        scored.append({
            "id": doc_id,
            "source": source,
            "title": title,
            "content": content,
            "metadata": json.loads(metadata) if metadata else {},
            "score": score,
        })
    
    scored.sort(key=lambda x: x["score"], reverse=True)
    non_zero = [s for s in scored if s["score"] > 0]
    return non_zero[:top_k] if non_zero else scored[:top_k]


def assemble_context(query: str, results: List[Dict], max_chars: int = 8000) -> str:
    """Assemble retrieved chunks into context string for LLM."""
    parts = []
    total = 0
    
    for i, result in enumerate(results, 1):
        header = f"[Doc {i}: {result['title']}] ({result['source']})"
        if total + len(header) + 1 + len(result["content"]) > max_chars:
            break
        
        parts.append(f"\n{header}\n{result['content']}")
        total += len(header) + 1 + len(result["content"])
    
    return "\n".join(parts)


# --- LLM API ---

def call_llm(messages: List[Dict], model: str = MODEL_27B, base_url: str = VLLM_BASE, 
             max_tokens: int = 4096, temperature: float = 0.7) -> str:
    """Call the vLLM API."""
    import urllib.request
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('VLLM_API_KEY', '')}",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM error: {e}"


# --- Autoresearch ---

def autoresearch(query: str, model: str = MODEL_27B, top_k: int = 5, 
                 verbose: bool = False) -> str:
    """
    Full autoresearch pipeline:
    1. Retrieve relevant document chunks
    2. Assemble context
    3. Send to LLM with research prompt
    4. Return answer
    """
    # Step 1: Retrieve relevant chunks
    if verbose:
        print(f"Searching for: '{query}'")
    
    results = search_documents(DB_PATH, query, top_k=top_k)
    
    if not results:
        return "No relevant documents found in the database."
    
    if verbose:
        print(f"Found {len(results)} relevant documents:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['title']} (score: {r['score']:.1f})")
        print()
    
    # Step 2: Assemble context
    context = assemble_context(query, results)
    
    # Step 3: Build research prompt
    system_prompt = """You are a quantum physics research assistant specializing in Gradient Relativity.
You have access to the author's research notes, draft papers, equation audits, and theoretical frameworks.
Your job is to:
1. Answer questions based on the provided context from the Gradient Relativity research documents
2. Identify gaps, errors, or inconsistencies in the theory
3. Suggest improvements, derivations, or experimental tests
4. Connect the theory to established physics (GR, QFT, cosmology)
5. Be honest about what the theory claims vs what is established physics

When answering:
- Cite which documents your answer is based on
- Distinguish between the author's original claims and standard physics
- Point out dimensional inconsistencies or mathematical errors
- Suggest specific improvements or experiments
- Be thorough but concise"""

    user_prompt = f"""Research question: {query}

=== RELEVANT DOCUMENT CONTEXT ===

{context}

=== END CONTEXT ===

Please answer the research question using the context above. Be specific, cite sources, and distinguish between the author's claims and established physics. If the context doesn't fully answer the question, say so and explain what additional research would be needed."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    if verbose:
        print(f"Sending to LLM ({model})...")
    
    # Step 4: Get answer
    answer = call_llm(messages, model=model)
    
    return answer


def main():
    parser = argparse.ArgumentParser(description="Gradient Relativity Autoresearch")
    parser.add_argument("query", help="Research question")
    parser.add_argument("--model", choices=["27b", "35b"], default="27b", help="Model to use")
    parser.add_argument("--top-k", type=int, default=5, help="Number of documents to retrieve")
    parser.add_argument("--verbose", action="store_true", help="Show retrieval details")
    parser.add_argument("--context-only", action="store_true", help="Only show retrieved context, don't call LLM")
    parser.add_argument("--db-path", type=str, default=DB_PATH)
    args = parser.parse_args()
    
    model = MODEL_27B if args.model == "27b" else MODEL_35B
    base_url = VLLM_BASE if args.model == "27b" else LLAMA_BASE
    
    # Check database
    if not os.path.exists(args.db_path):
        print(f"Error: Database not found at {args.db_path}")
        print("Run: python3 ingest_docs.py")
        sys.exit(1)
    
    # Search
    results = search_documents(args.db_path, args.query, top_k=args.top_k)
    
    if args.context_only:
        print(f"Retrieved {len(results)} documents for: '{args.query}'\n")
        context = assemble_context(args.query, results)
        print(context)
        return
    
    # Autoresearch
    answer = autoresearch(args.query, model=model, top_k=args.top_k, verbose=args.verbose)
    print(answer)


if __name__ == "__main__":
    main()
