#!/bin/bash

# Check python3
if ! command -v python3 &> /dev/null; then
  echo "[ERROR] python3 not found."
  echo "  Ubuntu/Debian: sudo apt install python3"
  exit 1
fi

# Setup if .venv/bin/python is missing (also handles broken .venv)
if [ ! -f ".venv/bin/python" ]; then
  echo "[1/3] Creating virtual environment..."

  rm -rf .venv

  if ! python3 -m venv .venv; then
    echo ""
    echo "[ERROR] Failed to create virtual environment."
    echo "  Ubuntu/Debian: sudo apt install python3-venv python3-pip"
    exit 1
  fi

  echo "[2/3] Installing packages..."
  if ! .venv/bin/pip install --upgrade pip -q; then
    echo "[ERROR] Failed to upgrade pip."
    exit 1
  fi

  if ! .venv/bin/pip install -r requirements.txt -q; then
    echo "[ERROR] Failed to install packages."
    exit 1
  fi

  echo "[3/3] Setup complete."
fi

echo "Starting Bookmark App -> http://localhost:5000"
.venv/bin/python app.py
