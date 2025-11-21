#!/bin/bash
# Setup script for Ethics Oversight Board automated consultation

echo "=================================="
echo "Ethics Oversight Board Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install anthropic package
echo "Installing required Python package (anthropic)..."
pip3 install anthropic

if [ $? -eq 0 ]; then
    echo "✓ anthropic package installed successfully"
else
    echo "❌ Failed to install anthropic package"
    exit 1
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Set your Anthropic API key:"
echo "   export ANTHROPIC_API_KEY='your-api-key-here'"
echo ""
echo "   Or add to your ~/.zshrc or ~/.bashrc for persistence:"
echo "   echo \"export ANTHROPIC_API_KEY='your-api-key-here'\" >> ~/.zshrc"
echo ""
echo "2. Run a consultation:"
echo "   python ethics-consultation.py \"Your ethical question here\""
echo ""
echo "3. Check QUICK-START.md for more usage examples"
echo ""
