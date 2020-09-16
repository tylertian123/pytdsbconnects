import aiohttp
import datetime
import time
import typing
from multidict import CIMultiDict

class TDSBConnects:

    API_URL = "https://zappsmaprd.tdsb.on.ca/"

    X_CLIENT_APP_INFO = "pytdsbconnects|||False|0.0.2|False|51|False)"

    def __init__(self, auto_refresh: bool=True, min_token_life: float=30.0):
        """
        Constructor.
        
        :param auto_refresh: Whether to automatically refresh the token.
        :param min_token_life: When a token is valid for less than this number of seconds,
                               it will be automatically refreshed.
        """
        self._auto_refresh = auto_refresh
        self._min_token_life = min_token_life
        self._token = None
        self._refresh_token = None
        self._token_expiry = None
        self._session = aiohttp.ClientSession(raise_for_status=True, headers={
            "X-Client-App-Info": self.X_CLIENT_APP_INFO,
        })

    def _update_auth(self, data: typing.Dict[str, typing.Any]):
        self._token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        self._token_expiry = time.time() + data["expires_in"]
        self._session._default_headers = CIMultiDict({
            "Authorization": "Bearer " + self._token,
            "X-Client-App-Info": self.X_CLIENT_APP_INFO,
        })
    
    async def login(self, username: str, password: str):
        resp = await self._session.post(self.API_URL + "token", data={
            "username": username,
            "password": password,
            "grant_type": "password",
        })
        self._update_auth(await resp.json())
    
    async def refresh_token(self):
        if self._refresh_token is None:
            return
        resp = await self._session.post(self.API_URL + "token", data={
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        })
        self._update_auth(await resp.json())
    
    async def refresh_if_expired(self):
        if self._refresh_token is None:
            return
        if time.time() + self._min_token_life >= self._token_expiry:
            await self.refresh_token()
    
    async def _get_endpoint(self, endpoint):
        if self._token is None:
            return
        if self._auto_refresh:
            await self.refresh_if_expired()
        resp = await self._session.get(self.API_URL + endpoint)
        data = await resp.json()
        return data
    
    async def get_timetable(self, school_id: int, date: datetime.date):
        url = f"/api/TimeTable/GetTimeTable/Student/{school_id}/{date.day:02d}{date.month:02d}{date.year}"
        return await self._get_endpoint(url)
    
    async def get_user_info(self):
        return await self._get_endpoint("api/Account/GetUserInfo")
