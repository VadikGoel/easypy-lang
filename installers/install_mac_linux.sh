#!/bin/bash
echo "==================================================="
echo "  Installing Easypy Globally (Mac/Linux)"
echo "==================================================="
echo ""

# Check for Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Error: Python not found. Please install Python 3.10+"
    exit 1
fi

echo "1. Installing dependencies..."
$PYTHON_CMD -m pip install -r ../requirements.txt

echo ""
echo "2. Installing package..."
$PYTHON_CMD -m pip install -e ..

echo ""
echo "==================================================="
echo "  SUCCESS!"
echo "==================================================="
echo "You can now open a terminal and type:"
echo ""
echo "  easypy --version"
echo ""