from . import configs
from requests_oauthlib import OAuth2Session

from flask import request, session, redirect



class DiscordOAuth2Session(object):

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

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
        scope = request.args.get("scope", configs.DEFAULT_SCOPES).split()
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
