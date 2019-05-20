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
        "discord_oauth2_state",
        "discord_oauth2_token",
    ]

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if "http://" in self.redirect_uri:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

    @staticmethod
    def _token_updater(token):
        session["discord_oauth2_token"] = token

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
            token=token or session.get("discord_oauth2_token"),
            state=state,
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            },
            auto_refresh_url=configs.TOKEN_URL,
            token_updater=self._token_updater)

    def get(self, route: str) -> dict:
        """Sends HTTP GET request to provided route or discord  endpoint.

        Note
        ----
        It automatically prefixes the API Base URL so you will just have to pass routes or URL endpoints.

        Parameters
        ----------
        route : str
            Route or endpoint URL to send HTTP GET request to. Example: ``/users/@me``

        Returns
        -------
        dict
            Dictionary containing received from sent HTTP GET request.

        Raises
        ------
        flask_discord.exceptions.Unauthorized
            Raises :py:class:`flask_discord.exceptions.Unauthorized` if current user is not authorized.

        """
        response = self._make_session().get(configs.API_BASE_URL + route)

        if response.status_code == 401:
            raise exceptions.Unauthorized

        return response.json()

    def get_json(self):
        discord_session = self._make_session(token=session.get("discord_oauth2_token"))
        user = discord_session.get(configs.API_BASE_URL + '/users/@me').json()
        guilds = discord_session.get(configs.API_BASE_URL + '/users/@me/guilds').json()
        connections = discord_session.get(configs.API_BASE_URL + '/users/@me/connections').json()
        return jsonify(user=user, guilds=guilds, connections=connections)
