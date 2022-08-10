import enum


@enum.unique
class DiscordOAuth2Scope(enum.Enum):
    """These are a `list of all the OAuth2 scopes that Discord supports
    <https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes>`_. Some scopes require
    approval from Discord to use. Requesting them from a user without approval from Discord may cause
    undocumented/error behavior in the OAuth2 flow.

    Attributes
    ----------
    READ_ACTIVITIES
        Allows your app to fetch data from a user's "Now Playing/Recently Played" list - requires Discord approval.
    WRITE_ACTIVITIES
        Allows your app to update a user's activity - requires Discord approval
        (NOT REQUIRED FOR `GAMESDK ACTIVITY MANAGER <https://discord.com/developers/docs/game-sdk/activities>`_).
    READ_APPLICATION_BUILDS
        Allows your app to read build data for a user's applications.
    UPLOAD_APPLICATION_BUILDS
        Allows your app to upload/update builds for a user's applications - requires Discord approval.
    APPLICATION_COMMANDS
        Allows your app to use `Slash Commands <https://discord.com/developers/docs/interactions/slash-commands>`_
        in a guild.
    UPDATE_APPLICATION_COMMANDS
        Allows your app to update its
        `Slash Commands <https://discord.com/developers/docs/interactions/slash-commands>`_
        via this bearer token -
        `client credentials grant only <https://discord.com/developers/docs/topics/oauth2#client-credentials-grant>`_.
    UPDATE_APPLICATION_COMMANDS_PERMISSIONS
        Allows your app to update
        `permissions for its commands
        <https://discord.com/developers/docs/interactions/application-commands#permissions>`_.
        in a guild a user has permissions to.
    READ_APPLICATION_ENTITLEMENTS
        Allows your app to read entitlements for a user's applications.
    READ_UPDATE_APPLICATION_STORE
        Allows your app to read and update store data (SKUs, store listings, achievements, etc.)
        for a user's applications.
    BOT
        For oauth2 bots, this puts the bot in the user's selected guild by default.
    CONNECTIONS
        Allows `/users/@me/connections <https://discord.com/developers/docs/resources/user#get-user-connections>`_
        to return linked third-party accounts.
    READ_DM_CHANNELS
        Allows your app to see information about the user's DMs and group DMs - requires Discord approval.
    EMAIL
        Enables `/users/@me <https://discord.com/developers/docs/resources/user#get-current-user>`_ to return an email.
    JOIN_GROUP_DM
        Allows your app to
        `join users to a group dm <https://discord.com/developers/docs/resources/channel#group-dm-add-recipient>`_.
    GUILDS
        Allows `/users/@me/guilds <https://discord.com/developers/docs/resources/user#get-current-user-guilds>`_
        to return basic information about all of a user's guilds.
    JOIN_GUILDS
        Allows
        `/guilds/{guild.id}/members/{user.id} <https://discord.com/developers/docs/resources/guild#add-guild-member>`_
        to be used for joining users to a guild.
    READ_GUILD_MEMBERS
        Allows
        `/users/@me/guilds/{guild.id}/member
        <https://discord.com/developers/docs/resources/user#get-current-user-guild-member>`_ to return a user's
        member information in a guild.
    IDENTIFY
        Allows `/users/@me <https://discord.com/developers/docs/resources/user#get-current-user>`_ without email.
    READ_MESSAGES
        For local rpc server api access, this allows you to read messages from all client channels
        (otherwise restricted to channels/guilds your app creates).
    READ_RELATIONSHIPS
        Allows your app to know a user's friends and implicit relationships - requires Discord approval.
    RPC
        For local rpc server access, this allows you to control a user's local Discord client
        - requires Discord approval.
    WRITE_RPC_ACTIVITIES
        For local rpc server access, this allows you to update a user's activity - requires Discord approval.
    READ_RPC_NOTIFICATIONS
        For local rpc server access, this allows you to receive notifications pushed out to the user
        - requires Discord approval.
    READ_RPC_VOICE
        For local rpc server access, this allows you to read a user's voice settings and listen for voice events
        - requires Discord approval.
    WRITE_RPC_VOICE
        For local rpc server access, this allows you to update a user's voice settings - requires Discord approval.
    VOICE
        Allows your app to connect to voice on user's behalf and see all the voice members - requires Discord approval.
    INCOMING_WEBHOOK
        This generates a webhook that is returned in the oauth token response for authorization code grants.

    """

    READ_ACTIVITIES = "activities.read"
    WRITE_ACTIVITIES = "activities.write"

    READ_APPLICATION_BUILDS = "applications.builds.read"
    UPLOAD_APPLICATION_BUILDS = "applications.builds.upload"

    APPLICATION_COMMANDS = "applications.commands"
    UPDATE_APPLICATION_COMMANDS = "applications.commands.update"
    UPDATE_APPLICATION_COMMANDS_PERMISSIONS = "applications.commands.permissions.update"
    READ_APPLICATION_ENTITLEMENTS = "applications.entitlements"
    READ_UPDATE_APPLICATION_STORE = "applications.store.update"

    BOT = "bot"
    CONNECTIONS = "connections"
    READ_DM_CHANNELS = "dm_channels.read"
    EMAIL = "email"
    JOIN_GROUP_DM = "gdm.join"
    GUILDS = "guilds"
    JOIN_GUILDS = "guilds.join"
    READ_GUILD_MEMBERS = "guilds.members.read"
    IDENTIFY = "identify"
    READ_MESSAGES = "messages.read"
    READ_RELATIONSHIPS = "relationships.read"

    RPC = "rpc"
    WRITE_RPC_ACTIVITIES = "rpc.activities.write"
    READ_RPC_NOTIFICATIONS = "rpc.notifications.read"
    READ_RPC_VOICE = "rpc.voice.read"
    WRITE_RPC_VOICE = "rpc.voice.write"

    VOICE = "voice"
    INCOMING_WEBHOOK = "webhook.incoming"

    def __str__(self):
        return self.value
