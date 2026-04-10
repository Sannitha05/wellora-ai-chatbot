"""
Medical Image Analysis Module using ZhipuAI's GLM-4.6V-Flash
Two-step approach:
  Step 1 – Classification: Is the image medical or not?
  Step 2 – Analysis: Only runs if Step 1 confirms "medical".
"""

import os
import base64
import asyncio
import logging
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")
GLM_BASE_URL = "https://api.z.ai/api/paas/v4/chat/completions"
GLM_MODEL = "glm-4.6v-flash"  # ZhipuAI Vision model

# Maximum image size (3 MB in bytes)
MAX_IMAGE_SIZE = 3 * 1024 * 1024

# Fixed rejection message for non-medical images
NON_MEDICAL_RESPONSE = "I'm a healthcare assistant and can only help with medical and health-related queries. Please ask a health question and I'll be happy to assist! 🏥"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

# Step 1: Classification prompt — binary answer only
CLASSIFICATION_PROMPT = """Look at this image and answer with ONE word only.

Medical images are ONLY: X-ray, MRI, CT scan, ECG, lab report, prescription, or skin disease/wound photo.

If the image is any of those → reply: medical
If the image is ANYTHING else (food, objects, people, animals, scenery, etc.) → reply: non-medical
If you are not sure → reply: non-medical

Output ONE word only. No explanation. No punctuation."""

# Step 2: Full analysis prompt — only called for confirmed medical images
ANALYSIS_PROMPT = """You are WELLORA, a professional medical image analysis AI.

Analyze this medical image and generate a structured report in this exact format:

Medical Image Analysis Report

Image Type:
[X-ray / MRI / CT scan / ECG / Lab Report / Prescription / Skin Condition]

Observed Findings:
• [Finding 1]
• [Finding 2]
• [Finding 3]

Possible Interpretation:
• [Brief clinical explanation — not a diagnosis]

Urgency Level:
[Low / Moderate / High]

Recommended Action:
• [Next step]
• [Consultation advice]

Follow-Up Guidance:
• [Additional tests if needed]
• [Monitoring advice]

Confidence Level:
[Percentage based on image clarity]

Disclaimer:
This analysis is AI-generated for educational purposes only and is not a medical diagnosis. Please consult a qualified healthcare professional.

RULES:
- Do NOT diagnose
- Do NOT prescribe dosage
- Be concise and clinical
- No repetition"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _decode_base64_image(data_url: str) -> bytes:
    """Strip the data-URI prefix and decode to raw bytes."""
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    return base64.b64decode(data_url)


def _get_base64_from_data_url(data_url: str) -> str:
    """Extract raw base64 string from a data URL."""
    if "," in data_url:
        return data_url.split(",", 1)[1]
    return data_url


def _validate_image_size(image_bytes: bytes) -> str | None:
    """Return an error message if the image is too large, else None."""
    if len(image_bytes) > MAX_IMAGE_SIZE:
        size_mb = len(image_bytes) / (1024 * 1024)
        return f"Image too large ({size_mb:.1f} MB). Maximum allowed is {MAX_IMAGE_SIZE // (1024*1024)} MB."
    return None


def _build_payload(image_b64: str, prompt: str, max_tokens: int = 10) -> dict:
    """Build the GLM-4V API request payload."""
    return {
        "model": GLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": max_tokens
    }


# ---------------------------------------------------------------------------
# Core API call
# ---------------------------------------------------------------------------

def _should_retry(exc):
    if isinstance(exc, aiohttp.ClientResponseError):
        return exc.status in [429, 503, 504]
    if isinstance(exc, asyncio.TimeoutError):
        return True
    return False


async def _call_glm(payload: dict, headers: dict) -> str:
    """Make a single GLM-4V API call and return the text response."""

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception(_should_retry),
        reraise=True
    )
    async def _execute(pl, hdrs):
        async with aiohttp.ClientSession() as session:
            async with session.post(GLM_BASE_URL, headers=hdrs, json=pl, timeout=30.0) as resp:
                if resp.status in [400, 429, 503, 504]:
                    error_body = await resp.text()
                    logger.error(f"[GLM-4V] API error (Status {resp.status}): {error_body}")
                    raise aiohttp.ClientResponseError(
                        resp.request_info, resp.history,
                        status=resp.status, message=error_body
                    )
                resp.raise_for_status()
                data = await resp.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    return await _execute(payload, headers)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def analyze_medical_image(data_url: str) -> dict | None:
    """
    Two-step medical image analysis:
    1. Classify the image (medical / non-medical).
    2. Only analyze if confirmed medical.
    Returns a dict with 'summary' key, or None on setup failure.
    """
    if not ZHIPUAI_API_KEY:
        logger.warning("[GLM-4V] ZHIPUAI_API_KEY not set – skipping image analysis.")
        return None

    # Decode & validate
    try:
        image_bytes = _decode_base64_image(data_url)
    except Exception as e:
        logger.error(f"[GLM-4V] Failed to decode image: {e}")
        return None

    size_error = _validate_image_size(image_bytes)
    if size_error:
        return {"summary": size_error, "error": size_error}

    image_b64 = _get_base64_from_data_url(data_url)
    headers = {
        "Authorization": f"Bearer {ZHIPUAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # ------------------------------------------------------------------
    # STEP 1: Classify the image
    # ------------------------------------------------------------------
    try:
        logger.info("[GLM-4V] Step 1: Classifying image (medical / non-medical)...")
        classify_payload = _build_payload(image_b64, CLASSIFICATION_PROMPT, max_tokens=10)
        classification_raw = await _call_glm(classify_payload, headers)
        classification = classification_raw.strip().lower().split()[0] if classification_raw.strip() else "non-medical"
        logger.info(f"[GLM-4V] Classification result: '{classification}'")
    except Exception as e:
        logger.error(f"[GLM-4V] Classification call failed: {e}. Defaulting to non-medical.")
        classification = "non-medical"

    # ------------------------------------------------------------------
    # STEP 2: Block non-medical images immediately in code
    # ------------------------------------------------------------------
    if "medical" not in classification or "non" in classification:
        logger.info("[GLM-4V] Non-medical image detected. Returning rejection message.")
        return {
            "summary": NON_MEDICAL_RESPONSE,
            "caption": NON_MEDICAL_RESPONSE,
            "model": GLM_MODEL,
            "status": "non_medical"
        }

    # ------------------------------------------------------------------
    # STEP 3: Full medical analysis (only reached for medical images)
    # ------------------------------------------------------------------
    try:
        logger.info("[GLM-4V] Step 2: Running medical image analysis...")
        analysis_payload = _build_payload(image_b64, ANALYSIS_PROMPT, max_tokens=800)
        analysis_text = await _call_glm(analysis_payload, headers)

        if not analysis_text:
            logger.warning("[GLM-4V] Received empty analysis response")
            return {"summary": "Model returned an empty analysis.", "model": GLM_MODEL}

        logger.info(f"[GLM-4V] Analysis received: {len(analysis_text)} chars")
        return {
            "summary": analysis_text,
            "raw_analysis": analysis_text,
            "caption": "Image analyzed successfully.",
            "model": GLM_MODEL,
            "status": "success"
        }

    except aiohttp.ClientResponseError as e:
        logger.error(f"[GLM-4V] Analysis API error (Status {e.status}): {e.message}")
        if e.status == 429:
            return {"summary": "Analysis unavailable: Rate limit exceeded. Please try again later.", "status": "rate_limited"}
        if e.status == 401:
            return {"summary": "Analysis unavailable: Invalid API key.", "status": "error"}
        if e.status == 400:
            return {"summary": "Image analysis request rejected by API as ill-formatted.", "status": "error"}
        return {"summary": f"Analysis failed: HTTP {e.status} Server Error", "status": "error"}

    except asyncio.TimeoutError:
        logger.error("[GLM-4V] Analysis request timed out.")
        return {"summary": "Analysis timed out. Please try again.", "status": "timeout"}

    except Exception as e:
        logger.exception(f"[GLM-4V] Unexpected error: {type(e).__name__}: {e}")
        return {"summary": f"Analysis failed: {str(e)[:100]}", "status": "error"}
