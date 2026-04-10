"""
Groq Text Analysis Module for WELLORA
Uses AsyncGroq for fast, reliable text-based LLM interactions.
GLM-4V (image_analysis.py) handles vision — this module handles text only.
"""

import os
import logging
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Verify GROQ API key is present
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("[GLM-Text] GROQ_API_KEY is not set. Text responses will fail.")

# Note: We name it `glm_chat` so we don't have to touch main.py
GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"
_client = AsyncGroq(api_key=GROQ_API_KEY or "missing")

async def glm_chat(
    messages: list,
    temperature: float = 0.3,
    max_tokens: int = 400,
) -> str:
    """
    Async function to call Groq for text generation.
    Matches the existing GLM interface so main.py doesn't break.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not configured.")

    logger.info(f"[Groq] Calling {GROQ_TEXT_MODEL} with {len(messages)} messages...")
    try:
        completion = await _client.chat.completions.create(
            model=GROQ_TEXT_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = completion.choices[0].message.content
        logger.info(f"[Groq] Response received: {len(reply)} chars")
        return reply
    except Exception as e:
        logger.error(f"[Groq] Error calling API: {e}")
        raise e
