import json
import os
import boto3
from dotenv import load_dotenv
from agent.prompts import SYSTEM_PROMPT
from mcp_server.server import execute_sql, search_leagues

load_dotenv()

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

# S3 configuration
S3_BUCKET = os.environ.get("S3_BUCKET", "nhl94dbs")
DB_FILES = {
    "gensDatabase.db": os.environ.get("GENS_DB_PATH", "data/gensDatabase.db"),
    "snesDatabase.db": os.environ.get("SNES_DB_PATH", "data/snesDatabase.db"),
}

def download_databases():
    """Download .db files from S3 to the path specified in environment variables."""
    s3 = boto3.client("s3")
    for filename, local_path in DB_FILES.items():
        print(f"Downloading {filename} from S3 to {local_path}...")
        s3.download_file(S3_BUCKET, filename, local_path)
        print(f"Download complete. File exists: {os.path.exists(local_path)}")

def is_lambda() -> bool:
    """Check if we are running inside AWS Lambda."""
    return os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

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
    },
    {
        "toolSpec": {
            "name": "search_leagues",
            "description": (
                "Search for exact league names in the database using a partial "
                "or approximate search term. Use this whenever the user refers "
                "to a league by an approximate, partial, or informal name before "
                "constructing a SQL query that filters by league."
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
                        "search_term": {
                            "type": "string",
                            "description": (
                                "A partial or approximate league name to search "
                                "for. Use individual words or partial strings. "
                                "For example: 'Classic Fall 2023' or 'Chaos Spring'."
                            )
                        }
                    },
                    "required": ["platform", "search_term"]
                }
            }
        }
    }
]

def run_agent(question: str) -> str:
    """
    Run the agentic loop for a given question.
    Downloads databases from S3 if running in Lambda.
    Returns the final formatted answer as a string.
    """
    if is_lambda():
        download_databases()

    messages = [{"role": "user", "content": [{"text": question}]}]

    while True:
        response = bedrock.converse(
            modelId=MODEL_ID,
            system=[{"text": SYSTEM_PROMPT}],
            toolConfig={"tools": TOOLS},
            messages=messages
        )

        output_message = response["output"]["message"]
        messages.append(output_message)

        stop_reason = response["stopReason"]

        if stop_reason == "end_turn":
            for block in output_message["content"]:
                if "text" in block:
                    return block["text"]
            return "No response generated."

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
                    elif tool_name == "search_leagues":
                        result = search_leagues(
                            platform=tool_input["platform"],
                            search_term=tool_input["search_term"]
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