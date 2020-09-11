import os

from flask import Flask
from flask_discord import DiscordOAuth2Session


discord = DiscordOAuth2Session(client_id=490732332240863233)


def get_app():
    app = Flask(__name__)

    app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # !! Only in development environment.

    # app.config["DISCORD_CLIENT_ID"] = 490732332240863233
    app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
    app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
    app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"

    discord.init_app(app)

    return app
