#!/usr/bin/env bash
set -e

echo "=== Feature Threat Model - Setup ==="

# Check Python version
if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_CMD=python3.11
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
else
    echo "ERROR: python3 or python3.11 not found."
    echo "Install Python 3.11+ (e.g. brew install python@3.11)"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
$PYTHON_CMD -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
echo "Copying environment example (if .env doesn't exist)..."
cp -n .env.example .env || true

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Edit .env with your LM Studio (or other provider) settings."
echo "  2. Run: source .venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "To deactivate the virtual environment, run: deactivate"
echo "To remove the virtual environment, run: rm -rf .venv"
echo "To remove the .env file, run: rm .env"
echo "to run the app: source .venv/bin/activate && uvicorn app.main:app --reload"
echo "To test the application, run: curl http://127.0.0.1:8000/health"
echo "To test the application, run: curl http://127.0.0.1:8000/providers"