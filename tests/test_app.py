import os

from quart import Quart, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization


app = Quart(__name__)

app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 490732332240863233
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"

discord = DiscordOAuth2Session(app)


HYPERLINK = '<a href="{}">{}</a>'


@app.route("/")
async def index():
    if not await discord.authorized():
        return f"""
        {HYPERLINK.format(url_for(".login"), "Login")} <br />
        {HYPERLINK.format(url_for(".login_with_data"), "Login with custom data")} <br />
        {HYPERLINK.format(url_for(".invite_bot"), "Invite Bot with permissions 8")} <br />
        {HYPERLINK.format(url_for(".invite_oauth"), "Authorize with oauth and bot invite")}
        """

    return f"""
    {HYPERLINK.format(url_for(".me"), "@ME")}<br />
    {HYPERLINK.format(url_for(".logout"), "Logout")}<br />
    {HYPERLINK.format(url_for(".user_guilds"), "My Servers")}<br />
    {HYPERLINK.format(url_for(".add_to_guild", guild_id=475549041741135881), "Add me to 475549041741135881.")}    
    """


@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/login-data/")
async def login_with_data():
    return await discord.create_session(data=dict(redirect="/me/", coupon="15off", number=15, zero=0, status=False))


@app.route("/invite-bot/")
async def invite_bot():
    return await discord.create_session(
        scope=["bot"], permissions=8, guild_id=464488012328468480, disable_guild_select=True
    )


@app.route("/invite-oauth/")
async def invite_oauth():
    return await discord.create_session(scope=["bot", "identify"], permissions=8)


@app.route("/callback/")
async def callback():
    data = await discord.callback()
    redirect_to = data.get("redirect", "/")
    return redirect(redirect_to)


@app.route("/me/")
async def me():
    user = await discord.fetch_user()
    return f"""
<html>
<head>
<title>{user.name}</title>
</head>
<body><img src='{user.avatar_url or user.default_avatar_url}' />
<p>Is avatar animated: {str(user.is_avatar_animated)}</p>
<a href={url_for("my_connections")}>Connections</a>
<br />
</body>
</html>

"""


@app.route("/me/guilds/")
async def user_guilds():
    guilds = await discord.fetch_guilds()
    return "<br />".join([f"[ADMIN] {g.name}" if g.permissions.administrator else g.name for g in guilds])


@app.route("/add_to/<int:guild_id>/")
async def add_to_guild(guild_id):
    user = await discord.fetch_user()
    return await user.add_to_guild(guild_id)


@app.route("/me/connections/")
async def my_connections():
    user = await discord.fetch_user()
    connections = await discord.fetch_connections()
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
async def logout():
    discord.revoke()
    return redirect(url_for(".index"))


@app.route("/secret/")
@requires_authorization
async def secret():
    return os.urandom(16)


if __name__ == "__main__":
    app.run(debug=True)
