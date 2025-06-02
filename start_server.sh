#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables (optional)
export ENV=dev

# Start the FastAPI server using uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
