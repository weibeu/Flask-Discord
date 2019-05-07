from . import configs, _http, models

from flask import request, session, redirect


class DiscordOAuth2Session(_http.DiscordOAuth2HttpClient):

    def create_session(self, scope=None):
        scope = scope or request.args.get("scope", str()).split() or configs.DEFAULT_SCOPES
        discord_session = self._make_session(scope=scope)
        authorization_url, state = discord_session.authorization_url(configs.AUTHORIZATION_BASE_URL)
        session["oauth2_state"] = state
        return redirect(authorization_url)

    def callback(self):
        if request.values.get("error"):
            return request.values["error"]
        discord = self._make_session(state=session.get("oauth2_state"))
        token = discord.fetch_token(
            configs.TOKEN_URL,
            client_secret=self.client_secret,
            authorization_response=request.url
        )
        session["oauth2_token"] = token

    def fetch_user(self):
        return models.User(self.get("/users/@me"))

    def fetch_connections(self):
        return models.UserConnection(self.get("/users/@me/connections"))

    def fetch_guilds(self):
        guilds_payload = self.get("/users/@me/guilds")
        return [models.Guild(payload) for payload in guilds_payload]
