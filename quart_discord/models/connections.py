from quart import current_app

from .base import DiscordModelsBase
from .integration import Integration


class UserConnection(DiscordModelsBase):
    """Class representing connections in discord account of the user.

    Attributes
    ----------
    id : str
        ID of the connection account.
    name : str
        The username of the connection account.
    type : str
        The service of connection (twitch, youtube).
    revoked : bool
        A boolean representing whether the connection is revoked.
    integrations : list
        A list of server Integration objects.
    verified : bool
        A boolean representing whether the connection is verified.
    friend_sync : bool
        A boolean representing whether friend sync is enabled for this connection.
    show_activity : bool
        A boolean representing whether activities related to this connection will
        be shown in presence updates.
    visibility : int
        An integer representing
        `visibility <https://discordapp.com/developers/docs/resources/user#user-object-visibility-types>`_
        of this connection.

    """

    MANY = True
    ROUTE = "/users/@me/connections"

    def __init__(self, payload):
        super().__init__(payload)
        self.id = self._payload["id"]
        self.name = self._payload.get("name")
        self.type = self._payload.get("type")
        self.revoked = self._payload.get("revoked")
        self.integrations = self.__get_integrations()
        self.verified = self._payload.get("verified")
        self.friend_sync = self._payload.get("friend_sync")
        self.show_activity = self._payload.get("show_activity")
        self.visibility = self._payload.get("visibility")

    def __get_integrations(self):
        return [Integration(payload) for payload in self._payload.get("integrations", list())]

    @property
    def is_visible(self):
        """A property returning bool if this integration is visible to everyone."""
        return bool(self.visibility)

    @classmethod
    async def fetch_from_api(cls, cache=True):
        """A class method which returns an instance or list of instances of this model by implicitly making an
        API call to Discord. If an instance of :py:class:`quart_discord.User` exists in the users internal cache
        who are attached to these connections then, the cached property :py:attr:`quart_discord.User.connections`
        is updated.

        Parameters
        ----------
        cache : bool
            Determines if the :py:attr:`quart_discord.User.guilds` cache should be updated with the new guilds.

        Returns
        -------
        list[quart_discord.UserConnection, ...]
            List of instances of :py:class:`quart_discord.UserConnection` to which this user belongs.

        """
        connections = await super().fetch_from_api()

        if cache:
            user = current_app.discord.users_cache.get(current_app.discord.user_id)
            try:
                user.connections = connections
            except AttributeError:
                pass

        return connections
