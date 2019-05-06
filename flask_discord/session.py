from . import configs
from requests_oauthlib import OAuth2Session

from flask import current_app, request, session, sessions, redirect


class Session(dict, sessions.SessionMixin):

    def to_discord(self, scope=str()):
        scope = (request.args.get("scope") or scope).split()
        discord_session = OAuth2Session()

    def __init__(self, client_id, client_secret, redirect_uri, token_updater=None):
        auto_refresh_kwargs = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        super().__init__(
            client_id=client_id, redirect_uri=redirect_uri,
            auto_refresh_kwargs=auto_refresh_kwargs,
            auto_refresh_url=configs.TOKEN_URL, token_updater=token_updater
        )

    def create_session(self, scope=None):
        self.scope = scope
        authorization_url, state = self.authorization_url(configs.AUTHORIZATION_BASE_URL)
        session["oauth2_state"] = state
        return redirect(authorization_url)


class MySessionInterface(sessions.SessionInterface):

    def __init__(self, client_id, client_secret, redirect_uri, token_updater=None):
        pass

    def open_session(self, app, request):
        pass

    def save_session(self, app, session, response):



class DiscordOAuth2Session(object):

    def __init__(self, app):
        app.session_interface = Session()
