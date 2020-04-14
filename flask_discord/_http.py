import os
import abc

from . import configs
from . import exceptions

from flask import session, jsonify
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

    """

    SESSION_KEYS = [
        "DISCORD_OAUTH2_STATE",
        "DISCORD_OAUTH2_TOKEN",
    ]

    def __init__(self, app):
        self.client_id = app.config["DISCORD_CLIENT_ID"]
        self.client_secret = app.config["DISCORD_CLIENT_SECRET"]
        self.redirect_uri = app.config["DISCORD_REDIRECT_URI"]
        if "http://" in self.redirect_uri:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

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
            state=state,
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            },
            auto_refresh_url=configs.DISCORD_TOKEN_URL,
            token_updater=self._token_updater)

    def request(self, route: str, method="GET", data=None, **kwargs) -> dict:
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

        Returns
        -------
        dict
            Dictionary containing received from sent HTTP GET request.

        Raises
        ------
        flask_discord.Unauthorized
            Raises :py:class:`flask_discord.Unauthorized` if current user is not authorized.

        """
        response = self._make_session().request(method, configs.DISCORD_API_BASE_URL + route, data, **kwargs)

        if response.status_code == 401:
            raise exceptions.Unauthorized

        return response.json()

    def get_json(self):
        user = self.request('/users/@me')
        guilds = self.request('/users/@me/guilds')
        connections = self.request('/users/@me/connections')
        return jsonify(user=user, guilds=guilds, connections=connections)
