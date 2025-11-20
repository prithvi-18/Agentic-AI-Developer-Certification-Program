"""
Configuration settings for RAG Assistant
"""

# LLM Configuration
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS = 2048

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Document Processing
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval Configuration
NUM_RETRIEVED_DOCS = 3
SIMILARITY_THRESHOLD = 0.0

# Vector Store
VECTOR_DB_PATH = "./chroma_data"
COLLECTION_NAME = "rag_documents"

# Paths
DOCUMENTS_DIR = "./data/sample_documents"

# System Prompt
SYSTEM_PROMPT = """You are a helpful AI assistant. 
Answer questions based ONLY on the provided document context.
If the answer is not found in the documents, say "This information is not covered in the provided documents."
Always be clear about what information comes from the documents.
Maintain a professional and helpful tone."""
