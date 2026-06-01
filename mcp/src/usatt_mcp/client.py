import httpx
from usatt_mcp.config import (
    USATT_USERNAME,
    USATT_PASSWORD,
    SITE_BASE,
    API_BASE,
    TOURNAMENT_RESULT_TYPE_ID,
)


class USATTClient:
    def __init__(self):
        self._http = httpx.AsyncClient(timeout=30, follow_redirects=True)
        self._jwt: str | None = None
        self._player_id: str | None = None
        self._user_id: int | None = None

    async def login(self):
        await self._http.get(SITE_BASE)
        resp = await self._http.post(
            f"{SITE_BASE}/Account.mvc/AuthenticateLogin",
            json={
                "payload": {
                    "userName": USATT_USERNAME,
                    "password": USATT_PASSWORD,
                    "rememberMe": "false",
                    "returnUrl": "",
                },
                "paths": [],
            },
            headers={"X-Requested-With": "XMLHttpRequest", "Origin": SITE_BASE},
        )
        data = resp.json()
        if data.get("type") != 0:
            raise RuntimeError(f"Login failed: {data.get('message', 'unknown error')}")

        self._jwt = self._http.cookies.get("jwt", "").replace("Bearer ", "")
        self._user_id = data["userId"]
        self._player_id = data["user"]["UserSyncId"]

    @property
    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._jwt}"}

    async def _ensure_auth(self):
        if not self._jwt:
            await self.login()

    async def _get(self, path: str, params: dict | None = None) -> dict:
        await self._ensure_auth()
        resp = await self._http.get(f"{API_BASE}{path}", params=params, headers=self._headers)
        if resp.status_code == 401:
            await self.login()
            resp = await self._http.get(f"{API_BASE}{path}", params=params, headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    async def get_my_profile(self) -> dict:
        await self._ensure_auth()
        data = await self._get(
            "/api/v1/events-results/get-player-profile",
            {"PlayerId": self._player_id},
        )
        return data["data"]

    async def get_player_profile(self, player_id: str) -> dict:
        data = await self._get(
            "/api/v1/events-results/get-player-profile",
            {"PlayerId": player_id},
        )
        return data["data"]

    async def search_players(self, search_term: str, page_size: int = 10, page_number: int = 1) -> dict:
        data = await self._get(
            "/api/v1/events-results/rankings",
            {
                "SearchTerm": search_term,
                "ResultEventTypeId": TOURNAMENT_RESULT_TYPE_ID,
                "PageSize": page_size,
                "PageNumber": page_number,
            },
        )
        return data["data"]

    async def close(self):
        await self._http.aclose()
