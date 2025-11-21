#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) for Knowledge Base
Embeds all markdown files and enables semantic search
"""

import os
from pathlib import Path
import json
import hashlib
from datetime import datetime

# Knowledge Base path
KB_PATH = Path.home() / "Documents/ObsidianVault/Knowledge-Base"
RAG_INDEX_PATH = Path.home() / ".claude/rag-index"
RAG_INDEX_PATH.mkdir(parents=True, exist_ok=True)

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def build_rag_index():
    """Build RAG index from all markdown files"""

    print("Building RAG index...")

    index = {
        "documents": [],
        "metadata": {
            "created": datetime.now().isoformat(),
            "total_files": 0,
            "total_chunks": 0
        }
    }

    md_files = list(KB_PATH.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    for file_path in md_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Get metadata
            rel_path = file_path.relative_to(KB_PATH)
            topic = str(rel_path.parts[0]) if len(rel_path.parts) > 1 else "Root"
            file_hash = hashlib.md5(content.encode()).hexdigest()

            # Chunk the content
            chunks = chunk_text(content)

            for i, chunk in enumerate(chunks):
                doc = {
                    "id": f"{file_hash}_{i}",
                    "file_path": str(rel_path),
                    "topic": topic,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "content": chunk,
                    "file_hash": file_hash,
                    "word_count": len(chunk.split())
                }
                index["documents"].append(doc)

            index["metadata"]["total_files"] += 1
            index["metadata"]["total_chunks"] += len(chunks)

            if index["metadata"]["total_files"] % 10 == 0:
                print(f"Processed {index['metadata']['total_files']} files...")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Save index
    index_file = RAG_INDEX_PATH / "kb_index.json"
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\n✓ RAG Index Complete!")
    print(f"  Files indexed: {index['metadata']['total_files']}")
    print(f"  Total chunks: {index['metadata']['total_chunks']}")
    print(f"  Index saved to: {index_file}")

    return index

def search_knowledge_base(query, top_k=5):
    """Simple keyword-based search (can be enhanced with embeddings later)"""

    index_file = RAG_INDEX_PATH / "kb_index.json"

    if not index_file.exists():
        print("Index not found. Building...")
        build_rag_index()

    with open(index_file, 'r') as f:
        index = json.load(f)

    # Simple keyword matching (TODO: Use embeddings for better results)
    query_lower = query.lower()
    results = []

    for doc in index["documents"]:
        if query_lower in doc["content"].lower():
            score = doc["content"].lower().count(query_lower)
            results.append({
                "file_path": doc["file_path"],
                "topic": doc["topic"],
                "chunk": doc["content"][:300] + "...",
                "score": score
            })

    # Sort by score and return top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Search mode
        query = " ".join(sys.argv[1:])
        print(f"Searching for: {query}\n")
        results = search_knowledge_base(query)

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['file_path']} ({result['topic']})")
            print(f"   {result['chunk']}")
            print(f"   Score: {result['score']}")
    else:
        # Build index mode
        build_rag_index()
