import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage

async def main():
    # Use the ClaudeSDKClient to send a query and receive responses
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")

        # process responses for question
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())