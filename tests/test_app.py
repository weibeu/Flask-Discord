import os

from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session


app = Flask(__name__)

app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"

app.config["DISCORD_CLIENT_ID"] = 490732332240863233
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"

discord = DiscordOAuth2Session(app)


@app.route("/")
def index():
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
<body><img src='{user.avatar_url}' />
<a href={url_for("my_connections")}>Connections</a>
</body>
</html>

"""


@app.route("/me/connections/")
def my_connections():
    user = discord.fetch_user()
    connections = discord.fetch_connections()
    return f"""
<html>
<head>
<title>{user.name}</title>
</head>
<body>
{str([f"{connection.name} - {connection.type}" for connection in connections])}
</body>
</html>

"""


@app.route("/logout/")
def logout():
    discord.revoke()
    return redirect(url_for(".index"))


if __name__ == "__main__":
    app.run(debug=True)
