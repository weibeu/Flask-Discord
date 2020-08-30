DISCORD_API_BASE_URL = "https://discord.com/api"

DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + "/oauth2/authorize"
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + "/oauth2/token"


DISCORD_OAUTH_ALL_SCOPES = [
    "bot", "connections", "email", "identify", "guilds", "guilds.join",
    "gdm.join", "messages.read", "rpc", "rpc.api", "rpc.notifications.read", "webhook.incoming",
]

DISCORD_OAUTH_DEFAULT_SCOPES = [
    "identify", "email", "guilds", "guilds.join"
]


DISCORD_PASSTHROUGH_SCOPES = [
    "bot", "webhook.incoming",
]


DISCORD_IMAGE_BASE_URL = "https://cdn.discordapp.com/"
DISCORD_EMBED_BASE_BASE_URL = "https://cdn.discordapp.com/"
DISCORD_IMAGE_FORMAT = "png"
DISCORD_ANIMATED_IMAGE_FORMAT = "gif"
DISCORD_USER_AVATAR_BASE_URL = DISCORD_IMAGE_BASE_URL + "avatars/{user_id}/{avatar_hash}.{format}"
DISCORD_DEFAULT_USER_AVATAR_BASE_URL = DISCORD_EMBED_BASE_BASE_URL + "embed/avatars/{modulo5}.png"
DISCORD_GUILD_ICON_BASE_URL = DISCORD_IMAGE_BASE_URL + "icons/{guild_id}/{icon_hash}.png"

DISCORD_USERS_CACHE_DEFAULT_MAX_LIMIT = 100
