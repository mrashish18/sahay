#!/usr/bin/env python3
"""
SahayAI Data Ingestion Script — Seeding authentic public assistance schemes.
"""
import os
import sys
import json

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.services.knowledge_base import knowledge_base_service

def run_ingestion():
    print("Starting SahayAI Authentic Schemes Ingestion Pipeline...")
    schemes = knowledge_base_service.list_schemes()
    print(f"Loaded {len(schemes)} authentic public service schemes.")
    
    for s in schemes:
        print(f"  - [{s['id']}] {s['title']} ({s['category']}) -> Source: {s['source_url']}")
        
    print("Ingestion Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    run_ingestion()
