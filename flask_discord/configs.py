from .scopes import DiscordOAuth2Scope


DISCORD_API_VERSION = 9


DISCORD_API_BASE_URL = "https://discord.com/api/v{version}"
DISCORD_API_BASE_URL = DISCORD_API_BASE_URL.format(version=DISCORD_API_VERSION)

DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + "/oauth2/authorize"
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + "/oauth2/token"


DISCORD_OAUTH_DEFAULT_SCOPES = [
    DiscordOAuth2Scope.IDENTIFY, DiscordOAuth2Scope.EMAIL,
    DiscordOAuth2Scope.GUILDS, DiscordOAuth2Scope.JOIN_GUILDS,
]
DISCORD_PASSTHROUGH_SCOPES = [
    DiscordOAuth2Scope.APPLICATION_COMMANDS,
    DiscordOAuth2Scope.BOT, DiscordOAuth2Scope.INCOMING_WEBHOOK,
]


DISCORD_IMAGE_BASE_URL = "https://cdn.discordapp.com/"
DISCORD_EMBED_BASE_BASE_URL = "https://cdn.discordapp.com/"
DISCORD_IMAGE_FORMAT = "png"
DISCORD_ANIMATED_IMAGE_FORMAT = "gif"
DISCORD_USER_AVATAR_BASE_URL = DISCORD_IMAGE_BASE_URL + "avatars/{user_id}/{avatar_hash}.{format}"
DISCORD_DEFAULT_USER_AVATAR_BASE_URL = DISCORD_EMBED_BASE_BASE_URL + "embed/avatars/{modulo5}.png"
DISCORD_GUILD_ICON_BASE_URL = DISCORD_IMAGE_BASE_URL + "icons/{guild_id}/{icon_hash}.png"

DISCORD_USERS_CACHE_DEFAULT_MAX_LIMIT = 100
