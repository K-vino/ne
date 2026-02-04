#!/bin/bash

# NEXORA AI - Startup Script
# This script starts the backend server

echo "🧠 Starting NEXORA AI - Decision Intelligence System"
echo "=================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python version: $python_version"

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing now..."
    pip install -r requirements.txt
fi

echo "✓ Dependencies installed"
echo ""

# Start the server
echo "🚀 Starting backend server..."
echo "   URL: http://localhost:8000"
echo "   Press CTRL+C to stop"
echo ""

python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
