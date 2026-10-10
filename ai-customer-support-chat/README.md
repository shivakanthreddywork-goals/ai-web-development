# AI Customer Support Chat

A small full-stack customer-support web app with a FastAPI backend and browser chat interface.

## Features
- Browser chat with conversation history
- Editable system prompt at `prompts/support_agent.md`
- Demo responses without an API key
- Optional OpenAI-compatible API integration
- Health endpoint at `/health`

## Run locally
```bash
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, optionally add an API key, then run:
```bash
uvicorn app:app --reload
```
Open `http://127.0.0.1:8000`.

Do not use as a production support system without authentication, rate limiting, monitoring, privacy review, and a verified knowledge base.
