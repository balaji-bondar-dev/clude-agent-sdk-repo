import asyncio
from claude_agent_sdk import query, tool, create_sdk_mcp_server, ClaudeAgentOptions, AssistantMessage, ResultMessage

# Define tools using the @tool decorator
@tool("add", "Add two numbers", {"a": float, "b": float})
async def add(args):
    return {"content": [{"type": "text", "text": f"Sum: {args['a'] + args['b']}"}]}


@tool("multiply", "Multiply two numbers", {"a": float, "b": float})
async def multiply(args):
    return {"content": [{"type": "text", "text": f"Product: {args['a'] * args['b']}"}]}

# Create an MCP server with the defined tools
calculator = create_sdk_mcp_server(
    name="calculator",
    version="2.0.0",
    tools=[add, multiply],  # Pass decorated functions
)

# Example usage of the MCP server in a query
async def main():
    # Set up agent options to use the MCP server and specify allowed tools
    options = ClaudeAgentOptions(
        system_prompt="You are an expert mathematics assistant",
        permission_mode="acceptEdits",
        mcp_servers={"calc": calculator},
        allowed_tools=["mcp__calc__add", "mcp__calc__multiply"],
    )
    # Query that uses the tools defined in the MCP server
    async for message in query(prompt="what is the addition of 5 and 3?", options=options):
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