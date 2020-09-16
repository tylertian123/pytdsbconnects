import aiohttp
import asyncio
import datetime
import time
import typing
from multidict import CIMultiDict
from .objects import *

class TDSBConnects:

    API_URL = "https://zappsmaprd.tdsb.on.ca/"

    # Platform Name | Client App UUID | Current Time | First App Launch | Version Number | First Launch Current Version | Build Number | First Launch Current Build
    # The server will send a 401 if the build number isn't high enough, however it doesn't check if the number is too high
    # So 2147483647 should ensure that the lib always works
    # The server also doesn't verify any of the fields beside the build num
    X_CLIENT_APP_INFO = "pytdsbconnects||||0.0.0||2147483647|"

    def __init__(self, auto_refresh: bool=True, min_token_life: float=30.0):
        """
        Constructor.

        Although the session is created when the object is constructed, an access token
        is not obtained. login() must be called before any operations.
        
        :param auto_refresh: Whether to automatically refresh the token (default true).
        :param min_token_life: The minimum remaining time before expiry for a token
                               before it is refreshed (in seconds, default 30).
        """
        self._auto_refresh = auto_refresh
        self._min_token_life = min_token_life
        self._token = None
        self._refresh_token = None
        self._token_expiry = None
        self._session = aiohttp.ClientSession(raise_for_status=True, headers={
            "X-Client-App-Info": self.X_CLIENT_APP_INFO,
        })
    
    async def close(self) -> None:
        """
        Close the session.
        """
        await self._session.close()
        await asyncio.sleep(0.250)
    
    async def __aenter__(self) -> "TDSBConnects":
        return self
    
    async def __aexit__(self, exc, *exc_info):
        return await self.close()

    def _update_auth(self, data: typing.Dict[str, typing.Any]) -> None:
        """
        Updates the auth token, refresh token and expiry time.

        For internal use only.

        :param data: A dict containing the auth data.
        """
        self._token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        self._token_expiry = time.time() + data["expires_in"]
        self._session._default_headers = CIMultiDict({
            "Authorization": "Bearer " + self._token,
            "X-Client-App-Info": self.X_CLIENT_APP_INFO,
        })
    
    async def login(self, username: str, password: str) -> None:
        """
        Login to the system. This must be called before any operations.

        :param username: The username (student ID).
        :param password: The password.
        """
        resp = await self._session.post(self.API_URL + "token", data={
            "username": username,
            "password": password,
            "grant_type": "password",
        })
        self._update_auth(await resp.json())
    
    async def refresh_token(self) -> None:
        """
        Refresh the access token.
        """
        if self._refresh_token is None:
            return
        resp = await self._session.post(self.API_URL + "token", data={
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        })
        self._update_auth(await resp.json())
    
    async def refresh_if_expired(self) -> None:
        """
        Refresh the access token if it has expired.
        """
        if self._refresh_token is None:
            return
        if time.time() + self._min_token_life >= self._token_expiry:
            await self.refresh_token()
    
    async def _get_endpoint(self, endpoint) -> typing.Dict[str, typing.Any]:
        """
        Make a GET request to an endpoint.

        For internal use only.

        :param endpoint: The endpoint.
        """
        if self._token is None:
            return
        if self._auto_refresh:
            await self.refresh_if_expired()
        resp = await self._session.get(self.API_URL + endpoint)
        data = await resp.json()
        return data
    
    async def get_timetable(self, school_id: int, date: typing.Union[datetime.date, datetime.datetime]):
        url = f"api/TimeTable/GetTimeTable/Student/{school_id}/{date.day:02d}{date.month:02d}{date.year}"
        return await self._get_endpoint(url)
    
    async def get_user_info(self) -> User:
        return User(self, await self._get_endpoint("api/Account/GetUserInfo"))
