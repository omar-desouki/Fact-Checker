#!/bin/bash

echo "🚀 Enhanced RAG Fact Checker - Unix/Linux/macOS Launcher"
echo "======================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.8+ from python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Check if fact-checker.py exists
if [ ! -f "fact-checker.py" ]; then
    echo "❌ fact-checker.py not found in current directory"
    exit 1
fi

# Check for API key
if [ -z "$GOOGLE_API_KEY" ] && [ ! -f "config.py" ]; then
    echo "⚠️  Google API key not configured!"
    echo "   Please either:"
    echo "   1. Set environment variable: export GOOGLE_API_KEY='your-key'"
    echo "   2. Copy config_template.py to config.py and add your key"
    echo "   3. Edit fact-checker.py directly"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Launch the application
echo "🌐 Starting Enhanced RAG Fact Checker..."
echo "   Interface will be available at: http://localhost:7860"
echo "   Press Ctrl+C to stop the application"
echo "======================================================="

python3 fact-checker.py
