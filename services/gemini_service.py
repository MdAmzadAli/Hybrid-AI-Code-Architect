import asyncio
import os
from google import genai
from google.genai import types

class GeminiService:
    """
    Uses official google-genai SDK with clearly defined system roles.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    async def generate_code(self, prompt: str) -> str:

        system_instruction = """
You are a Senior Python Engineer.

Generate ONE complete Python solution.

STRICT RULES:
- Provide exactly ONE implementation.
- Do NOT generate alternative versions.
- Do NOT include commented-out code.
- Do NOT include multiple approaches.
- Do NOT include analysis or reasoning.
- Do NOT include markdown.
- Do NOT include docstrings.

COMMENTING RULES:
- Only add inline comments if the logic is non-trivial 
  and must be short to the point 
- Do NOT explain obvious code.
- Do NOT write multi-line comments.
- Do NOT include Args/Returns sections.

OUTPUT:
- Return only valid executable Python code.
- No explanation before or after the code.
"""

        response = await asyncio.get_event_loop().run_in_executor(
    None,
    lambda: self.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
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

        system_instruction = """
You are a Senior Security Engineer performing a professional code review.

Your responsibilities:
- Identify security vulnerabilities.
- Identify performance bottlenecks.
- Identify bad coding practices.
- Identify unsafe patterns.

STRICT OUTPUT RULES:
- Return bullet points only.
- Each issue must start with '- '.
- Be concise.
- If no issues exist, return exactly: LGTM
- Do NOT explain beyond bullet points.
- Do NOT include markdown formatting.
- Ignore commented-out code.
- Only review executable code.
"""


        response = await asyncio.get_event_loop().run_in_executor(
    None,
    lambda: self.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {"role": "user", "parts": [{"text": code}]}
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    ),
)

        text = response.text

        if not text or not text.strip():
            raise ValueError("Fallback reviewer returned empty")