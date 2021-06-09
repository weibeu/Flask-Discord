import enum


@enum.unique
class DiscordOAuth2Scope(enum.Enum):

    READ_ACTIVITIES = "activities.read"
    WRITE_ACTIVITIES = "activities.write"

    READ_APPLICATION_BUILDS = "applications.builds.read"
    UPLOAD_APPLICATION_BUILDS = "applications.builds.upload"

    APPLICATION_COMMANDS = "applications.commands"
    UPDATE_APPLICATION_COMMANDS = "applications.commands.update"
    READ_APPLICATION_ENTITLEMENTS = "applications.entitlements"
    READ_UPDATE_APPLICATION_STORE = "applications.store.update"

    BOT = "bot"
    CONNECTIONS = "connections"
    EMAIL = "email"
    JOIN_GROUP_DM = "gdm.join"
    GUILDS = "guilds"
    JOIN_GUILDS = "guilds.join"
    IDENTIFY = "identify"
    READ_MESSAGES = "messages.read"
    READ_RELATIONSHIPS = "relationships.read"

    RPC = "rpc"
    WRITE_RPC_ACTIVITIES = "rpc.activities.write"
    READ_RPC_NOTIFICATIONS = "rpc.notifications.read"
    READ_RPC_VOICE = "rpc.voice.read"
    WRITE_RPC_VOICE = "rpc.voice.write"

    INCOMING_WEBHOOK = "webhook.incoming"

    def __str__(self):
        return self.value
