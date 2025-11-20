# Contributing to RAG Assistant - Module 1 Project

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Project Scope

This project is part of the **Ready Tensor Agentic AI Developer Certification Program - Module 1**. It demonstrates:
- Retrieval Augmented Generation (RAG) concepts from Weeks 1-3
- Document processing and chunking
- Vector embeddings and semantic search
- LLM integration with Groq API
- Production-level error handling and quality controls

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Suggesting Enhancements

We welcome suggestions for:
- Performance improvements
- Additional error handling
- New features that align with RAG concepts
- Documentation improvements
- Additional test cases

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests for new features

4. **Test your changes**
   ```bash
   # Run the system
   python examples/basic_example.py
   
   # Run edge case tests
   python test_edge_cases.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Clear description of what you added"
   git commit -m "Fix: Clear description of what you fixed"
   git commit -m "Update: Clear description of what you updated"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes you made and why

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Keep functions focused and small

### Error Handling
- Always use try-except blocks for external API calls
- Log errors with appropriate severity levels
- Provide user-friendly error messages
- Don't silence exceptions without logging

### Documentation
- Update README.md if you add new features
- Add inline comments for complex logic
- Update docstrings when changing function behavior
- Include examples in documentation

## Testing Guidelines

### Before Submitting
- [ ] Code runs without errors
- [ ] All existing tests pass
- [ ] New features have appropriate tests
- [ ] Documentation is updated
- [ ] Code follows style guidelines

### Test Cases to Consider
- Empty inputs
- Very long inputs
- Special characters
- Unicode/emoji
- API failures
- Network timeouts
- Invalid configurations

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Agentic-AI-Developer-Certification-Program.git
cd Agentic-AI-Developer-Certification-Program

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

## Project Structure

```
rag-assistant-module1/
├── src/                  # Core source code
│   ├── rag_system.py    # Main RAG implementation
│   ├── config.py        # Configuration
│   └── utils.py         # Helper functions
├── data/                # Sample documents
├── examples/            # Usage examples
├── screenshots/         # System demos
├── test_edge_cases.py   # Edge case tests
└── README.md            # Documentation
```

## What We're Looking For

### High Priority
- Bug fixes
- Performance improvements
- Additional test coverage
- Better error messages
- Documentation improvements

### Medium Priority
- New features aligned with RAG concepts
- Additional document formats support
- Enhanced logging
- Code refactoring

### Low Priority
- UI/UX improvements
- Additional examples
- Code style improvements

## Questions?

If you have questions about contributing:
1. Check the README.md for project documentation
2. Look through existing issues and pull requests
3. Create a new issue with your question

## Code of Conduct

- Be respectful and constructive
- Help others learn
- Focus on improving the project
- Welcome newcomers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to this educational project! 🎓
