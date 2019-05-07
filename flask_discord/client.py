from . import configs, _http

from flask import request, session, redirect


class DiscordOAuth2Session(_http.DiscordOAuth2HttpClient):

    def make_session(self):
        scope = request.args.get("scope", str()).split() or configs.DEFAULT_SCOPES
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
