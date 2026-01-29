#!/usr/bin/env bash
set -e

APP_NAME="learning-dashboard-premium"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "==============================================="
echo "🚀 One Click Setup: $APP_NAME"
echo "==============================================="

# 1) check python
if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
  echo "❌ Python not found. Install python3 first."
  exit 1
fi

# 2) create venv
if [ ! -d ".venv" ]; then
  echo "✅ Creating virtual environment..."
  $PYTHON_BIN -m venv .venv
else
  echo "✅ Virtual env already exists"
fi

# 3) activate venv
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# 4) install requirements
echo "✅ Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5) Create uploads folder
mkdir -p uploads

# 6) Run App
echo "✅ Starting Streamlit..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
