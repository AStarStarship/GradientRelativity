"""
Document Ingestion Pipeline for Gradient Relativity Research
=============================================================
Uses SQLite with numpy vectors (no pgvector needed).
Migrates to pgvector when superuser access is available.

Usage:
    python3 ingest_docs.py                    # Ingest all Gradient Relativity docs
    python3 ingest_docs.py --dry-run          # Preview without writing
    python3 ingest_docs.py --search "gravity" # Search after ingestion
"""
import os
import sys
import json
import re
import hashlib
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional
import sqlite3
import struct

# Configuration
DB_PATH = os.path.expanduser("~/.gradient_research/docs.db")
GRADIENT_RESEARCH_DIR = Path("/home/astarcale/AStarStarship/GradientRelativity")

# Chunking settings
CHUNK_SIZE = 120  # words
CHUNK_OVERLAP = 20
MAX_CHUNKS_PER_DOC = 50
VECTOR_DIM = 1536  # matches text-embedding-3-large / all-MiniLM-L6-v2


@dataclass
class DocumentChunk:
    source: str
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_index: int = 0
    total_chunks: int = 0


def simple_embed(text: str, dim: int = VECTOR_DIM) -> List[float]:
    """
    Simple deterministic embedding using hash-based projection.
    Not a real ML embedding — good enough for demo/testing.
    Replace with actual embedding model when GPU is available.
    
    Uses a fixed seed hash so the same text always gets the same embedding.
    """
    import hashlib
    
    # Use SHA-256 of the text as seed, then generate deterministic pseudo-random values
    seed = int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)
    
    # Generate deterministic values using a simple LCG
    state = seed
    embedding = []
    for _ in range(dim):
        # Linear congruential generator
        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        # Map to [-1, 1] range
        val = (state / (1 << 64)) * 2 - 1
        embedding.append(val)
    
    # Normalize
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


def read_markdown_file(filepath: Path) -> str:
    """Read a markdown file and return its content."""
    return filepath.read_text(encoding="utf-8")


def extract_frontmatter(content: str) -> tuple:
    """Extract YAML frontmatter if present."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            meta = {}
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip()
            return meta, parts[2].strip()
    return {}, content


def extract_title(content: str) -> str:
    """Extract the first H1 heading as the title."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into chunks with overlap (word-based)."""
    words = text.split()
    if not words:
        return []
    
    chunks = []
    i = 0
    while i < len(words):
        end = min(i + chunk_size, len(words))
        chunk = " ".join(words[i:end])
        chunks.append(chunk)
        i = end - overlap
        if i < end:
            i = end  # avoid infinite loop at end
        if i >= len(words):
            break
    return chunks


def generate_chunk_id(source: str, title: str, chunk_index: int) -> str:
    """Generate a unique chunk ID."""
    raw = f"{source}:{title}:{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def ingest_gradient_research_docs(dry_run: bool = False) -> List[DocumentChunk]:
    """Ingest all documents from the Gradient Relativity project."""
    chunks = []
    
    if not GRADIENT_RESEARCH_DIR.exists():
        print(f"Warning: {GRADIENT_RESEARCH_DIR} not found")
        return chunks
    
    for md_file in sorted(GRADIENT_RESEARCH_DIR.rglob("*.md")):
        try:
            content = read_markdown_file(md_file)
            meta, clean_content = extract_frontmatter(content)
            title = extract_title(clean_content)
            source = str(md_file.relative_to(GRADIENT_RESEARCH_DIR.parent))
            
            if len(clean_content) < 50:
                continue
            
            text_chunks = chunk_text(clean_content)
            
            for idx, chunk in enumerate(text_chunks):
                if idx >= MAX_CHUNKS_PER_DOC:
                    break
                    
                doc = DocumentChunk(
                    source=source,
                    title=title,
                    content=chunk,
                    metadata={
                        "file": str(md_file),
                        "word_count": len(chunk.split()),
                        "section": meta.get("section", ""),
                        "type": meta.get("type", "research"),
                    },
                    chunk_index=idx,
                    total_chunks=len(text_chunks),
                )
                chunks.append(doc)
                
            print(f"  Ingested {len(text_chunks)} chunks from {md_file.name}")
            
        except Exception as e:
            print(f"  Error processing {md_file}: {e}")
    
    return chunks


def init_db(db_path: str = DB_PATH):
    """Initialize SQLite database with schema."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding BLOB,
            metadata TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_source 
        ON documents (source)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_title 
        ON documents (title)
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            results JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    return conn


def insert_chunks(conn, chunks: List[DocumentChunk], dry_run: bool = False) -> int:
    """Insert chunks into the database with embeddings."""
    cursor = conn.cursor()
    inserted = 0
    
    for chunk in chunks:
        chunk_id = generate_chunk_id(chunk.source, chunk.title, chunk.chunk_index)
        
        # Check if already exists
        cursor.execute("SELECT id FROM documents WHERE id = ?", (chunk_id,))
        if cursor.fetchone():
            continue
        
        if not dry_run:
            # Generate embedding
            embedding = simple_embed(chunk.content)
            embedding_blob = struct.pack(f"{VECTOR_DIM}f", *embedding)
            
            cursor.execute("""
                INSERT INTO documents (id, source, title, content, embedding, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                chunk_id,
                chunk.source,
                chunk.title,
                chunk.content,
                embedding_blob,
                json.dumps(chunk.metadata),
            ))
            inserted += 1
        else:
            print(f"  Would insert: {chunk.title} (chunk {chunk.chunk_index}, {len(chunk.content)} chars)")
            inserted += 1
    
    conn.commit()
    return inserted


def search_documents(conn, query: str, top_k: int = 5) -> List[Dict]:
    """Search documents using vector similarity."""
    cursor = conn.cursor()
    
    # Generate query embedding
    query_embedding = simple_embed(query)
    
    # Get all documents
    cursor.execute("SELECT id, source, title, content, embedding, metadata FROM documents")
    rows = cursor.fetchall()
    
    # Compute cosine similarity for each document
    scored = []
    for row in rows:
        doc_id, source, title, content, embedding_blob, metadata = row
        if embedding_blob is None:
            continue
        
        # Decode embedding
        embedding = list(struct.unpack(f"{VECTOR_DIM}f", embedding_blob))
        sim = cosine_similarity(query_embedding, embedding)
        
        scored.append({
            "id": doc_id,
            "source": source,
            "title": title,
            "content": content,
            "metadata": json.loads(metadata) if metadata else {},
            "similarity": sim,
        })
    
    # Sort by similarity descending
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    
    return scored[:top_k]


def search_text(conn, query: str, top_k: int = 5) -> List[Dict]:
    """Simple text-based search fallback."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source, title, content, metadata
        FROM documents
        WHERE content LIKE ? OR title LIKE ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (f"%{query}%", f"%{query}%", top_k))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            "id": row[0],
            "source": row[1],
            "title": row[2],
            "content": row[3],
            "metadata": json.loads(row[4]) if row[4] else {},
            "similarity": 0.0,
        })
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Document ingestion pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--search", type=str, help="Search for a term after ingestion")
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    parser.add_argument("--db-path", type=str, default=DB_PATH)
    args = parser.parse_args()
    
    db_path = args.db_path
    
    print(f"Database: {db_path}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("-" * 60)
    
    conn = init_db(db_path)
    
    if args.stats:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM documents")
        count = cursor.fetchone()[0]
        print(f"\nDatabase contains {count} chunks")
        cursor.execute("SELECT DISTINCT source FROM documents")
        sources = [r[0] for r in cursor.fetchall()]
        print(f"Sources: {sources}")
        conn.close()
        return
    
    # Ingest documents
    print("\nIngesting Gradient Relativity documents...")
    chunks = ingest_gradient_research_docs(dry_run=args.dry_run)
    print(f"\nTotal chunks: {len(chunks)}")
    
    if chunks:
        print(f"\nInserting chunks into database...")
        inserted = insert_chunks(conn, chunks, dry_run=args.dry_run)
        print(f"Inserted: {inserted} chunks")
    
    # Search if requested
    if args.search:
        print(f"\nSearching for: '{args.search}'")
        results = search_documents(conn, args.search)
        if results:
            print(f"Found {len(results)} results (vector similarity):")
            for i, result in enumerate(results, 1):
                print(f"\n  {i}. {result['title']} (similarity: {result['similarity']:.4f})")
                print(f"     Source: {result['source']}")
                print(f"     Content: {result['content'][:300]}...")
        else:
            # Fallback to text search
            print("No vector matches. Trying text search...")
            results = search_text(conn, args.search)
            print(f"Found {len(results)} results (text match):")
            for i, result in enumerate(results, 1):
                print(f"\n  {i}. {result['title']}")
                print(f"     Source: {result['source']}")
                print(f"     Content: {result['content'][:300]}...")
    
    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
