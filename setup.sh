#!/usr/bin/env bash
set -e

echo "Creating virtual environment with python3..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Copying environment example (if .env doesn't exist)..."
cp -n .env.example .env || true

echo ""
echo "Setup complete. Edit .env with your API keys and configuration."
echo "Then run: source .venv/bin/activate && uvicorn app.main:app --reload"
echo "To deactivate the virtual environment, run: deactivate"
echo "To remove the virtual environment, run: rm -rf .venv"
echo "To remove the .env file, run: rm .env"
echo "To test the application, run: curl http://127.0.0.1:8000/health"
echo "To test the application, run: curl http://127.0.0.1:8000/providers"