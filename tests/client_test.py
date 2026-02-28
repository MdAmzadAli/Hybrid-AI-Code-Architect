import asyncio
import sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import json

async def main():
    params = StdioServerParameters(command=sys.executable, args=["server.py"])

    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            try:
                result = await session.call_tool(
                    "generate_and_review",
                    {"prompt": "Write a function to add 2 numbers."},
                )
                raw_text = result.content[0].text

                parsed = json.loads(raw_text)

                print("\n=== Generated Code ===\n")
                print(parsed["generated_code"])

                print("\n=== Security Review ===\n")
                print(parsed["security_review"])

                print("\n=== Reviewer Used ===\n")
                print(parsed["reviewer_used"])
            except Exception as e:
                print(f"Tool call failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())