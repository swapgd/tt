from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
from usatt_mcp.client import USATTClient


@asynccontextmanager
async def lifespan(server):
    client = USATTClient()
    await client.login()
    try:
        yield {"client": client}
    finally:
        await client.close()


mcp = FastMCP("USATT Ratings", lifespan=lifespan)


@mcp.tool()
async def get_my_rating(ctx) -> str:
    """Get your own USATT tournament and league ratings, match stats, and ranking."""
    client: USATTClient = ctx.request_context.lifespan_context["client"]
    profile = await client.get_my_profile()
    return (
        f"Player: {profile['playerName']}\n"
        f"USATT#: {profile['memberId']}\n"
        f"Tournament Rating: {profile['highestRating']}\n"
        f"League Rating: {profile['highestLeagueRating']}\n"
        f"Total Tournaments: {profile['totalTournaments']}\n"
        f"Total Matches: {profile['totalMatches']}\n"
        f"Record: {profile['totalWins']}W - {profile['totalLosses']}L ({profile['winPercentage']}%)"
    )


@mcp.tool()
async def search_player_rating(name: str, ctx) -> str:
    """Search for USATT table tennis players by name and return their ratings.

    Args:
        name: Player name to search (e.g. "Zhang" or "John Smith")
    """
    client: USATTClient = ctx.request_context.lifespan_context["client"]
    results = await client.search_players(name)
    players = results.get("players", [])

    if not players:
        return f"No players found matching '{name}'"

    lines = [f"Found {results['totalCount']} player(s) matching '{name}':\n"]
    for p in players:
        lines.append(
            f"  {p['playerName']} (USATT# {p['memberId']})\n"
            f"    Rating: {p['finalRating']} | Rank: {p['prefixedRank']}\n"
            f"    State: {p.get('address', 'N/A')} | Club: {p.get('clubName') or 'None'}\n"
            f"    Record: {p['totalWins']}W - {p['totalLost']}L\n"
        )
    return "\n".join(lines)


@mcp.tool()
async def get_player_details(player_id: str, ctx) -> str:
    """Get detailed profile for a specific player by their PlayerId (UUID).

    Args:
        player_id: The player's UUID (e.g. from search results)
    """
    client: USATTClient = ctx.request_context.lifespan_context["client"]
    profile = await client.get_player_profile(player_id)
    return (
        f"Player: {profile['playerName']}\n"
        f"USATT#: {profile['memberId']}\n"
        f"Tournament Rating: {profile['highestRating']}\n"
        f"League Rating: {profile['highestLeagueRating']}\n"
        f"Total Tournaments: {profile['totalTournaments']}\n"
        f"Total Matches: {profile['totalMatches']}\n"
        f"Record: {profile['totalWins']}W - {profile['totalLosses']}L ({profile['winPercentage']}%)"
    )


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
