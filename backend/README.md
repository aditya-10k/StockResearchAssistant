---
title: Stock Research Assistant Backend
emoji: 📈
colorFrom: gray
colorTo: blue
sdk: gradio
app_file: space.py
---

# Stock Research Assistant - Backend API

FastAPI agentic equity research pipeline powered by LangGraph, Groq (`qwen/qwen3.8-27b`), and yfinance.

## Hugging Face Spaces Setup

### 1. Repository Contents
Push the contents of the `backend/` folder to your Hugging Face Space:
- `space.py`
- `requirements.txt`
- `app/`

### 2. Environment Variables / Secrets
Go to your Space **Settings > Variables and Secrets** and add:
- `GROQ_API_KEY`: Your Groq API key (or `GEMINI_API_KEY` for Google Gemini)
- `LLM_PROVIDER`: `groq` (or `gemini`)
- `GROQ_MODEL`: `qwen/qwen3.8-27b`

### 3. Connecting Frontend
Your Space URL will be:
`https://<your-hf-username>-<space-name>.hf.space`

Build your Flutter frontend pointing to this backend:
```bash
flutter build web --dart-define=BACKEND_URL=https://<your-hf-username>-<space-name>.hf.space
```
