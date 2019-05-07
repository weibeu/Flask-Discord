from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, configs

OAUTH2_CLIENT_ID = 490732332240863233
OAUTH2_CLIENT_SECRET = "GjKMenfebgLrOYQ_A_X7ouaWv9IhWdbI"
OAUTH2_REDIRECT_URI = "http://127.0.0.1:5000/callback"


app = Flask(__name__)
app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
discord = DiscordOAuth2Session(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_REDIRECT_URI)


@app.route("/")
def index():
    return discord.make_session(configs.ALL_SCOPES)


@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


@app.route("/me")
def me():
    return discord.get_json()


if __name__ == "__main__":
    app.run(debug=True)
