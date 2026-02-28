import asyncio
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeService:
    """
    Primary reviewer using Claude.
    Falls back automatically if API key is missing.
    """

    def __init__(self) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            self.client = None
        else:
            self.client = Anthropic(api_key=api_key)

    async def review_code(self, code: str) -> str:
        if not self.client:
            raise RuntimeError("Claude API key not configured.")

        system_prompt = (
            "You are a senior security engineer. "
            "Review the following Python code for security and performance issues. "
            "Respond with bullet points only. "
            "If no issues found, respond with 'LGTM'."
        )

        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=500,
                system=system_prompt,
                messages=[{"role": "user", "content": code}],
            ),
        )

        review_text = response.content[0].text

        if not review_text or not review_text.strip():
            raise ValueError("Claude returned empty review.")

        return review_text.strip()