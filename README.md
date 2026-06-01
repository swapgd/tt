# USATT Ratings MCP Server

An MCP (Model Context Protocol) server that looks up USA Table Tennis (USATT) player ratings from usatt.justgo.com.

## Tools

| Tool | Description |
|------|-------------|
| `get_my_rating` | Get your own tournament and league ratings |
| `search_player_rating` | Search players by name and return their ratings |
| `get_player_details` | Get detailed profile for a player by their PlayerId |

## Setup

### Prerequisites

- Python 3.10+ (uses `uv` to manage)
- A USATT account at [usatt.justgo.com](https://usatt.justgo.com)

### Install

```bash
uv venv --python 3.12 .venv
uv pip install -e .
```

### Configure

Copy `.env.example` to `.env` and fill in your USATT credentials:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### Use with Claude Code

The `.mcp.json` is pre-configured. Set the environment variables and open Claude Code in this directory:

```bash
export USATT_USERNAME="your_email@example.com"
export USATT_PASSWORD="your_password"
```

Then ask Claude things like:
- "What's my USATT rating?"
- "Look up the rating for Zhang Kai"
- "Search for players named Krish"

## How it works

1. Authenticates with usatt.justgo.com using your credentials
2. Uses the JustGo REST API to query player ratings and rankings
3. Exposes the data through MCP tools that Claude Code can call
