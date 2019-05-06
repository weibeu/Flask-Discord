API_BASE_URL = "https://discordapp.com/api"

AUTHORIZATION_BASE_URL = API_BASE_URL + "/oauth2/authorize"
TOKEN_URL = API_BASE_URL + "/oauth2/token"


ALL_SCOPES = [
    "bot", "connections", "email", "identify", "guilds", "guilds.join",
    "gdm.join", "messages.read", "rpc", "rpc.api", "rpc.notifications.read", "webhook.incoming",
]

DEFAULT_SCOPES = [
    "bot", "identify", "email", "guilds", "guilds.join"
]
