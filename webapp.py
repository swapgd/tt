"""
USATT Ratings PWA - Mobile-friendly app with per-user authentication.
Run: .venv/bin/python webapp.py
"""

import sys

sys.path.insert(0, "src")

import json
import httpx
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from usatt_mcp.config import SITE_BASE, API_BASE, TOURNAMENT_RESULT_TYPE_ID

LOGIN_LOG = Path(__file__).parent / "logins.jsonl"

app = FastAPI()


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/login")
async def login(req: LoginRequest):
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        await client.get(SITE_BASE)
        resp = await client.post(
            f"{SITE_BASE}/Account.mvc/AuthenticateLogin",
            json={
                "payload": {
                    "userName": req.username,
                    "password": req.password,
                    "rememberMe": "false",
                    "returnUrl": "",
                },
                "paths": [],
            },
            headers={"X-Requested-With": "XMLHttpRequest", "Origin": SITE_BASE},
        )
        data = resp.json()
        if data.get("type") != 0:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        jwt_token = client.cookies.get("jwt", "").replace("Bearer ", "")
        name = f"{data['user']['FirstName']} {data['user']['LastName']}"
        with LOGIN_LOG.open("a") as f:
            f.write(json.dumps({
                "ts": datetime.now(timezone.utc).isoformat(),
                "name": name,
                "userId": data["userId"],
            }) + "\n")
        return {
            "token": jwt_token,
            "playerId": data["user"]["UserSyncId"],
            "name": name,
            "userId": data["userId"],
        }


@app.get("/api/my-rating")
async def my_rating(player_id: str, token: str):
    return await _api_get(
        token,
        "/api/v1/events-results/get-player-profile",
        {"PlayerId": player_id},
    )


@app.get("/api/search")
async def search(q: str, token: str, page: int = 1):
    return await _api_get(
        token,
        "/api/v1/events-results/rankings",
        {
            "SearchTerm": q,
            "ResultEventTypeId": TOURNAMENT_RESULT_TYPE_ID,
            "PageSize": "20",
            "PageNumber": str(page),
        },
    )


@app.get("/api/player/{player_id}")
async def player_detail(player_id: str, token: str):
    return await _api_get(
        token,
        "/api/v1/events-results/get-player-profile",
        {"PlayerId": player_id},
    )


async def _api_get(token: str, path: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}{path}",
            params=params,
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code == 401:
            raise HTTPException(status_code=401, detail="Session expired")
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", data)


@app.get("/api/stats")
async def stats():
    if not LOGIN_LOG.exists():
        return {"total_logins": 0, "unique_users": 0, "users": []}
    entries = [json.loads(line) for line in LOGIN_LOG.read_text().splitlines() if line.strip()]
    unique = {}
    for e in entries:
        uid = e["userId"]
        if uid not in unique:
            unique[uid] = {"name": e["name"], "first_seen": e["ts"], "logins": 0}
        unique[uid]["logins"] += 1
        unique[uid]["last_seen"] = e["ts"]
    return {
        "total_logins": len(entries),
        "unique_users": len(unique),
        "users": sorted(unique.values(), key=lambda u: u["first_seen"]),
    }


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
    <meta name="apple-mobile-web-app-title" content="TT Ratings">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%231a1a2e' width='100' height='100' rx='20'/><text y='70' x='15' font-size='60'>🏓</text></svg>">
    <title>TT Ratings</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            min-height: 100dvh;
            padding: 16px;
            padding-top: env(safe-area-inset-top, 16px);
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
            cursor: pointer;
        }
        .card:active { opacity: 0.8; }
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
        .loading { text-align: center; color: #888; padding: 20px; }
        .empty { text-align: center; color: #666; padding: 40px 20px; }
        .error { text-align: center; color: #ff6b6b; padding: 20px; }
        .login-form {
            max-width: 320px;
            margin: 60px auto;
        }
        .login-form input {
            display: block;
            width: 100%;
            margin-bottom: 12px;
        }
        .login-form button {
            width: 100%;
            margin-top: 4px;
        }
        .login-form .subtitle {
            text-align: center;
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 20px;
        }
        .logout-btn {
            position: absolute;
            top: 16px;
            right: 16px;
            background: none;
            border: none;
            color: #666;
            font-size: 0.8rem;
            padding: 4px 8px;
        }
        .user-greeting {
            text-align: center;
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <div id="app"></div>

    <script>
        const app = document.getElementById('app');

        function getSession() {
            try {
                const s = localStorage.getItem('usatt_session');
                return s ? JSON.parse(s) : null;
            } catch { return null; }
        }

        function saveSession(data) {
            localStorage.setItem('usatt_session', JSON.stringify(data));
        }

        function clearSession() {
            localStorage.removeItem('usatt_session');
            render();
        }

        async function apiFetch(url) {
            const session = getSession();
            if (!session) { render(); return null; }
            const sep = url.includes('?') ? '&' : '?';
            const resp = await fetch(url + sep + 'token=' + encodeURIComponent(session.token));
            if (resp.status === 401) {
                // Try re-login with saved credentials
                const creds = getSavedCreds();
                if (creds) {
                    const ok = await doLogin(creds.username, creds.password, true);
                    if (ok) {
                        const session2 = getSession();
                        const resp2 = await fetch(url + sep + 'token=' + encodeURIComponent(session2.token));
                        if (resp2.ok) return resp2.json();
                    }
                }
                clearSession();
                return null;
            }
            if (!resp.ok) throw new Error('Request failed');
            return resp.json();
        }

        function getSavedCreds() {
            try {
                const c = localStorage.getItem('usatt_creds');
                return c ? JSON.parse(c) : null;
            } catch { return null; }
        }

        function saveCreds(username, password) {
            localStorage.setItem('usatt_creds', JSON.stringify({username, password}));
        }

        async function doLogin(username, password, silent) {
            if (!silent) {
                app.querySelector('.login-form button').textContent = 'Logging in...';
                app.querySelector('.login-form button').disabled = true;
            }
            try {
                const resp = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password}),
                });
                if (!resp.ok) {
                    if (!silent) {
                        app.querySelector('.login-form button').textContent = 'Sign In';
                        app.querySelector('.login-form button').disabled = false;
                        app.querySelector('.error-msg').textContent = 'Invalid email or password';
                    }
                    return false;
                }
                const data = await resp.json();
                saveSession(data);
                saveCreds(username, password);
                if (!silent) render();
                return true;
            } catch(e) {
                if (!silent) {
                    app.querySelector('.login-form button').textContent = 'Sign In';
                    app.querySelector('.login-form button').disabled = false;
                    app.querySelector('.error-msg').textContent = 'Connection error';
                }
                return false;
            }
        }

        function renderLogin() {
            const creds = getSavedCreds();
            app.innerHTML = `
                <div class="login-form">
                    <h1>🏓 TT Ratings</h1>
                    <p class="subtitle">Sign in with your USATT account</p>
                    <input type="email" id="email" placeholder="Email" value="${creds?.username || ''}">
                    <input type="password" id="password" placeholder="Password" value="${creds?.password || ''}">
                    <button onclick="handleLogin()">Sign In</button>
                    <p class="error-msg error" style="margin-top:12px"></p>
                </div>
            `;
        }

        function handleLogin() {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            if (!email || !password) return;
            doLogin(email, password, false);
        }

        function renderApp() {
            const session = getSession();
            app.innerHTML = `
                <button class="logout-btn" onclick="clearSession()">Logout</button>
                <h1>🏓 TT Ratings</h1>
                <p class="user-greeting">Hi, ${session.name}</p>
                <button class="my-btn" onclick="loadMyRating()">My Rating</button>
                <div class="search-box">
                    <input type="text" id="search" placeholder="Search player name..."
                           onkeydown="if(event.key==='Enter')doSearch()">
                    <button onclick="doSearch()">Go</button>
                </div>
                <div id="results"></div>
            `;
        }

        async function loadMyRating() {
            const session = getSession();
            const results = document.getElementById('results');
            results.innerHTML = '<div class="loading">Loading...</div>';
            try {
                const d = await apiFetch('/api/my-rating?player_id=' + session.playerId);
                if (d) results.innerHTML = renderProfile(d);
            } catch(e) {
                results.innerHTML = '<div class="error">Error loading rating</div>';
            }
        }

        async function doSearch() {
            const q = document.getElementById('search').value.trim();
            if (!q) return;
            const results = document.getElementById('results');
            results.innerHTML = '<div class="loading">Searching...</div>';
            try {
                const d = await apiFetch('/api/search?q=' + encodeURIComponent(q));
                if (!d) return;
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
                results.innerHTML = '<div class="error">Error searching</div>';
            }
        }

        async function loadPlayer(id) {
            const results = document.getElementById('results');
            results.innerHTML = '<div class="loading">Loading...</div>';
            try {
                const d = await apiFetch('/api/player/' + id + '?x=1');
                if (d) results.innerHTML = renderProfile(d);
            } catch(e) {
                results.innerHTML = '<div class="error">Error loading player</div>';
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

        function render() {
            const session = getSession();
            if (session && session.token) {
                renderApp();
            } else {
                renderLogin();
            }
        }

        // Handle Enter key on login
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && document.getElementById('password')) {
                handleLogin();
            }
        });

        render();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
