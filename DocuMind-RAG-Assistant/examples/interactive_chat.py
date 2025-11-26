"""
Interactive Chat Example
Full interactive conversation with RAG assistant
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.rag_system import RAGAssistant
from src.utils import print_section


def main():
    """Run interactive chat"""
    
    print_section("DocuMind-RAG-Assistant - Interactive Chat")
    
    # Initialize
    print("Initializing RAG system...")
    rag = RAGAssistant()
    
    # Load documents
    print("Loading documents...")
    num_chunks = rag.load_documents()
    
    if num_chunks == 0:
        print("\n⚠ No documents found!")
        print("Please add .txt or .md files to: data/sample_documents/")
        print("\nExample:")
        print("1. Create data/sample_documents/")
        print("2. Add your .txt or .md files")
        print("3. Run this script again")
        return
    
    print(f"\n✓ Loaded {num_chunks} chunks\n")
    
    # Start chat
    rag.interactive_chat()


if __name__ == "__main__":
    main()
