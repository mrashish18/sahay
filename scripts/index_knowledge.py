#!/usr/bin/env python3
"""
Sahay RAG Indexing CLI Script.
Repeatable, idempotent knowledge chunking and vector embedding indexing pipeline.
"""
import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.services.rag_service import rag_service

def run_indexing():
    print("=" * 60)
    print("           Sahay Knowledge RAG Indexer")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resolved_path = os.path.abspath(os.path.join(base_dir, "../data/raw/authentic_schemes.json"))
    
    if not os.path.exists(resolved_path):
        print(f"Error: Target dataset file not found at {resolved_path}")
        sys.exit(1)

    print(f"Reading dataset: {resolved_path}")
    stats = rag_service.index_dataset(resolved_path)

    print("\n--- Indexing Execution Summary ---")
    print(f"Documents Discovered:      {stats['discovered']}")
    print(f"Valid Documents Indexed:   {stats['valid']}")
    print(f"Rejected Documents:        {stats['rejected']}")
    print(f"Chunks Generated:          {stats['chunks_generated']}")
    print(f"Embeddings Created:        {stats['embeddings_created']}")
    print(f"Total Vector Index Chunks: {stats['total_indexed_chunks']}")
    print("=" * 60)
    print("RAG Indexing Pipeline Completed Successfully.\n")

if __name__ == "__main__":
    run_indexing()
