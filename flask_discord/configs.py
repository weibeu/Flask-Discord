API_BASE_URL = "https://discordapp.com/api"

AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"


ALL_SCOPES = [
    "bot", "connections", "email", "identify", "guilds", "guilds.join",
    "gdm.join", "messages.read", "rpc", "rpc.api", "rpc.notifications.read", "webhook.incoming",
]

DEFAULT_SCOPES = [
    "identify", "email", "guilds", "guilds.join"
]


IMAGE_BASE_URL = "https://cdn.discordapp.com/"

USER_AVATAR_BASE_URL = IMAGE_BASE_URL + "avatars/{user_id}/{avatar_hash}.png"
GUILD_ICON_BASE_URL = IMAGE_BASE_URL + "icons/{guild_id}/{icon_hash}.png"
