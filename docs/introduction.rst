.. _intro:



Introduction
============

Flask-Discord is an extension for Flask - Python web framework which
makes easy implementation of Discord OAuth2 API. After creating a discord
client object, one can easily request authorization and hence any of the
resources provided by the discord OAuth2 API under the available scope
permissions.

Requirements
------------

- **Flask**
    This is an Flask extension.

- **requests_oauthlib**
    It also requires requests_oauthlib to make OAuth2 sessions with discord.

Installing
----------

You can install Flask-Discord directly from PyPI using PIP and following command
in shell or command prompt: ::

    python3 -m pip install -U Flask-Discord

You can also install the latest development version (**maybe unstable/broken**) by
using following command: ::

    python3 -m pip install -U git+https://github.com/thec0sm0s/Flask-Discord.git@dev


Basic Usage
-----------
Here is a simple example to get users authorization token using OAuth2 and use it
in exchange for fetching user's details and display them on web page.


.. code-block:: python3

    from flask import Flask, redirect, url_for
    from flask_discord import DiscordOAuth2Session, requires_authorization

    app = Flask(__name__)

    app.secret_key = b"random bytes representing flask secret key"

    app.config["DISCORD_CLIENT_ID"] = 490732332240863233    # Discord client ID.
    app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
    app.config["DISCORD_REDIRECT_URI"] = ""                 # Redirect URI.
    app.config["DISCORD_BOT_TOKEN"] = ""                    # Required when you want to use User.add_to_guild method.


    discord = DiscordOAuth2Session(app)


    @app.route("/login/")
    def login():
        return discord.create_session()


    @app.route("/callback/")
    def callback():
        discord.callback()
        return redirect(url_for(".me"))


    @app.route("/me/")
    @requires_authorization
    def me():
        user = discord.fetch_user()
        return f"""
        <html>
            <head>
                <title>{user.name}</title>
            </head>
            <body>
                <img src='{user.avatar_url}' />
            </body>
        </html>"""


    if __name__ == "__main__":
        app.run()