# NHL94 MCP Query Server

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?logo=awslambda&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock-FF9900?logo=amazonaws&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blueviolet)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)

An agentic AI system that answers natural language questions about NHL '94 video game statistics. Built with Anthropic's Model Context Protocol (MCP), powered by Claude via Amazon Bedrock, and deployed as an AWS Lambda function connected to a Discord bot.

---

## Background

NHL '94 is a classic hockey video game originally released for the Sega Genesis and Super Nintendo. It has maintained a small but dedicated community of enthusiasts who have been playing in online leagues for over 20 years. This project provides a natural language query interface over a large dataset of game statistics accumulated across those leagues — over 74,000 games and counting, spanning more than a decade of competition.

---

## What It Does

A Discord user invokes the `/qmcpquery` slash command with a plain English question:

```
/qmcpquery question: Who led the GENS Classic leagues in points per game among forwards with at least 100 games played?
```

The system figures out which database tables to query, writes the SQL, executes it, and returns a formatted answer — all without the user writing a single line of SQL.

---

## Architecture

```
Discord Slash Command (/qmcpquery)
            ↓
SNESCupChaseDiscordBotInteraction (Lambda)
  - Verifies Discord signature
  - Routes command
  - Invokes NHL94MCPQuery as async Event
  - Returns immediate ACK to Discord
            ↓
NHL94MCPQuery (Lambda)
  - Downloads .db files from S3 to /tmp
  - Runs the agentic loop
  - PATCHes the Discord interaction with the final answer
            ↓
  ┌─────────────────────────────┐
  │     Agentic Loop            │
  │                             │
  │  Claude (via Bedrock)       │
  │    ↓ writes SQL             │
  │  MCP Client                 │
  │    ↓ tool call              │
  │  MCP Server                 │
  │    ↓ executes query         │
  │  SQLite (.db files in /tmp) │
  │    ↓ returns results        │
  │  Claude formats response    │
  └─────────────────────────────┘
            ↓
Discord Response
```

---

## What Makes This Interesting

### Agentic AI with MCP
This project uses Anthropic's **Model Context Protocol (MCP)** — a relatively new open standard for connecting AI models to external tools and data sources. The MCP server exposes a single `execute_sql` tool. Claude calls this tool one or more times per question, reasoning about which tables to query and in what order, until it has enough information to formulate a complete answer.

### Claude Writes the SQL
Rather than hardcoding query logic for every possible question, Claude dynamically generates SQL based on a detailed schema document embedded in the system prompt. This means the system can answer questions that were never anticipated at build time. A well-crafted schema description does the heavy lifting — Claude reads the table structures, column definitions, and domain-specific notes, then writes correct SQL for a remarkably wide range of questions.

### Deferred Discord Response Pattern
Discord requires a response within 3 seconds of a slash command. Since an LLM query takes much longer than that, the system uses a deferred response pattern: the interaction Lambda immediately ACKs the command, then invokes the worker Lambda asynchronously. The worker Lambda PATCHes the original interaction with the final answer once it's ready.

---

## Database Structure

The system queries two SQLite databases — one for the Sega Genesis version of NHL '94 and one for the Super Nintendo version. Each database contains five tables:

- **matches** — one row per game, containing aggregate team statistics
- **skaters** — one row per skater per game
- **goalies** — one row per goalie per game
- **goals** — one row per goal, with scorer, assistants, strength, and timing
- **penalties** — one row per penalty, with player, infraction type, and timing

The databases are stored in an S3 bucket and updated twice daily by a separate Lambda process. The query Lambda downloads fresh copies on every invocation.

---

## Example Questions and Answers

*[Tickenest — add your favorite example questions and answers here]*

---

## Project Structure

```
NHL94-MCP-Query-Server/
├── lambda_function.py       — Lambda handler, Discord PATCH, user allowlist
├── deploy.ps1               — Deployment script (Windows)
├── deploy.sh                — Deployment script (Mac/Linux)
├── requirements.txt         — Python dependencies
├── README.md
├── agent/
│   ├── orchestrator.py      — Agentic loop, Bedrock API calls, tool dispatch
│   └── prompts.py           — System prompt with embedded schema
├── mcp_server/
│   └── server.py            — MCP server, execute_sql tool definition
├── schema/
│   └── schema.md            — Full database schema documentation
├── docs/
│   └── example_questions.md — Example queries and responses
└── data/
    └── README.md            — Instructions for obtaining database files
```

---

## Local Development Setup

### Prerequisites
- Python 3.12+
- AWS CLI configured with appropriate credentials
- Access to the NHL '94 database files (see `data/README.md`)

### Installation

```bash
git clone https://github.com/Tickenest/NHL94-MCP-Query-Server.git
cd NHL94-MCP-Query-Server
python -m venv .venv
source .venv/bin/activate  # Windows (Git Bash): source .venv/Scripts/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GENS_DB_PATH=data/gensDatabase.db
SNES_DB_PATH=data/snesDatabase.db
AWS_DEFAULT_REGION=us-east-1
AWS_PROFILE=your-aws-profile
S3_BUCKET=your-s3-bucket-name
```

### Running Locally

```bash
python -m agent.orchestrator
```

This starts an interactive command line interface for testing questions directly without Discord.

---

## AWS Deployment

### Prerequisites
- AWS Lambda function created (`NHL94MCPQuery`)
- IAM execution role with S3 read, Bedrock invoke, and CloudWatch logs permissions
- Claude Haiku 4.5 model access enabled in Amazon Bedrock
- Docker installed (required for building Linux-compatible deployment packages on Windows)
- Environment variables configured in the Lambda console:
  - `DISCORD_APPLICATION_ID`
  - `ALLOWED_DISCORD_USERS` (comma-separated Discord user IDs)
  - `GENS_DB_PATH` → `/tmp/gensDatabase.db`
  - `SNES_DB_PATH` → `/tmp/snesDatabase.db`
  - `S3_BUCKET` → your S3 bucket name

### Deploy

**Windows:**
```powershell
.\deploy.ps1
```

**Mac/Linux:**
```bash
./deploy.sh
```

The deployment scripts use Docker to build a Linux-compatible package, ensuring compiled dependencies work correctly in the Lambda runtime.

---

## Discord Integration

The `/qmcpquery` slash command is handled by a separate Discord bot interaction Lambda. The payload contract between the interaction Lambda and `NHL94MCPQuery` is:

```json
{
    "token": "discord_interaction_token",
    "question": "Your question here, including GENS or SNES",
    "sender_id": "discord_user_id"
}
```

Access to the command is restricted to an allowlist of Discord user IDs configured via the `ALLOWED_DISCORD_USERS` environment variable.

---

## Known Data Notes

- The `toi` (time on ice) column in the skaters and goalies tables is only available in the GENS database
- Some games record `toi = 0` rather than `NULL` when time on ice was not captured
- When calculating per-game statistics involving the penalties table, the system uses the skaters table for game counts rather than the penalties table, since a player only appears in the penalties table for games where they committed a penalty

---

## Built By

[Tickenest](https://github.com/Tickenest)
