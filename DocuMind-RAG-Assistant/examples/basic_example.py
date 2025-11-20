"""
Basic Example - Quick Start
Run this to see RAG in action with demo queries
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.rag_system import RAGAssistant
from src.utils import print_section


def main():
    """Run basic RAG example"""
    
    print_section("RAG Assistant - Basic Example")
    
    # Initialize RAG system
    print("Step 1: Initializing RAG system...")
    rag = RAGAssistant()
    
    # Load documents
    print("\nStep 2: Loading and indexing documents...")
    num_chunks = rag.load_documents()
    
    if num_chunks == 0:
        print("\n⚠ No documents found!")
        print("Please add .txt or .md files to: data/sample_documents/")
        return
    
    # Run demo queries
    print("\nStep 3: Running demo queries...")
    rag.demo_queries()
    
    print_section("Basic Example Complete!")
    print("Next steps:")
    print("1. Add your documents to: data/sample_documents/")
    print("2. Run: python examples/interactive_chat.py")

if __name__ == "__main__":
    main()
