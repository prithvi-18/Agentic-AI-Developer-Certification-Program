"""
Core RAG System Implementation
"""

import os
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


class RAGAssistant:
    """
    Retrieval Augmented Generation Assistant
    
    Combines document retrieval with LLM to answer questions
    grounded in provided documents.
    """
    
    def __init__(self, documents_folder=DOCUMENTS_DIR):
        """
        Initialize RAG Assistant
        
        Args:
            documents_folder: Path to folder containing documents
        """
        load_dotenv()
        
        # Validate API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
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
        
        print("✓ RAG Assistant initialized")
    
    def load_documents(self, force_reload=False):
        """
        Load and index documents from folder
        
        Args:
            force_reload: If True, delete existing database and reload
        """
        if force_reload and os.path.exists(VECTOR_DB_PATH):
            import shutil
            shutil.rmtree(VECTOR_DB_PATH)
            print("✓ Previous database cleared")
        
        print(f"Loading documents from: {self.documents_folder}")
        
        # Get all documents
        doc_list = get_documents_from_folder(self.documents_folder)
        
        if not doc_list:
            print("⚠ No documents found in folder")
            return 0
        
        print(f"Found {len(doc_list)} document(s)")
        
        # Process each document
        total_chunks = 0
        for filename, content in doc_list:
            print(f"  Processing: {filename}...")
            
            # Split into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
            chunks = splitter.split_text(content)
            
            # Store chunks with metadata
            for i, chunk in enumerate(chunks):
                self.vectorstore.add_texts(
                    texts=[chunk],
                    metadatas=[{
                        "source": filename,
                        "chunk_id": i
                    }]
                )
            
            total_chunks += len(chunks)
            print(f"    ✓ Split into {len(chunks)} chunks")
        
        print(f"\n✓ Total {total_chunks} chunks indexed and stored")
        return total_chunks
    
    def retrieve_relevant(self, query, k=NUM_RETRIEVED_DOCS):
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User question
            k: Number of documents to retrieve
        
        Returns:
            List of relevant documents
        """
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def query(self, user_query):
        """
        Answer a question using RAG
        
        Args:
            user_query: User's question
        
        Returns:
            Tuple of (answer, source_documents)
        """
        # Add to conversation history
        self.conversation_history.append(("user", user_query))
        
        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant(user_query)
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Build the prompt
        full_prompt = f"""Document Context:
{context}

Question: {user_query}

Answer based on the context above:"""
        
        # Generate response
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=full_prompt)
        ]
        
        response = self.llm.invoke(messages)
        answer = response.content
        
        # Add to conversation history
        self.conversation_history.append(("assistant", answer))
        
        return answer, relevant_docs
    
    def interactive_chat(self):
        """
        Start interactive chat session
        """
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
                    break
                
                if user_input.lower() == "history":
                    print_section("Conversation History")
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
                    print(f"Sources ({len(sources)} chunks):")
                    for i, doc in enumerate(sources, 1):
                        source = doc.metadata.get("source", "Unknown")
                        preview = doc.page_content[:80] + "..."
                        print(f"  {i}. [{source}] {preview}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n\nConversation ended by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again.\n")
    
    def _save_conversation(self):
        """Save current conversation to file"""
        filename = f"conversation_{len(self.conversation_history)}_turns.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for role, content in self.conversation_history:
                f.write(f"{role.upper()}:\n{content}\n\n")
        print(f"✓ Conversation saved to {filename}\n")
    
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


if __name__ == "__main__":
    # Example usage
    rag = RAGAssistant()
    rag.load_documents()
    rag.demo_queries()
