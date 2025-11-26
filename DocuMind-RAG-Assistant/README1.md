# DocuMind-RAG-Assistant - Module 1 Project
## Ready Tensor Agentic AI Developer Certification

## Project Overview

A **production-ready Retrieval Augmented Generation (RAG) system** demonstrating core Agentic AI concepts with **functional rigor and quality controls**.

This project showcases:
- ✅ Document processing and chunking
- ✅ Vector embeddings and semantic search
- ✅ LLM integration with proper error handling
- ✅ Memory management and conversation history
- ✅ Source attribution and grounding
- ✅ Production-level quality controls

---

## Key Features

### Functional Rigor

#### 1. Query Processing
- Semantic search using HuggingFace embeddings
- Vector similarity ranking for relevant documents
- Query validation and truncation for safety
- Handling of edge cases (empty queries, very long inputs)

#### 2. Memory Management
- Maintains conversation history across turns
- Stores user queries and assistant responses
- Enables context-aware responses in follow-up questions
- Efficient cleanup with configurable history limits

#### 3. Context-Aware Suggestions
- Uses previous conversation context when available
- Tailors responses based on interaction history
- Provides relevant follow-up information

#### 4. Grounding in Real Data
- All answers backed by source documents
- Clear citation of relevant chunks
- Prevents hallucination through document grounding
- Shows exact source and location of information

### Quality Controls

#### Error Handling
- Comprehensive try-catch blocks
- Graceful error messages for users
- Logging system for debugging
- Handles API failures and edge cases

#### Input Validation
- Empty query detection
- Maximum query length enforcement (5000 chars)
- Special character handling
- Prevents injection attacks

#### Data Quality
- Skips empty documents
- Filters non-empty chunks only
- Validates document format
- Handles encoding issues

#### Logging & Monitoring
- Detailed logging at every step
- Tracks system performance
- Records error conditions
- Helps with debugging and optimization

---

## Project Structure

```
rag-assistant-module1/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration settings
│   ├── rag_system.py            # Main RAG implementation
│   ├── rag_system.py            # Production version with error handling
│   └── utils.py                 # Utility functions
├── data/
│   └── sample_documents/
│       ├── document1_vae.md     # Variational Autoencoders guide
│       └── document2_agentic_ai.md  # Agentic AI principles
├── examples/
│   ├── basic_example.py         # Quick demo
│   └── interactive_chat.py      # Interactive mode
├── screenshots/
├── logs/                        # System logs
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── .env.example                 # Environment template
└── .gitignore                   # Hide secrets
```

---

## Installation

### 1. Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 4. Verify Setup
```bash
python -c "from src.rag_system import RAGAssistant; print('✓ Setup successful!')"
```

---

## Usage

### Quick Demo
```bash
python examples/basic_example.py
```

### Interactive Chat
```bash
python examples/interactive_chat.py
```

Then ask questions about the documents:
- Type your questions freely
- Type `history` to see conversation history
- Type `save` to save the conversation
- Type `exit` to quit

### Programmatic Usage
```python
from src.rag_system import RAGAssistant

# Initialize
rag = RAGAssistant()
rag.load_documents()

# Ask a question
answer, sources = rag.query("What is the main topic?")
print(f"Answer: {answer}")
print(f"Sources: {len(sources)} documents used")
```

---

## Technologies Used

- **LangChain 1.0+**: Framework for building LLM applications
- **Groq API**: Fast LLM inference (llama-3.3-70b-versatile)
- **HuggingFace Embeddings**: Semantic text representations
- **Chroma**: Vector database for storing embeddings
- **Python 3.8+**: Core language

---

## Week 3 Concepts Demonstrated

### 1. Document Loading & Chunking
- Loading multiple document formats
- Intelligent text chunking with overlap
- Metadata preservation

### 2. Vector Embeddings
- Converting text to semantic vectors
- Using pre-trained embedding models
- Similarity computation

### 3. Semantic Search
- Finding relevant documents by meaning
- Ranking results by relevance
- Handling ambiguous queries

### 4. LLM Integration
- Calling external LLMs via API
- Prompt engineering
- Response generation

### 5. Memory Management
- Storing conversation history
- Context awareness across turns
- Efficient state management

### 6. Safety & Grounding
- Preventing hallucination
- Source attribution
- Input validation
- Error handling

---

## Example Output

```
Q: What is the main topic of the documents?

A: The main topic of the documents is Agentic Systems, specifically 
their core components, key principles, and challenges. The documents 
provide an overview of how agentic systems work, their design 
principles, and the difficulties that come with developing such systems.

Sources: 3 relevant chunks found
  1. document2_agentic_ai.md
  2. document2_agentic_ai.md
  3. document2_agentic_ai.md
```

---

## Production Features

### Logging System
- All operations logged to `logs/system.log`
- Error tracking and debugging
- Performance monitoring

### Error Handling
- API failures handled gracefully
- Network timeouts managed
- Invalid input rejected

### Input Validation
- Empty queries detected
- Query length limits enforced
- Special characters handled

### Quality Assurance
- Empty documents skipped
- Chunk validation
- Metadata verification

---

## Troubleshooting

### "GROQ_API_KEY not found"
```bash
# Check .env file exists
cat .env

# Should contain:
GROQ_API_KEY=your-actual-key-here
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or upgrade
pip install --upgrade langchain-core
```

### "No documents found"
```bash
# Check document folder
ls data/sample_documents/

# Should see .txt or .md files
```

### "Chroma database error"
```bash
# Reset vector database
rm -rf chroma_data/

# Reload documents
python examples/basic_example.py
```

## Screenshots

### System Working - Interactive Chat

![Interactive Chat](screenshots/screenshot1_interactive_chat.jpg)
*Shows RAG system answering questions with source attribution*

### Document Loading & Indexing

![Document Loading](screenshots/screenshot2_document_loading.jpg)
*Shows 2 documents loaded and split into 22 chunks*

### Multiple Questions in Conversation

![Multiple Questions](screenshots/screenshot3_multiple_questions.jpg)
*Demonstrates conversation history and context awareness*

### Grounding & Safety

![Grounding](screenshots/screenshot4_error_handling.jpg)
*System refuses to answer outside document scope - no hallucination!*

---

## Performance

- **Query Processing**: < 2 seconds
- **Document Loading**: < 30 seconds for 2 documents
- **Memory Usage**: ~500MB (varies with document size)
- **Concurrent Queries**: Supports sequential processing

---

## Testing

### Test Edge Cases
```bash
# Empty query
rag.query("")  # Handled gracefully

# Very long query
rag.query("x" * 10000)  # Truncated to 5000 chars

# Special characters
rag.query("What is <script>?")  # Safe handling
```

### Test Error Cases
- Missing documents
- API connection failures
- Invalid environment variables

---

## Future Enhancements

- [ ] PDF document support
- [ ] Multi-language support
- [ ] Persistent database
- [ ] Web UI interface
- [ ] Batch processing
- [ ] Fine-tuned embeddings
- [ ] Response caching

---

## Code Quality

### Implemented Best Practices
- ✅ Modular design (config, RAG system, utils)
- ✅ Error handling at every step
- ✅ Input validation
- ✅ Logging system
- ✅ Type hints
- ✅ Comprehensive docstrings
- ✅ Configuration management
- ✅ Environment variable handling

---

## Learning Outcomes

After building this project, you understand:
- How RAG systems work in production
- Vector databases and semantic search
- LLM integration and prompt engineering
- Error handling in AI systems
- Memory management patterns
- Professional code organization
- Security best practices

---

## Repository

GitHub: [DocuMind-RAG-Assistant](https://github.com/prithvi-18/Agentic-AI-Developer-Certification-Program)

---

## Conclusion

This DocuMind-RAG-Assistant demonstrates a complete, production-ready implementation of Agentic AI concepts from Module 1. It combines proper software engineering practices with real AI functionality, serving as both a learning tool and a practical system for document-based question answering.

**Created for:** Ready Tensor Agentic AI Developer Certification  
**Module:** Module 1: Foundations of Agentic AI  
**Status:** ✅ Complete & Production Ready
