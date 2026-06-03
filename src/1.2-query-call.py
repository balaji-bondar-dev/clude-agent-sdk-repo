import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions,AssistantMessage, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode="acceptEdits",
    )

    async for message in query(prompt="Create Hello-world.py file in src/", options=options):
        #print(message)
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(f"Claude Reasoning: {block.text}")  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Final Result: {message.subtype}")  # Final result
            
asyncio.run(main())