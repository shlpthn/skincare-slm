import os
from pathlib import Path
from typing import List, Dict

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# -------------------------------------------------------------
# PATHS & CONSTANTS
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

OLLAMA_MODEL_NAME = "skincareslm"
OLLAMA_BASE_URL = "http://localhost:11434"

SYSTEM_PROMPT_PATH = BASE_DIR / "data" / "system_prompt.txt"
SKINCARE_KB_PATH = BASE_DIR / "data" / "skincare_kb.txt"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text().strip()
SKINCARE_KB_TEXT = SKINCARE_KB_PATH.read_text().strip()


# -------------------------------------------------------------
# KNOWLEDGE BASE
# -------------------------------------------------------------
def load_kb() -> Dict[str, str]:
    kb = {}
    for line in SKINCARE_KB_TEXT.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        kb[key.strip().lower()] = value.strip()
    return kb


KB_DICT = load_kb()
KB_KEYWORDS = set(KB_DICT.keys())


# -------------------------------------------------------------
# UTILITIES
# -------------------------------------------------------------
def is_skincare_query(text: str) -> bool:
    t = text.lower()
    generic_words = [
        "skin","face","pimple","acne","moisturizer","cream","sunscreen",
        "spf","oil","dryness","blackhead","whitehead","toner","serum",
        "retinol","vitamin c","niacinamide","bha","aha"
    ]
    return any(w in t for w in generic_words) or any(k in t for k in KB_KEYWORDS)


def get_kb(msg: str) -> str:
    t = msg.lower()
    for key, info in KB_DICT.items():
        if key in t:
            return info
    return ""


def clean_text(t: str) -> str:
    if not t:
        return ""
    t = t.replace("Answer:", "").replace("answer:", "").strip()
    t = t.lstrip(":").strip()
    return t

def build_prompt(user_msg: str, kb_info: str):
    prompt = SYSTEM_PROMPT.strip() + "\n\n"

    prompt += f"User message: {user_msg.strip()}\n"

    if kb_info:
        prompt += f"Relevant info: {kb_info}\n"

    prompt += "Answer:"
    return prompt.strip()

def generate_from_model(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
    data = resp.json()
    return data.get("response", "").strip()
    

def clean_text(t: str):
    bad = ["Assistant:", "assistant:", "User:", "user:"]
    for b in bad:
        t = t.replace(b, "")
    return t.strip()

# -------------------------------------------------------------
# FASTAPI INITIALIZATION
# -------------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []


# -------------------------------------------------------------
# MAIN CHAT ENDPOINT
# -------------------------------------------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.strip()

    if not is_skincare_query(msg):
        return {"reply": "I can answer only skincare-related questions."}

    kb_info = get_kb(msg)
    prompt = build_prompt(msg,kb_info)
    reply = generate_from_model(prompt)
    reply = clean_text(reply)

    return {"reply": reply}
