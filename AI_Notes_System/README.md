# AI Notes Management System

A full-stack Flask application that leverages Gemini AI to help users manage notes more effectively through summarization, extraction of key points, and quiz generation.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Copy `.env.example` to `.env` and add your `GEMINI_API_KEY`.

4. Run the app:
   ```bash
   python run.py
   ```

5. Visit `http://127.0.0.1:5000` in your browser.
