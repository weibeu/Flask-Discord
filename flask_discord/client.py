import os

from . import configs
from requests_oauthlib import OAuth2Session

from flask import request, session, redirect, jsonify


class DiscordOAuth2Session(object):

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        if "http://" in self.redirect_uri:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

    @staticmethod
    def __token_updater(token):
        session["oauth2_token"] = token

    def __make_session(self, token=None, state=None, scope=None):
        return OAuth2Session(
            client_id=self.client_id,
            token=token,
            state=state,
            scope=scope,
            redirect_uri=self.redirect_uri,
            auto_refresh_kwargs={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            },
            auto_refresh_url=configs.TOKEN_URL,
            token_updater=self.__token_updater)

    def make_session(self):
        scope = request.args.get("scope", str()).split() or configs.DEFAULT_SCOPES
        discord_session = self.__make_session(scope=scope)
        authorization_url, state = discord_session.authorization_url(configs.AUTHORIZATION_BASE_URL)
        session["oauth2_state"] = state
        return redirect(authorization_url)

    def callback(self):
        if request.values.get("error"):
            return request.values["error"]
        discord = self.__make_session(state=session.get("oauth2_state"))
        token = discord.fetch_token(
            configs.TOKEN_URL,
            client_secret=self.client_secret,
            authorization_response=request.url
        )
        session["oauth2_token"] = token

    def get_json(self):
        discord_session = self.__make_session(token=session.get("oauth2_token"))
        user = discord_session.get(configs.API_BASE_URL + '/users/@me').json()
        guilds = discord_session.get(configs.API_BASE_URL + '/users/@me/guilds').json()
        connections = discord_session.get(configs.API_BASE_URL + '/users/@me/connections').json()
        return jsonify(user=user, guilds=guilds, connections=connections)
