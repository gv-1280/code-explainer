#!/bin/bash
set -e

echo "🚀 Starting AI Code Assistant..."

# Start FastAPI backend in background
echo "📡 Starting FastAPI backend on port 8000..."
uvicorn backend.server:app --host 0.0.0.0 --port 8000 &

# Wait a moment for FastAPI to start
sleep 5

# Start Streamlit frontend
echo "🌐 Starting Streamlit frontend on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

# Keep the container running
wait