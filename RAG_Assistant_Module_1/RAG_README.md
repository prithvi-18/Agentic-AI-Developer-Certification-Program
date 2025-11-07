# RAG Assistant - Module 1 Project
## Ready Tensor Agentic AI Developer Certification

### Project Overview

This is a **Retrieval Augmented Generation (RAG) Assistant** built for the Ready Tensor Agentic AI Certification Module 1 Project. It demonstrates core concepts of agentic AI:
- Document ingestion and vectorization
- Semantic search and retrieval
- LLM integration with context grounding
- Multi-turn conversations with memory
- Safety and responsibility in AI systems

### What This Project Does

1. **Ingests documents** (PDF, markdown, text files)
2. **Converts to vectors** using embeddings
3. **Stores in vector database** (Chroma)
4. **Answers questions** based on document content
5. **Maintains conversation history** for context
6. **Prevents hallucinations** through source grounding

### Key Features

✅ **RAG Pipeline**: Complete retrieval + generation workflow
✅ **Document Processing**: Chunk documents intelligently
✅ **Semantic Search**: Find relevant content by meaning
✅ **Multi-turn Chat**: Remember conversation context
✅ **Source Attribution**: Know where answers come from
✅ **Production Ready**: Error handling and logging
✅ **Modular Design**: Easy to extend and customize

### Project Structure

```
rag-assistant-module1/
├── src/
│   ├── rag_system.py      # Core RAG implementation
│   ├── config.py          # Configuration settings
│   └── utils.py           # Helper functions
├── data/
│   └── sample_documents/  # Your documents here
├── examples/
│   ├── basic_example.py   # Quick start
│   └── interactive_chat.py # Full interactive mode
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

### Installation

**Prerequisites:**
- Python 3.8+
- Groq API key (free from https://console.groq.com/)

**Step 1: Clone or download the repository**
```bash
git clone <your-repo-url>
cd rag-assistant-module1
```

**Step 2: Create virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Setup environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

**Step 5: Add your documents**
```bash
# Copy your documents to data/sample_documents/
# Supported formats: .txt, .md, .pdf (with pdfplumber)
```

### Usage

#### Quick Start (Basic Example)
```bash
python examples/basic_example.py
```

This will:
1. Load sample documents
2. Build the RAG system
3. Ask sample questions
4. Show answers with sources

#### Interactive Chat
```bash
python examples/interactive_chat.py
```

This starts an interactive chat where you can:
- Ask questions about your documents
- Get answers grounded in source material
- See conversation history
- Type 'exit' to quit

### How It Works

#### 1. Document Ingestion
```python
rag_system = RAGAssistant("data/sample_documents/")
```
- Loads all documents from folder
- Splits into chunks (500 chars, 50 char overlap)
- Converts to embeddings (vector representations)

#### 2. Vector Storage
- Embeddings stored in Chroma vector database
- Local storage at `./chroma_data/`
- Persists between sessions

#### 3. Query Processing
```python
answer, sources = rag_system.query("What is ...?")
```
- User question converted to vector
- Semantic search finds top 3 relevant chunks
- Context built and sent to LLM
- Answer generated from context

#### 4. Response Generation
- Answer grounded in document content
- Cannot hallucinate beyond document scope
- Sources clearly referenced
- Multi-turn memory maintained

### Example Interactions

**Document Content:**
"Variational Autoencoders (VAEs) are generative models that learn efficient representations..."

**Query 1:**
```
User: What are VAEs?
Assistant: Variational Autoencoders (VAEs) are generative models that learn efficient 
representations. (Source: document1.txt, chunk 2)
```

**Query 2:**
```
User: How do they work?
Assistant: [Detailed explanation based on document]
(Source: document1.txt, chunks 2-3)
```

**Query 3 (Edge Case):**
```
User: What color are VAEs?
Assistant: This information is not covered in the provided documents.
```

### Technologies Used

- **LLM**: Groq (llama-3.3-70b-versatile)
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Vector DB**: Chroma
- **Framework**: LangChain
- **Language**: Python 3.8+

### Configuration

Edit `src/config.py` to customize:
- Model selection
- Chunk size and overlap
- Number of retrieved documents (k)
- Temperature and other LLM parameters

### Extending the Project

**Add new documents:**
```bash
# Just copy files to data/sample_documents/
cp your_document.txt data/sample_documents/
python examples/basic_example.py  # Re-index
```

**Customize embeddings:**
```python
# In config.py:
EMBEDDING_MODEL = "all-mpnet-base-v2"  # Different model
```

**Change LLM:**
```python
# In config.py:
LLM_MODEL = "mixtral-8x7b-32768"  # Different Groq model
```

### Limitations & Safety

✅ **Prevents hallucinations** - Can only answer from documents  
✅ **Source attribution** - Tracks where answers come from  
⚠️ **Quality depends on documents** - Garbage in = garbage out  
⚠️ **Semantic search isn't perfect** - May retrieve irrelevant chunks  
⚠️ **LLM can still misinterpret** - Always verify important info  

### Troubleshooting

**Q: "API key not found"**
- Check .env file exists
- Verify GROQ_API_KEY is set correctly
- Restart Python after changing .env

**Q: "No relevant documents found"**
- Ensure documents are in data/sample_documents/
- Check document format is supported
- Try simpler search queries

**Q: "Slow responses"**
- First run indexes documents (takes time)
- Subsequent runs are faster
- Reduce chunk_size in config if still slow

**Q: "Out of memory"**
- Reduce number of documents
- Smaller chunk size
- Reduce k (number of retrieved documents)

### Project Submission Notes

**For certification submission:**

1. ✅ Core RAG pipeline implemented
2. ✅ Document ingestion working
3. ✅ LLM integration complete
4. ✅ Interactive interface ready
5. ✅ Sample documents included
6. ✅ README documentation complete
7. ✅ Code is clean and commented
8. ✅ No hardcoded API keys (use .env)

**Submission Steps:**
1. Push to GitHub
2. Add link in Ready Tensor portal
3. Provide demo output
4. Write brief description

### Learning Outcomes

After completing this project, you understand:

- **RAG Systems**: How to build production RAG pipelines
- **Vector Databases**: Semantic search and retrieval
- **LLM Integration**: Grounding LLMs with external data
- **Agent Architecture**: Core components of agentic AI
- **Production Best Practices**: Structure, error handling, configuration
- **Document Processing**: Chunking, embedding, and indexing

### Next Steps (Beyond Module 1)

- **Module 2**: Build multi-agent systems
- **Week 4**: Advanced agent orchestration
- **Week 5+**: Production deployment, testing, monitoring

### Resources

- **LangChain Docs**: https://python.langchain.com/docs/
- **Chroma Docs**: https://docs.trychroma.com/
- **Groq API**: https://console.groq.com/docs
- **Ready Tensor Course**: https://app.readytensor.ai/certifications/

### License

This project is created as part of the Ready Tensor Agentic AI Certification.

### Support

For questions:
1. Check the troubleshooting section
2. Review code comments in `src/`
3. Check Ready Tensor course materials
4. Ask on Ready Tensor community

---

**Project Created**: November 2025  
**Status**: ✅ Production Ready  
**Version**: 1.0