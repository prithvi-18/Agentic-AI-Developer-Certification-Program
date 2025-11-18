"""
ENHANCED RAG_SYSTEM.py - With Error Handling & Quality Controls
Production-ready version with functional rigor
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .config import (
    LLM_MODEL, LLM_TEMPERATURE, EMBEDDING_MODEL,
    CHUNK_SIZE, CHUNK_OVERLAP, NUM_RETRIEVED_DOCS,
    VECTOR_DB_PATH, COLLECTION_NAME, SYSTEM_PROMPT,
    DOCUMENTS_DIR
)
from .utils import get_documents_from_folder, format_sources, print_section

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAssistant:
    """
    Production-ready RAG Assistant with:
    ✅ Error handling
    ✅ Input validation
    ✅ Memory management
    ✅ Source grounding
    ✅ Quality controls
    """
    
    def __init__(self, documents_folder=DOCUMENTS_DIR):
        """Initialize RAG Assistant with error handling"""
        try:
            load_dotenv()
            
            # Validate API key
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("❌ GROQ_API_KEY not found in .env file")
            
            # Initialize LLM
            self.llm = ChatGroq(
                model=LLM_MODEL,
                temperature=LLM_TEMPERATURE,
                api_key=api_key
            )
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL
            )
            
            # Initialize vector store
            self.vectorstore = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=VECTOR_DB_PATH
            )
            
            self.documents_folder = documents_folder
            self.conversation_history = []
            
            logger.info("✓ RAG Assistant initialized successfully")
            print("✓ RAG Assistant initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Assistant: {e}")
            raise
    
    def load_documents(self, force_reload=False):
        """Load and index documents with error handling"""
        try:
            if force_reload and os.path.exists(VECTOR_DB_PATH):
                import shutil
                shutil.rmtree(VECTOR_DB_PATH)
                logger.info("Previous database cleared")
                print("✓ Previous database cleared")
            
            # Validate folder exists
            if not os.path.exists(self.documents_folder):
                raise FileNotFoundError(f"Documents folder not found: {self.documents_folder}")
            
            logger.info(f"Loading documents from: {self.documents_folder}")
            print(f"Loading documents from: {self.documents_folder}")
            
            # Get all documents
            doc_list = get_documents_from_folder(self.documents_folder)
            
            if not doc_list:
                logger.warning("No documents found in folder")
                print("⚠ No documents found in folder")
                return 0
            
            logger.info(f"Found {len(doc_list)} document(s)")
            print(f"Found {len(doc_list)} document(s)")
            
            # Process each document
            total_chunks = 0
            for filename, content in doc_list:
                try:
                    if not content or not content.strip():
                        logger.warning(f"Empty document: {filename}")
                        continue
                    
                    logger.info(f"Processing: {filename}")
                    print(f"  Processing: {filename}...")
                    
                    # Split into chunks
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=CHUNK_OVERLAP
                    )
                    chunks = splitter.split_text(content)
                    
                    if not chunks:
                        logger.warning(f"No chunks created from {filename}")
                        continue
                    
                    # Store chunks with metadata
                    for i, chunk in enumerate(chunks):
                        if chunk.strip():  # Only store non-empty chunks
                            self.vectorstore.add_texts(
                                texts=[chunk],
                                metadatas=[{
                                    "source": filename,
                                    "chunk_id": i
                                }]
                            )
                    
                    total_chunks += len(chunks)
                    logger.info(f"✓ Split {filename} into {len(chunks)} chunks")
                    print(f"    ✓ Split into {len(chunks)} chunks")
                    
                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
                    print(f"    ❌ Error: {e}")
                    continue
            
            logger.info(f"✓ Total {total_chunks} chunks indexed")
            print(f"\n✓ Total {total_chunks} chunks indexed and stored")
            return total_chunks
            
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            print(f"❌ Error loading documents: {e}")
            raise
    
    def retrieve_relevant(self, query, k=NUM_RETRIEVED_DOCS):
        """Retrieve relevant documents with validation"""
        try:
            # Validate query
            if not query or not query.strip():
                logger.warning("Empty query received")
                return []
            
            if len(query) > 1000:
                query = query[:1000]  # Truncate very long queries
                logger.warning("Query truncated to 1000 characters")
            
            logger.info(f"Retrieving {k} documents for query: {query[:50]}...")
            results = self.vectorstore.similarity_search(query, k=k)
            
            logger.info(f"Found {len(results)} relevant documents")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def query(self, user_query):
        """
        Answer a question using RAG with full error handling
        
        Returns:
            Tuple of (answer, source_documents)
        """
        try:
            # Input validation
            if not user_query or not user_query.strip():
                return "❌ Error: Query cannot be empty. Please ask a question.", []
            
            if len(user_query) > 5000:
                return "❌ Error: Query too long (max 5000 characters)", []
            
            # Add to conversation history
            self.conversation_history.append(("user", user_query))
            
            logger.info(f"Processing query: {user_query[:50]}...")
            
            # Retrieve relevant documents
            relevant_docs = self.retrieve_relevant(user_query)
            
            if not relevant_docs:
                logger.warning("No relevant documents found")
                return "⚠ No relevant documents found. Try rephrasing your question.", []
            
            # Build context from retrieved documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Build the prompt
            full_prompt = f"""Document Context:
{context}

Question: {user_query}

Answer based ONLY on the context above:"""
            
            # Generate response
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=full_prompt)
            ]
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            # Add to conversation history
            self.conversation_history.append(("assistant", answer))
            
            logger.info(f"✓ Generated answer with {len(relevant_docs)} sources")
            return answer, relevant_docs
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"❌ Error: {str(e)}", []
    
    def interactive_chat(self):
        """Start interactive chat session with error handling"""
        print_section("Interactive Chat Mode")
        print("Type 'exit' or 'quit' to end conversation")
        print("Type 'history' to see conversation history")
        print("Type 'save' to save conversation\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit"]:
                    print("\nGoodbye!")
                    logger.info("Chat session ended")
                    break
                
                if user_input.lower() == "history":
                    print_section("Conversation History")
                    if not self.conversation_history:
                        print("No conversation history yet.")
                    else:
                        for role, content in self.conversation_history:
                            print(f"{role.upper()}: {content}\n")
                    continue
                
                if user_input.lower() == "save":
                    self._save_conversation()
                    continue
                
                # Get answer
                print("\nThinking...")
                answer, sources = self.query(user_input)
                
                print(f"\nAssistant: {answer}\n")
                
                if sources:
                    print(f"Sources ({len(sources)} chunks used):")
                    for i, doc in enumerate(sources, 1):
                        source = doc.metadata.get("source", "Unknown")
                        preview = doc.page_content[:60] + "..."
                        print(f"  {i}. [{source}] {preview}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nChat ended by user")
                logger.info("Chat interrupted by user")
                break
            except Exception as e:
                logger.error(f"Chat error: {e}")
                print(f"Error: {e}\n")
    
    def _save_conversation(self):
        """Save conversation to file"""
        try:
            filename = f"conversation_{len(self.conversation_history)}_turns.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for role, content in self.conversation_history:
                    f.write(f"{role.upper()}:\n{content}\n\n")
            
            logger.info(f"Conversation saved to {filename}")
            print(f"✓ Conversation saved to {filename}\n")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            print(f"❌ Error saving conversation: {e}\n")
    
    def demo_queries(self):
        """Run demo with sample queries"""
        sample_queries = [
            "What is the main topic of the documents?",
            "Provide a summary of the key points",
            "What are the most important concepts?",
        ]
        
        print_section("Running Demo Queries")
        
        for query in sample_queries:
            print(f"Q: {query}")
            answer, sources = self.query(query)
            print(f"A: {answer}\n")
            
            if sources:
                print(f"Sources: {len(sources)} relevant chunks found")
                for i, doc in enumerate(sources, 1):
                    source = doc.metadata.get("source", "Unknown")
                    print(f"  {i}. {source}")
            
            print("-" * 70 + "\n")
        
        logger.info("Demo queries completed")


if __name__ == "__main__":
    # Example usage
    try:
        rag = RAGAssistant()
        rag.load_documents()
        rag.demo_queries()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
