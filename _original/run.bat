@echo off

if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
    echo [2/3] Installing packages...
    .venv\Scripts\pip install --upgrade pip -q
    .venv\Scripts\pip install -r requirements.txt -q
    echo [3/3] Setup complete.
)

echo Starting Bookmark App -^> http://localhost:5000
.venv\Scripts\python app.py
