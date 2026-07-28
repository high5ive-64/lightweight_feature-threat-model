#!/usr/bin/env bash
set -e

echo "Creating virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Copying environment example..."
cp -n .env.example .env || true

echo ""
echo "Setup complete. Edit .env with your API keys and configuration."
echo "Then run: uvicorn app.main:app --reload"