#!/bin/bash
# ResumeAI Pro - Quick Setup Script

echo "🚀 ResumeAI Pro - Setup Script"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Setup environment
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo "  ⚠️  IMPORTANT: Edit .env and add your GROQ_API_KEY"
else
    echo "✓ .env already exists"
fi

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python3 -c "from database import DB; DB.init()"
echo "✓ Database initialized"

# Ready to launch
echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY from console.groq.com"
echo "2. Run: streamlit run app.py"
echo "3. Open: http://localhost:8501"
echo ""
echo "======================================"
