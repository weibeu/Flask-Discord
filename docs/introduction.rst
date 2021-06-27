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

- **cachetools**
    Flask Discord supports caching discord objects to boost the performance when page loads.

- **discord.py**
    Makes use of discord.py for re-using many Discord models.

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

    import os

    from flask import Flask, redirect, url_for
    from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

    app = Flask(__name__)

    app.secret_key = b"random bytes representing flask secret key"
    # OAuth2 must make use of HTTPS in production environment.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

    app.config["DISCORD_CLIENT_ID"] = 490732332240863233    # Discord client ID.
    app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
    app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
    app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.


    discord = DiscordOAuth2Session(app)

    def welcome_user(user):
        dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
        return discord.bot_request(
            f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
        )

    @app.route("/login/")
    def login():
        return discord.create_session()


    @app.route("/callback/")
    def callback():
        discord.callback()
        user = discord.fetch_user()
        welcome_user(user)
        return redirect(url_for(".me"))


    @app.errorhandler(Unauthorized)
    def redirect_unauthorized(e):
        return redirect(url_for("login"))


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

**Lazy initialization with flask factory pattern**

.. code-block:: python3

    from flask_discord import DiscordOAuth2Session

    discord = DiscordOAuth2Session()

    def get_app():
        app = Flask(__name__)

        app.secret_key = b"random bytes representing flask secret key"
        # OAuth2 must make use of HTTPS in production environment.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.
        app.config["DISCORD_CLIENT_ID"] = 490732332240863233    # Discord client ID.
        app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
        app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
        app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.

        discord.init_app(app)

        return app
