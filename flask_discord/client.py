import jwt
import typing

from . import configs, _http, models, utils, exceptions, types

from flask import request, session, redirect, current_app
from oauthlib.common import add_params_to_uri, generate_token


class DiscordOAuth2Session(_http.DiscordOAuth2HttpClient):
    """Main client class representing hypothetical OAuth2 session with discord.
    It uses Flask `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ local proxy object
    to save state, authorization token and keeps record of users sessions across different requests.
    This class inherits :py:class:`flask_discord._http.DiscordOAuth2HttpClient` class.

    Parameters
    ----------
    app : Flask
        An instance of your `flask application <http://flask.pocoo.org/docs/1.0/api/#flask.Flask>`_.
    client_id : int, optional
        The client ID of discord application provided. Can be also set to flask config
        with key ``DISCORD_CLIENT_ID``.
    client_secret : str, optional
        The client secret of discord application provided. Can be also set to flask config
        with key ``DISCORD_CLIENT_SECRET``.
    redirect_uri : str, optional
        The default URL to use to redirect user to after authorization. Can be also set to flask config
        with key ``DISCORD_REDIRECT_URI``.
    bot_token : str, optional
        The bot token of the application. This is required when you also need to access bot scope resources
        beyond the normal resources provided by the OAuth. Can be also set to flask config with
        key ``DISCORD_BOT_TOKEN``.
    users_cache : cachetools.LFUCache, optional
        Any dict like mapping to internally cache the authorized users. Preferably an instance of
        cachetools.LFUCache or cachetools.TTLCache. If not specified, default cachetools.LFUCache is used.
        Uses the default max limit for cache if ``DISCORD_USERS_CACHE_MAX_LIMIT`` isn't specified in app config.

    Attributes
    ----------
    client_id : int
        The client ID of discord application provided.
    redirect_uri : str
        The default URL to use to redirect user to after authorization.
    users_cache : cachetools.LFUCache
        A dict like mapping to internally cache the authorized users. Preferably an instance of
        cachetools.LFUCache or cachetools.TTLCache. If not specified, default cachetools.LFUCache is used.
        Uses the default max limit for cache if ``DISCORD_USERS_CACHE_MAX_LIMIT`` isn't specified in app config.

    """

    @staticmethod
    def __save_state(state):
        session["DISCORD_OAUTH2_STATE"] = state

    @staticmethod
    def __get_state():
        return session.get("DISCORD_OAUTH2_STATE", str())

    def create_session(
            self, scope: list = None, *, data: dict = None, prompt: bool = True,
            permissions: typing.Union[types.Permissions, int] = 0, **params
    ):
        """Primary method used to create OAuth2 session and redirect users for
        authorization code grant.

        Parameters
        ----------
        scope : list, optional
            An optional list of valid `Discord OAuth2 Scopes
            <https://discordapp.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes>`_.
        data : dict, optional
            A mapping of your any custom data which you want to access after authorization grant. Use
            `:py:meth:flask_discord.DiscordOAuth2Session.callback` to retrieve this data in your callback view.
        prompt : bool, optional
            Determines if the OAuth2 grant should be explicitly prompted and re-approved. Defaults to True.
            Specify False for implicit grant which will skip the authorization screen and redirect to redirect URI.
        permissions: typing.Union[flask_discord.types.Permissions, int], optional
            An optional parameter determining guild permissions of the bot while adding it to a guild using
            discord OAuth2 with `bot` scope. It is same as generating so called *bot invite link* which redirects
            to your callback endpoint after bot authorization flow. Defaults to 0 or no permissions.
        params : kwargs, optional
            Additional query parameters to append to authorization URL for customized OAuth flow.

        Returns
        -------
        redirect
            Flask redirect to discord authorization servers to complete authorization code grant process.

        """
        scope = scope or request.args.get("scope", str()).split() or configs.DISCORD_OAUTH_DEFAULT_SCOPES

        if not prompt and set(scope) & set(configs.DISCORD_PASSTHROUGH_SCOPES):
            raise ValueError("You should use explicit OAuth grant for passthrough scopes like bot.")

        data = data or dict()
        data["__state_secret_"] = generate_token()

        state = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm="HS256")

        discord_session = self._make_session(scope=scope, state=state)
        authorization_url, state = discord_session.authorization_url(configs.DISCORD_AUTHORIZATION_BASE_URL)

        self.__save_state(state)

        params = params or dict()
        params["prompt"] = "consent" if prompt else "none"
        if "bot" in scope:
            if not isinstance(permissions, (types.Permissions, int)):
                raise ValueError(f"Passed permissions must be an int or discord.Permissions, not {type(permissions)}.")
            if isinstance(permissions, types.Permissions):
                permissions = permissions.value
            params["permissions"] = permissions
            try:
                params["disable_guild_select"] = utils.json_bool(params["disable_guild_select"])
            except KeyError:
                pass
        authorization_url = add_params_to_uri(authorization_url, params)

        return redirect(authorization_url)

    @staticmethod
    def save_authorization_token(token: dict):
        """A staticmethod which saves a dict containing Discord OAuth2 token and other secrets to the user's cookies.
        Meaning by default, it uses client side session handling.

        Override this method if you want to handle the user's session server side. If this method is overridden then,
        you must also override :py:meth:`flask_discord.DiscordOAuth2Session.get_authorization_token`.

        """
        session["DISCORD_OAUTH2_TOKEN"] = token

    @staticmethod
    def get_authorization_token() -> dict:
        """A static method which returns a dict containing Discord OAuth2 token and other secrets which was saved
        previously by `:py:meth:`flask_discord.DiscordOAuth2Session.save_authorization_token` from user's cookies.

        You must override this method if you are implementing server side session handling.

        """
        return session.get("DISCORD_OAUTH2_TOKEN")

    def callback(self):
        """A method which should be always called after completing authorization code grant process
        usually in callback view.
        It fetches the authorization token and saves it flask
        `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_ object.

        """
        error = request.values.get("error")
        if error:
            if error == "access_denied":
                raise exceptions.AccessDenied()
            raise exceptions.HttpException(error)

        state = self.__get_state()
        token = self._fetch_token(state)
        self.save_authorization_token(token)

        return jwt.decode(state, current_app.config["SECRET_KEY"], algorithms="HS256")

    def revoke(self):
        """This method clears current discord token, state and all session data from flask
        `session <http://flask.pocoo.org/docs/1.0/api/#flask.session>`_. Which means user will have
        to go through discord authorization token grant flow again. Also tries to remove the user from internal
        cache if they exist.

        """

        self.users_cache.pop(self.user_id, None)

        for session_key in self.SESSION_KEYS:
            try:
                session.pop(session_key)
            except KeyError:
                pass

    @property
    def authorized(self):
        """A boolean indicating whether current session has authorization token or not."""
        return self._make_session().authorized

    @staticmethod
    def fetch_user() -> models.User:
        """This method returns user object from the internal cache if it exists otherwise makes an API call to do so.

        Returns
        -------
        flask_discord.models.User

        """
        return models.User.get_from_cache() or models.User.fetch_from_api()

    @staticmethod
    def fetch_connections() -> list:
        """This method returns list of user connection objects from internal cache if it exists otherwise
        makes an API call to do so.

        Returns
        -------
        list
            List of :py:class:`flask_discord.models.UserConnection` objects.

        """
        user = models.User.get_from_cache()
        try:
            if user.connections is not None:
                return user.connections
        except AttributeError:
            pass

        return models.UserConnection.fetch_from_api()

    @staticmethod
    def fetch_guilds() -> list:
        """This method returns list of guild objects from internal cache if it exists otherwise makes an API
        call to do so.

        Returns
        -------
        list
            List of :py:class:`flask_discord.models.Guild` objects.

        """
        user = models.User.get_from_cache()
        try:
            if user.guilds is not None:
                return user.guilds
        except AttributeError:
            pass

        return models.Guild.fetch_from_api()
