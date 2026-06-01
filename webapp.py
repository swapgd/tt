"""
USATT Ratings Web App - Mobile-friendly PWA for looking up table tennis ratings.
Run: .venv/bin/python webapp.py
"""

import asyncio
import sys

sys.path.insert(0, "src")

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from usatt_mcp.client import USATTClient

app = FastAPI()
client = USATTClient()


@app.on_event("startup")
async def startup():
    await client.login()


@app.on_event("shutdown")
async def shutdown():
    await client.close()


@app.get("/api/my-rating")
async def my_rating():
    profile = await client.get_my_profile()
    return profile


@app.get("/api/search")
async def search(q: str, page: int = 1):
    results = await client.search_players(q, page_size=20, page_number=page)
    return results


@app.get("/api/player/{player_id}")
async def player_detail(player_id: str):
    profile = await client.get_player_profile(player_id)
    return profile


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_PAGE


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="USATT">
    <title>USATT Ratings</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 16px;
        }
        h1 {
            text-align: center;
            font-size: 1.4rem;
            margin-bottom: 16px;
            color: #00d4ff;
        }
        .search-box {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
        }
        input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #333;
            border-radius: 10px;
            background: #16213e;
            color: #eee;
            font-size: 16px;
            outline: none;
        }
        input:focus { border-color: #00d4ff; }
        button {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            background: #00d4ff;
            color: #1a1a2e;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        button:active { opacity: 0.7; }
        .my-btn {
            display: block;
            width: 100%;
            margin-bottom: 16px;
            background: #0f3460;
            color: #00d4ff;
            border: 1px solid #00d4ff;
        }
        .card {
            background: #16213e;
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 10px;
        }
        .card h3 {
            color: #00d4ff;
            font-size: 1rem;
            margin-bottom: 6px;
        }
        .card .rating {
            font-size: 1.8rem;
            font-weight: 700;
            color: #fff;
        }
        .card .league {
            font-size: 1.2rem;
            color: #aaa;
        }
        .card .meta {
            font-size: 0.85rem;
            color: #888;
            margin-top: 4px;
        }
        .loading {
            text-align: center;
            color: #888;
            padding: 20px;
        }
        .empty {
            text-align: center;
            color: #666;
            padding: 40px 20px;
        }
    </style>
</head>
<body>
    <h1>USATT Ratings</h1>
    <button class="my-btn" onclick="loadMyRating()">My Rating</button>
    <div class="search-box">
        <input type="text" id="search" placeholder="Search player name..."
               onkeydown="if(event.key==='Enter')doSearch()">
        <button onclick="doSearch()">Go</button>
    </div>
    <div id="results"></div>

    <script>
        const results = document.getElementById('results');

        async function loadMyRating() {
            results.innerHTML = '<div class="loading">Loading...</div>';
            try {
                const res = await fetch('/api/my-rating');
                const d = await res.json();
                results.innerHTML = renderProfile(d);
            } catch(e) {
                results.innerHTML = '<div class="empty">Error loading rating</div>';
            }
        }

        async function doSearch() {
            const q = document.getElementById('search').value.trim();
            if (!q) return;
            results.innerHTML = '<div class="loading">Searching...</div>';
            try {
                const res = await fetch('/api/search?q=' + encodeURIComponent(q));
                const d = await res.json();
                if (!d.players || d.players.length === 0) {
                    results.innerHTML = '<div class="empty">No players found</div>';
                    return;
                }
                results.innerHTML = d.players.map(p => `
                    <div class="card" onclick="loadPlayer('${p.playerId}')">
                        <h3>${p.playerName}</h3>
                        <span class="rating">${p.finalRating}</span>
                        <div class="meta">
                            Rank ${p.prefixedRank} &bull;
                            ${p.address || 'N/A'} &bull;
                            ${p.totalWins}W-${p.totalLost}L &bull;
                            ${p.clubName || 'No club'}
                        </div>
                    </div>
                `).join('');
            } catch(e) {
                results.innerHTML = '<div class="empty">Error searching</div>';
            }
        }

        async function loadPlayer(id) {
            results.innerHTML = '<div class="loading">Loading...</div>';
            try {
                const res = await fetch('/api/player/' + id);
                const d = await res.json();
                results.innerHTML = renderProfile(d);
            } catch(e) {
                results.innerHTML = '<div class="empty">Error loading player</div>';
            }
        }

        function renderProfile(d) {
            return `
                <div class="card">
                    <h3>${d.playerName}</h3>
                    <div>USATT# ${d.memberId}</div>
                    <div style="margin-top:10px">
                        <div class="rating">${d.highestRating}</div>
                        <div class="meta">Tournament Rating</div>
                    </div>
                    <div style="margin-top:8px">
                        <div class="league">${d.highestLeagueRating}</div>
                        <div class="meta">League Rating</div>
                    </div>
                    <div class="meta" style="margin-top:10px">
                        ${d.totalTournaments} tournaments &bull;
                        ${d.totalMatches} matches &bull;
                        ${d.totalWins}W-${d.totalLosses}L (${d.winPercentage}%)
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
