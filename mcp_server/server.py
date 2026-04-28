import sqlite3
import json
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import os

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"

DB_PATHS = {
    "gens": Path(os.environ.get("GENS_DB_PATH", str(DATA_DIR / "gensDatabase.db"))),
    "snes": Path(os.environ.get("SNES_DB_PATH", str(DATA_DIR / "snesDatabase.db"))),
}

mcp = FastMCP("nhl94-agent")

@mcp.tool()
def execute_sql(platform: str, query: str) -> str:
    """
    Execute a read-only SQL SELECT query against the GENS or SNES NHL '94 database.

    Args:
        platform: Either 'gens' or 'snes'
        query: A SQL SELECT statement

    Returns:
        JSON string of query results as a list of row dicts
    """
    if platform not in DB_PATHS:
        return json.dumps({
            "error": f"Unknown platform '{platform}'. Must be 'gens' or 'snes'."
        })

    # Diagnostic logging
    db_path = DB_PATHS[platform]

    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({
            "error": "Only SELECT queries are permitted."
        })

    try:
        conn = sqlite3.connect(DB_PATHS[platform])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return json.dumps(rows)
    except sqlite3.Error as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def search_leagues(platform: str, search_term: str) -> str:
    """
    Search for league names in the database that match a search term.
    Use this when the user refers to a league by an approximate or partial name.
    Returns a list of matching exact league names.

    Args:
        platform: Either 'gens' or 'snes'
        search_term: A partial or approximate league name to search for

    Returns:
        JSON string containing a list of matching league names
    """
    if platform not in DB_PATHS:
        return json.dumps({
            "error": f"Unknown platform '{platform}'. Must be 'gens' or 'snes'."
        })

    try:
        conn = sqlite3.connect(DB_PATHS[platform])
        cursor = conn.cursor()

        words = search_term.strip().split()
        conditions = " AND ".join([
            f"league LIKE ?" for _ in words
        ])
        params = [f"%{word}%" for word in words]

        cursor.execute(f"""
            SELECT DISTINCT league
            FROM matches
            WHERE {conditions}
            ORDER BY league
        """, params)

        leagues = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not leagues:
            return json.dumps({
                "message": "No leagues found matching that search term.",
                "matches": []
            })

        return json.dumps({
            "message": f"Found {len(leagues)} matching league(s).",
            "matches": leagues
        })

    except sqlite3.Error as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    mcp.run()