import asyncio
import json
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from services.gemini_service import GeminiService
from services.claude_service import ClaudeService


server = Server("Hybrid-AI-Code-Architect")

gemini_service = GeminiService()
claude_service = ClaudeService()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="generate_and_review",
            description="Generates Python code using Gemini and reviews it using Claude. Includes fallback and self-correction loop.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The coding task or requirement to generate Python code for."
                    }
                },
                "required": ["prompt"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name != "generate_and_review":
        raise ValueError(f"Unknown tool: {name}")

    prompt = arguments.get("prompt", "")

    try:
        # STEP 1 — Generate Code
        generated_code = await gemini_service.generate_code(prompt)

        # STEP 2 — Try Claude Review
        try:
            review = await claude_service.review_code(generated_code)
            reviewer_used = "claude"
        except Exception:
            review = await gemini_service.review_code_fallback(generated_code)
            reviewer_used = "gemini_fallback"

        # STEP 3 — Self-Correction Loop
        if review != "LGTM":
            refactor_prompt = (
                f"Refactor the following Python code to fix these issues:\n\n"
                f"Issues:\n{review}\n\n"
                f"Original Code:\n{generated_code}"
            )

            generated_code = await gemini_service.generate_code(refactor_prompt)

            try:
                review = await claude_service.review_code(generated_code)
                reviewer_used = "claude_after_refactor"
            except Exception:
                review = await gemini_service.review_code_fallback(generated_code)
                reviewer_used = "gemini_fallback_after_refactor"

        result = {
            "generated_code": generated_code,
            "security_review": review,
            "reviewer_used": reviewer_used
        }

    except Exception as e:
        result = {
            "generated_code": "",
            "security_review": f"Critical failure: {str(e)}",
            "reviewer_used": "none"
        }

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())