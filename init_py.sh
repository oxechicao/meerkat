#!/bin/bash
# Setup script for Meerkat CLI

echo "Setting up Meerkat CLI..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x meerkat.py
chmod +x mrkt

echo ""
echo "Setup complete!"
echo ""
echo "To use mrkt globally, add this directory to your PATH or create a symlink:"
echo "  sudo ln -s $(pwd)/mrkt /usr/local/bin/mrkt"
echo ""
echo "Or run it directly from this directory:"
echo "  ./mrkt --help"
