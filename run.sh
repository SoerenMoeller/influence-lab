#!/bin/bash

# Start Svelte frontend in background
npm run dev -- --port 5173 &

# Start Python backend
cd backend
.venv/bin/python -m uvicorn main:app --reload --port 8000
