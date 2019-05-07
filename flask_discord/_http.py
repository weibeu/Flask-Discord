import os

from . import configs

from flask import session, jsonify
from requests_oauthlib import OAuth2Session


class DiscordOAuth2HttpClient(object):

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if "http://" in self.redirect_uri:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

    @staticmethod
    def _token_updater(token):
        session["oauth2_token"] = token

    def _make_session(self, token=None, state=None, scope=None):
        return OAuth2Session(
            client_id=self.client_id,
            token=token or session.get("oauth2_token"),
            state=state,
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            },
            auto_refresh_url=configs.TOKEN_URL,
            token_updater=self._token_updater)

    def get(self, route):
        return self._make_session().get(configs.API_BASE_URL + route).json()

    def get_json(self):
        discord_session = self._make_session(token=session.get("oauth2_token"))
        user = discord_session.get(configs.API_BASE_URL + '/users/@me').json()
        guilds = discord_session.get(configs.API_BASE_URL + '/users/@me/guilds').json()
        connections = discord_session.get(configs.API_BASE_URL + '/users/@me/connections').json()
        return jsonify(user=user, guilds=guilds, connections=connections)
