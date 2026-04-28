import json
import os
import boto3
import requests
from agent.orchestrator import run_agent

# Discord application ID - stored as environment variable
APPLICATION_ID = os.environ.get("DISCORD_APPLICATION_ID")

# Allowed Discord user IDs - stored as environment variable, comma-separated
ALLOWED_USERS = set(os.environ.get("ALLOWED_DISCORD_USERS", "").split(","))

def patch_discord_response(token: str, content: str):
    """Send the final response back to Discord."""
    url = f"https://discord.com/api/v10/webhooks/{APPLICATION_ID}/{token}/messages/@original"
    
    # Truncate if over Discord's 2000 character limit
    if len(content) > 2000:
        content = content[:1950] + "\n\n*(Response truncated due to length.)*"
    
    payload = {"content": content}
    headers = {"Content-Type": "application/json"}
    
    response = requests.patch(url, json=payload, headers=headers)
    return response.status_code

def lambda_handler(event, context):
    token = event.get("token")
    question = event.get("question")
    sender_id = event.get("sender_id")

    # Check if user is authorized
    if sender_id not in ALLOWED_USERS:
        patch_discord_response(
            token,
            "Sorry, you are not authorized to use this command."
        )
        return {"statusCode": 403}

    # Check that we have a question
    if not question:
        patch_discord_response(token, "No question was received.")
        return {"statusCode": 400}

    try:
        answer = run_agent(question)
        print(f"Agent answer: {answer}")  # visible in CloudWatch
        patch_discord_response(token, answer)
        return {"statusCode": 200}
    except Exception as e:
        patch_discord_response(
            token,
            "An error occurred while processing your question. Please try again."
        )
        print(f"Error: {str(e)}")
        return {"statusCode": 500}