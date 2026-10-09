"""
Context Assembly System for Gradient Relativity Autoresearch
==============================================================
Retrieves relevant document chunks and assembles context for LLM prompts.

Usage:
    python3 context_assembly.py --query "gravity"              # Search
    python3 context_assembly.py --query "gravity" --top-k 3    # Top 3 results
    python3 context_assembly.py --assemble --query "black holes"  # Full context assembly
    python3 context_assembly.py --stats                         # Database stats
"""
import os
import sys
import json
import math
import sqlite3
import struct
from pathlib import Path
from typing import List, Dict, Any

DB_PATH = os.path.expanduser("~/.gradient_research/docs.db")
VECTOR_DIM = 1536


def simple_embed(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """Deterministic hash-based embedding (same as ingest_docs.py)."""
    import hashlib
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


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def search_vectors(db_path: str, query: str, top_k: int = 5) -> List[Dict]:
    """Search documents using vector similarity."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query_embedding = simple_embed(query)
    cursor.execute("SELECT id, source, title, content, metadata FROM documents")
    rows = cursor.fetchall()
    
    scored = []
    for row in rows:
        doc_id, source, title, content, metadata = row
        # For now, skip vector search (hash embeddings are deterministic but not semantic)
        # Use text-based search instead
        scored.append({
            "id": doc_id,
            "source": source,
            "title": title,
            "content": content,
            "metadata": json.loads(metadata) if metadata else {},
            "similarity": 0.0,
        })
    
    conn.close()
    
    # Text-based scoring: title match > content match > metadata match
    query_lower = query.lower()
    query_words = query_lower.split()
    
    for item in scored:
        score = 0.0
        title_lower = item["title"].lower()
        content_lower = item["content"].lower()
        
        # Title matches weighted higher
        for word in query_words:
            if word in title_lower:
                score += 3.0
            if word in content_lower:
                score += 1.0
        
        # Exact phrase match bonus
        if query_lower in content_lower:
            score += 5.0
        
        item["similarity"] = score
    
    # Sort by score descending
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Return top_k with non-zero scores, or top_k overall if all zero
    non_zero = [s for s in scored if s["similarity"] > 0]
    if non_zero:
        return non_zero[:top_k]
    return scored[:top_k]


def assemble_context(query: str, top_k: int = 5, max_context_chars: int = 8000) -> str:
    """
    Assemble context from relevant document chunks.
    Returns a formatted context string suitable for LLM prompts.
    """
    results = search_vectors(DB_PATH, query, top_k=top_k)
    
    if not results:
        return "No relevant documents found."
    
    context_parts = []
    total_chars = 0
    
    for i, result in enumerate(results, 1):
        source = result["source"]
        title = result["title"]
        content = result["content"]
        score = result["similarity"]
        
        # Format: [Document N: Title] (source)
        header = f"[Document {i}: {title}] ({source})"
        header_len = len(header) + 1
        
        if total_chars + header_len + len(content) > max_context_chars:
            break
        
        context_parts.append(f"\n{header}\n")
        context_parts.append(content)
        total_chars += header_len + len(content)
    
    context = "\n".join(context_parts)
    
    # Add retrieval metadata
    context += f"\n\n---\nRetrieved {len(results)} documents for query: '{query}'"
    context += f"\nTop similarity score: {max(r['similarity'] for r in results):.2f}"
    
    return context


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Context assembly for autoresearch")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--assemble", action="store_true", help="Full context assembly for LLM")
    parser.add_argument("--stats", action="store_true", help="Database statistics")
    parser.add_argument("--db-path", type=str, default=DB_PATH)
    args = parser.parse_args()
    
    if not os.path.exists(args.db_path):
        print(f"Error: Database not found at {args.db_path}")
        print("Run ingest_docs.py first.")
        sys.exit(1)
    
    if args.stats:
        conn = sqlite3.connect(args.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM documents")
        count = cursor.fetchone()[0]
        print(f"Documents: {count} chunks")
        cursor.execute("SELECT DISTINCT source FROM documents ORDER BY source")
        sources = [r[0] for r in cursor.fetchall()]
        print(f"Sources ({len(sources)}):")
        for source in sources:
            cursor.execute("SELECT count(*) FROM documents WHERE source LIKE ?", (f"%{source}%",))
            n = cursor.fetchone()[0]
            print(f"  - {source}: {n} chunks")
        conn.close()
        return
    
    if not args.query:
        print("Error: --query is required")
        print("Usage: python3 context_assembly.py --query 'gravity' [--top-k 5]")
        sys.exit(1)
    
    if args.assemble:
        # Full context assembly for LLM
        context = assemble_context(args.query, top_k=args.top_k)
        print(context)
    else:
        # Just show search results
        results = search_vectors(args.db_path, args.query, top_k=args.top_k)
        print(f"Query: '{args.query}' ({args.top_k} results)\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Source: {result['source']}")
            print(f"   Score: {result['similarity']:.2f}")
            print(f"   Content: {result['content'][:200]}...")
            print()


if __name__ == "__main__":
    main()
