import json
import boto3
from dotenv import load_dotenv
from agent.prompts import SYSTEM_PROMPT
from mcp_server.server import execute_sql

load_dotenv()

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

client = boto3.client("bedrock-runtime", region_name="us-east-1")

TOOLS = [
    {
        "toolSpec": {
            "name": "execute_sql",
            "description": (
                "Execute a read-only SQL SELECT query against the GENS or SNES "
                "NHL '94 database. Use platform to specify which database to query."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "description": "Either 'gens' or 'snes'",
                            "enum": ["gens", "snes"]
                        },
                        "query": {
                            "type": "string",
                            "description": "A SQL SELECT statement"
                        }
                    },
                    "required": ["platform", "query"]
                }
            }
        }
    }
]

def run_agent(question: str) -> str:
    """
    Run the agentic loop for a given question.
    Returns the final formatted answer as a string.
    """
    messages = [{"role": "user", "content": [{"text": question}]}]

    while True:
        response = client.converse(
            modelId=MODEL_ID,
            system=[{"text": SYSTEM_PROMPT}],
            toolConfig={"tools": TOOLS},
            messages=messages
        )

        # Append assistant response to history
        output_message = response["output"]["message"]
        messages.append(output_message)

        stop_reason = response["stopReason"]

        # If no tool calls, we have our final answer
        if stop_reason == "end_turn":
            for block in output_message["content"]:
                if "text" in block:
                    return block["text"]
            return "No response generated."

        # Handle tool calls
        if stop_reason == "tool_use":
            tool_results = []

            for block in output_message["content"]:
                if "toolUse" in block:
                    tool_use = block["toolUse"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    tool_use_id = tool_use["toolUseId"]

                    if tool_name == "execute_sql":
                        result = execute_sql(
                            platform=tool_input["platform"],
                            query=tool_input["query"]
                        )
                    else:
                        result = json.dumps({
                            "error": f"Unknown tool: {tool_name}"
                        })

                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"text": result}]
                        }
                    })

            # Append tool results and loop
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("NHL '94 Agent ready. Type 'quit' to exit.\n")
    while True:
        question = input("Question: ").strip()
        if question.lower() == "quit":
            break
        if question:
            answer = run_agent(question)
            print(f"\nAnswer:\n{answer}\n")