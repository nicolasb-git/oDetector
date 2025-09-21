#!/bin/bash
# setup.sh - Quick setup script for oDEtector on Linux

echo "Setting up oDEtector..."

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install it first:"
    echo "sudo apt install python3 python3-pip python3-venv python3-full"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the oDEtector directory."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv oDEtector_env

# Activate virtual environment
echo "Activating virtual environment..."
source oDEtector_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install torch torchvision transformers pillow

# Create images directory if it doesn't exist
mkdir -p images

# Create output directory if it doesn't exist
mkdir -p output

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To run the script:"
echo "1. source oDEtector_env/bin/activate"
echo "2. python3 main.py"
echo ""
echo "To deactivate the virtual environment when done:"
echo "deactivate"
