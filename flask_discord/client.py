from . import configs, _http, models

from flask import request, session, redirect


class DiscordOAuth2Session(_http.DiscordOAuth2HttpClient):
    """Main client class representing hypothetical OAuth2 session with discord.
    It uses Flask `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ local proxy object
    to save state, authorization token and keeps record of users sessions across different requests.
    This class inherits :py:class:`flask_discord._http.DiscordOAuth2HttpClient` class.

    Parameters
    ----------
    client_id : int
        Client ID of your discord application.
    client_secret : str
        Client secret of your discord application.
    redirect_uri : str
        The default URL to be used to redirect user after the OAuth2 authorization.

    """

    def create_session(self, scope: list = None):
        """Primary method used to create OAuth2 session and redirect users for
        authorization code grant.

        Parameters
        ----------
        scope : list, optional
            An optional list of valid `Discord OAuth2 Scopes
            <https://discordapp.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes>`_.

        Returns
        -------
        redirect
            Flask redirect to discord authorization servers to complete authorization code grant process.

        """
        scope = scope or request.args.get("scope", str()).split() or configs.DEFAULT_SCOPES
        discord_session = self._make_session(scope=scope)
        authorization_url, state = discord_session.authorization_url(configs.AUTHORIZATION_BASE_URL)
        session["discord_oauth2_state"] = state
        return redirect(authorization_url)

    def callback(self, fetch_user: bool = True):
        """A method which should be always called after completing authorization code grant process
        usually in callback view.
        It fetches the authorization token and saves it flask
        `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object.

        Parameters
        ----------
        fetch_user : bool, optional
            If this parameter is set to True, it caches :py:class:`flask_discord.models.User` to flask
            `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object with ``discord_user`` key
            and ``None`` if False.

        """
        if request.values.get("error"):
            return request.values["error"]
        discord = self._make_session(state=session.get("discord_oauth2_state"))
        token = discord.fetch_token(
            configs.TOKEN_URL,
            client_secret=self.client_secret,
            authorization_response=request.url
        )
        session["discord_oauth2_token"] = token
        if fetch_user:
            session["discord_user"] = self.fetch_user()
        else:
            session["discord_user"] = None

    def revoke(self):
        """This method clears current discord token, state and all session data from flask
        `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_. Which means user will have
        to go through discord authorization token grant flow again.

        """
        for session_key in self.SESSION_KEYS:
            session.pop(session_key)

    @property
    def authorized(self):
        """A boolean indicating whether current session has authorization token or not."""
        return self._make_session().authorized

    def fetch_user(self) -> models.User:
        """This method requests current user data from discord, caches native :py:class:`flask_discord.models.User`
        to flask `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object.

        Returns
        -------
        flask_discord.models.User

        """
        session["discord_user"] = models.User(self.get("/users/@me"))
        return session["discord_user"]

    @property
    def user(self) -> models.User:
        """A property which returns cached current :py:class:`flask_discord.models.User` from flask
        `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object.

        Note
        ----
        If user is not present in flask `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_
        object, it requests user data from discord, caches user to session and then returns user object.

        Returns
        -------
        flask_discord.models.User
            Cached discord user object form flask `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_.

        """
        return session.get("discord_user") or self.fetch_user()

    def fetch_connections(self) -> models.UserConnection:
        """Requests and returns connections of current user from discord.

        Returns
        -------
        flask_discord.models.UserConnection

        """
        return models.UserConnection(self.get("/users/@me/connections"))

    def fetch_guilds(self) -> list:
        """Requests and returns guilds of current user from discord.

        Returns
        -------
        list
            List of :py:class:`flask_discord.models.Guild` objects.

        """
        guilds_payload = self.get("/users/@me/guilds")
        return [models.Guild(payload) for payload in guilds_payload]
