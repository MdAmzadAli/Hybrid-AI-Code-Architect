import asyncio
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from prompts.system_prompts import SECURITY_REVIEW_PROMPT
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

        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(
            None,
            lambda: self.client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=500,
                system=SECURITY_REVIEW_PROMPT,
                messages=[{"role": "user", "content": code}],
            ),
        )

        review_text = (response.content[0].text or "").strip()
       
        if not review_text:
            return "LGTM"

        if review_text.upper() in {"NO ISSUES", "NO ISSUES FOUND", "NONE"}:
            return "LGTM"

        return review_text