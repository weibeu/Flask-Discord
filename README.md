# Flask-Discord
![PyPI](https://img.shields.io/pypi/v/Flask-Discord?style=for-the-badge) ![Read the Docs](https://img.shields.io/readthedocs/flask-discord?style=for-the-badge) [![Discord](https://img.shields.io/discord/690878977920729177?label=Discord%20Community&logo=Discord&style=for-the-badge)](https://discord.gg/7CrQEyP)

Discord OAuth2 extension for Flask.


### Installation
To install current latest release you can use following command:
```sh
python3 -m pip install Flask-Discord
```


### Basic Example
```python
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session

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
```


### Requirements
* Flask
* requests_oauthlib


### Documentation
Head over to [documentation] for full API reference. 


[documentation]: https://flask-discord.readthedocs.io/en/latest/
