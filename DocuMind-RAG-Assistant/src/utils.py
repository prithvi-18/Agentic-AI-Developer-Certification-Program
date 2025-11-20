"""
Utility functions for RAG Assistant
"""

import os
from pathlib import Path


def get_documents_from_folder(folder_path):
    """
    Load all text and markdown files from a folder
    
    Args:
        folder_path: Path to folder containing documents
    
    Returns:
        List of (filename, content) tuples
    """
    documents = []
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return documents
    
    # Supported extensions
    extensions = ['.txt', '.md', '.markdown']
    
    for file in os.listdir(folder_path):
        if any(file.endswith(ext) for ext in extensions):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append((file, content))
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    return documents


def format_sources(documents):
    """
    Format retrieved documents for display
    
    Args:
        documents: List of document objects from Chroma
    
    Returns:
        Formatted string with sources
    """
    if not documents:
        return "No sources found"
    
    sources = []
    for i, doc in enumerate(documents, 1):
        content = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
        sources.append(f"{i}. {content}")
    
    return "\n".join(sources)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def save_conversation(messages, output_file="conversation.txt"):
    """
    Save conversation history to file
    
    Args:
        messages: List of message tuples (role, content)
        output_file: Path to output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for role, content in messages:
            f.write(f"{role.upper()}:\n{content}\n\n")
    
    print(f"✓ Conversation saved to {output_file}")


def check_env_vars():
    """Check if required environment variables are set"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Please set it in .env file or environment variables."
        )
    
    return api_key
