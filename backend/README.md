# Multi-modal Search Backend

This project is a simplified Flask backend for a multi-modal search engine. It provides APIs for uploading files, background processing, and performing semantic search using Qdrant and Ollama models.

## Setup

1. Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and adjust settings.
3. Run the application:
   ```bash
   python run.py
   ```

This will start the Flask development server and create database tables automatically.
