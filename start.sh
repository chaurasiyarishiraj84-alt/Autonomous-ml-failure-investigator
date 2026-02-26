#!/bin/bash

echo "Starting FastAPI backend..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Waiting for backend to start..."
sleep 5

echo "Starting Streamlit dashboard..."
python -m streamlit run ui/dashboard.py --server.port 7860 --server.address 0.0.0.0