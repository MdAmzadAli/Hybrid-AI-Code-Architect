import asyncio
import os
from google import genai
from google.genai import types
from prompts.system_prompts import CODE_GENERATOR_PROMPT, SECURITY_REVIEW_PROMPT

from utils.logger import logger

import sys

class GeminiService:
    """
    Uses official google-genai SDK with clearly defined system roles.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    async def generate_code(self, prompt: str) -> str:

        response = await asyncio.get_event_loop().run_in_executor(
    None,
    lambda: self.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        config=types.GenerateContentConfig(
            system_instruction=CODE_GENERATOR_PROMPT
        )
    ),
)
        text = response.text.strip()

        if not text:
            raise ValueError("Gemini returned empty response")

        # Extra safety strip markdown if it still appears
        text = text.replace("```python", "").replace("```", "").strip()

        return text

    async def review_code_fallback(self, code: str) -> str:
        """
        Gemini fallback reviewer acting as a strict security auditor.
        """

        response = await asyncio.get_event_loop().run_in_executor(
    None,
    lambda: self.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {"role": "user", "parts": [{"text": code}]}
        ],
        config=types.GenerateContentConfig(
            system_instruction=SECURITY_REVIEW_PROMPT
        )
    ),
)

        text = (response.text or "").strip()

        if not text:
            return "LGTM"

        if text.upper() in {"NO ISSUES", "NO ISSUES FOUND", "NONE"}:
            return "LGTM"

        return text