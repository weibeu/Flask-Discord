import cachetools
import requests
import typing
import json
import os
import abc

from . import configs
from . import exceptions

from flask import session
from collections.abc import Mapping
from requests_oauthlib import OAuth2Session


class DiscordOAuth2HttpClient(abc.ABC):
    """An OAuth2 http abstract base class providing some factory methods.
    This class is meant to be overridden by :py:class:`flask_discord.DiscordOAuth2Session`
    and should not be used directly.

    Attributes
    ----------
    client_id : int
        The client ID of discord application provided.
    client_secret : str
        The client secret of discord application provided.
    redirect_uri : str
        The default URL to use to redirect user to after authorization.
    bot_token : str
        The bot token of the application. This is required when you also need to access bot scope resources
        beyond the normal resources provided by the OAuth. Can be also set to flask config with
        key ``DISCORD_BOT_TOKEN``.
    users_cache : cachetools.LFUCache
        Any dict like mapping to internally cache the authorized users. Preferably an instance of
        cachetools.LFUCache or cachetools.TTLCache. If not specified, default cachetools.LFUCache is used.
        Uses the default max limit for cache if ``DISCORD_USERS_CACHE_MAX_LIMIT`` isn't specified in app config.

    """

    SESSION_KEYS = [
        "DISCORD_USER_ID",
        "DISCORD_OAUTH2_STATE",
        "DISCORD_OAUTH2_TOKEN",
    ]

    def __init__(self, app, client_id=None, client_secret=None, redirect_uri=None, bot_token=None, users_cache=None):
        self.client_id = client_id or app.config["DISCORD_CLIENT_ID"]
        self.__client_secret = client_secret or app.config["DISCORD_CLIENT_SECRET"]
        self.redirect_uri = redirect_uri or app.config["DISCORD_REDIRECT_URI"]
        self.__bot_token = bot_token or app.config.get("DISCORD_BOT_TOKEN", str())
        self.users_cache = cachetools.LFUCache(
            app.config.get("DISCORD_USERS_CACHE_MAX_LIMIT", configs.DISCORD_USERS_CACHE_DEFAULT_MAX_LIMIT)
        ) if users_cache is None else users_cache
        if not issubclass(self.users_cache.__class__, Mapping):
            raise ValueError("Instance users_cache must be a mapping like object.")
        if "http://" in self.redirect_uri:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
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
    def _token_updater(token):
        session["DISCORD_OAUTH2_TOKEN"] = token

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
            token=token or session.get("DISCORD_OAUTH2_TOKEN"),
            state=state or session.get("DISCORD_OAUTH2_STATE"),
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.__client_secret,
            },
            auto_refresh_url=configs.DISCORD_TOKEN_URL,
            token_updater=self._token_updater)

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
        response = self._make_session(
        ).request(method, route, data, **kwargs) if oauth else requests.request(method, route, data=data, **kwargs)

        if response.status_code == 401:
            raise exceptions.Unauthorized
        if response.status_code == 429:
            raise exceptions.RateLimited(response)

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
