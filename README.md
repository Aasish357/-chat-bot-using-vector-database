# AI Chatbot using Vector Databases

This is a chatbot application that uses Google's Gemini AI to answer questions about PDF documents. It processes PDFs, creates vector embeddings, and provides intelligent responses based on the document content.

## Features

- PDF document processing and text extraction
- Vector database storage using FAISS
- Google Gemini 1.5 Flash integration
- Support for local PDF files and URLs (Google Drive, Google Docs)
- Interactive question-answering interface

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Clone or download this project**

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Get a Google Gemini API key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key

2. **Create a .env file**:
   - Copy `env_template.txt` to `.env`
   - Add your API key and file path:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   FILE_PATH=/path/to/your/document.pdf
   ```

## Usage

1. **Run the application**:
   ```bash
   python app.py
   ```

2. **Ask questions** about your document:
   - The chatbot will process your PDF and create a knowledge base
   - Type questions and get AI-powered answers
   - Type 'exit' to quit

## Supported File Sources

- Local PDF files
- Google Drive links
- Google Docs links
- Direct PDF URLs

## Example Questions

- "What is the main topic of this document?"
- "Summarize the key points"
- "What does the document say about [specific topic]?"
- "List the main conclusions"

## Troubleshooting

- **Python not found**: Make sure Python is installed and added to PATH
- **API key error**: Verify your Google Gemini API key is correct
- **File not found**: Check the file path in your .env file
- **Import errors**: Run `pip install -r requirements.txt` to install dependencies
