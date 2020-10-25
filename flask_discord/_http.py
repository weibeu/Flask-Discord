import cachetools
import requests
import typing
import json
import abc

from . import configs
from . import exceptions

from flask import session, request
from collections.abc import Mapping
from requests_oauthlib import OAuth2Session


class DiscordOAuth2HttpClient(abc.ABC):
    """An OAuth2 http abstract base class providing some factory methods.
    This class is meant to be overridden by :py:class:`flask_discord.DiscordOAuth2Session` and should not be
    used directly.

    """

    SESSION_KEYS = [
        "DISCORD_USER_ID",
        "DISCORD_OAUTH2_STATE",
        "DISCORD_OAUTH2_TOKEN",
    ]

    def __init__(
            self, app=None,
            client_id=None, client_secret=None, redirect_uri=None,
            bot_token=None, users_cache=None, proxy=None, proxy_auth=None
    ):
        self.client_id = client_id
        self.__client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.__bot_token = bot_token
        self.users_cache = users_cache
        self.proxy = proxy
        self.proxy_auth = proxy_auth

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """A method to lazily initialize the application.
        Use this when you're using flask factory pattern to create your instances of your flask application.

        Parameters
        ----------
        app : Flask
            An instance of your `flask application <http://flask.pocoo.org/docs/1.0/api/#flask.Flask>`_.

        """
        self.client_id = self.client_id or app.config["DISCORD_CLIENT_ID"]
        self.__client_secret = self.__client_secret or app.config["DISCORD_CLIENT_SECRET"]
        self.redirect_uri = self.redirect_uri or app.config["DISCORD_REDIRECT_URI"]
        self.__bot_token = self.__bot_token or app.config.get("DISCORD_BOT_TOKEN", str())
        self.users_cache = cachetools.LFUCache(
            app.config.get("DISCORD_USERS_CACHE_MAX_LIMIT", configs.DISCORD_USERS_CACHE_DEFAULT_MAX_LIMIT)
        ) if self.users_cache is None else self.users_cache
        if not issubclass(self.users_cache.__class__, Mapping):
            raise ValueError("Instance users_cache must be a mapping like object.")
        self.proxy = self.proxy or app.config.get("DISCORD_PROXY_SETTINGS")
        self.proxy_auth = self.proxy_auth or app.config.get("DISCORD_PROXY_AUTH_SETTINGS")
        app.discord = self

    @property
    def user_id(self) -> typing.Union[int, None]:
        """A property which returns Discord user ID if it exists in flask :py:attr:`flask.session` object.

        Returns
        -------
        int
            The Discord user ID of current user.
        None
            If the user ID doesn't exists in flask :py:attr:`flask.session`.

        """
        return session.get("DISCORD_USER_ID")

    @staticmethod
    @abc.abstractmethod
    def save_authorization_token(token: dict):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_authorization_token() -> dict:
        raise NotImplementedError

    def _fetch_token(self, state):
        discord = self._make_session(state=state)
        return discord.fetch_token(
            configs.DISCORD_TOKEN_URL,
            client_secret=self.__client_secret,
            authorization_response=request.url
        )

    def _make_session(self, token: str = None, state: str = None, scope: list = None) -> OAuth2Session:
        """A low level method used for creating OAuth2 session.

        Parameters
        ----------
        token : str, optional
            The authorization token to use which was previously received from authorization code grant.
        state : str, optional
            The state to use for OAuth2 session.
        scope : list, optional
            List of valid `Discord OAuth2 Scopes
            <https://discordapp.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes>`_.

        Returns
        -------
        OAuth2Session
            An instance of OAuth2Session class.

        """
        return OAuth2Session(
            client_id=self.client_id,
            token=token or self.get_authorization_token(),
            state=state,
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.__client_secret,
            },
            auto_refresh_url=configs.DISCORD_TOKEN_URL,
            token_updater=self.save_authorization_token)

    def request(self, route: str, method="GET", data=None, oauth=True, **kwargs) -> typing.Union[dict, str]:
        """Sends HTTP request to provided route or discord endpoint.

        Note
        ----
        It automatically prefixes the API Base URL so you will just have to pass routes or URL endpoints.

        Parameters
        ----------
        route : str
            Route or endpoint URL to send HTTP request to. Example: ``/users/@me``
        method : str, optional
            Specify the HTTP method to use to perform this request.
        data : dict, optional
            The optional payload the include with the request.
        oauth : bool
            A boolean determining if this should be Discord OAuth2 session request or any standard request.

        Returns
        -------
        dict, str
            Dictionary containing received from sent HTTP GET request if content-type is ``application/json``
            otherwise returns raw text content of the response.

        Raises
        ------
        flask_discord.Unauthorized
            Raises :py:class:`flask_discord.Unauthorized` if current user is not authorized.
        flask_discord.RateLimited
            Raises an instance of :py:class:`flask_discord.RateLimited` if application is being rate limited by Discord.

        """
        route = configs.DISCORD_API_BASE_URL + route

        if self.proxy is not None:
            kwargs["proxy"] = self.proxy
        if self.proxy_auth is not None:
            kwargs["proxy_auth"] = self.proxy_auth

        response = self._make_session(
        ).request(method, route, data, **kwargs) if oauth else requests.request(method, route, data=data, **kwargs)

        if response.status_code == 401:
            raise exceptions.Unauthorized()
        if response.status_code == 429:
            raise exceptions.RateLimited(response.json(), response.headers)

        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text

    def bot_request(self, route: str, method="GET", **kwargs) -> typing.Union[dict, str]:
        """Make HTTP request to specified endpoint with bot token as authorization headers.

        Parameters
        ----------
        route : str
            Route or endpoint URL to send HTTP request to.
        method : str, optional
            Specify the HTTP method to use to perform this request.

        Returns
        -------
        dict, str
            Dictionary containing received from sent HTTP GET request if content-type is ``application/json``
            otherwise returns raw text content of the response.

        Raises
        ------
        flask_discord.Unauthorized
            Raises :py:class:`flask_discord.Unauthorized` if current user is not authorized.
        flask_discord.RateLimited
            Raises an instance of :py:class:`flask_discord.RateLimited` if application is being rate limited by Discord.

        """
        headers = {"Authorization": f"Bot {self.__bot_token}"}
        return self.request(route, method=method, oauth=False, headers=headers, **kwargs)
