import os
from pathlib import Path
from typing import List, Literal
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI(title="AI Customer Support Chat", version="1.0.0")
HTML_FILE = Path(__file__).parent / "static" / "index.html"
SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "support_agent.md").read_text(encoding="utf-8")

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(min_length=1, max_length=30)

class ChatResponse(BaseModel):
    reply: str
    mode: str

def demo_reply(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ["refund", "return", "money back"]):
        return ("I can help explain a return process, but this demo is not connected to a real company policy. "
                "Check the official return policy and contact a human agent for account-specific decisions.")
    if any(word in lowered for word in ["human", "agent", "person", "complaint"]):
        return "A human support agent should review this request. Please use the support contact listed on the company's official website."
    if any(word in lowered for word in ["price", "cost", "plan", "subscription"]):
        return "Pricing can change. Check the company's current pricing page. If you paste the available plans here, I can help compare them."
    return ("Thanks for your question. This demo is not connected to a real company knowledge base. "
            "Share a relevant help article or policy and I can help summarize it.")

def generate_reply(messages):
    if not os.getenv("OPENAI_API_KEY"):
        return demo_reply(messages[-1].content), "demo"
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    chat_messages += [{"role": m.role, "content": m.content} for m in messages]
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=chat_messages,
        temperature=0.2,
    )
    return response.choices[0].message.content, "live AI"

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_FILE.read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply, mode = generate_reply(request.messages)
    return ChatResponse(reply=reply, mode=mode)
