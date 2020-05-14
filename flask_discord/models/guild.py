from flask import current_app, session
from .base import DiscordModelsBase

from .. import configs


class Guild(DiscordModelsBase):
    """Class representing discord Guild the user is part of.

    Attributes
    ----------
    id : int
        Discord ID of the guild.
    name : str
        Name of the guild.
    icon_hash : str
        Hash of guild's icon.
    is_owner : bool
        Boolean determining if current user is owner of the guild or not.
    permissions_value : int
        An integer representing permissions of current user in the guild.

    """

    MANY = True
    ROUTE = "/users/@me/guilds"

    def __init__(self, payload):
        super().__init__(payload)
        self.id = int(self._payload["id"])
        self.name = self._payload["name"]
        self.icon_hash = self._payload.get("icon")
        self.is_owner = self._payload.get("owner")
        self.permissions_value = self._payload.get("permissions")

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        """A property returning direct URL to the guild's icon. Returns None if guild has no icon set."""
        if not self.icon_hash:
            return
        return configs.DISCORD_GUILD_ICON_BASE_URL.format(guild_id=self.id, icon_hash=self.icon_hash)

    @classmethod
    def fetch_from_api(cls, cache=True):
        """A class method which returns an instance or list of instances of this model by implicitly making an
        API call to Discord. If an instance of :py:class:`flask_discord.User` exists in the users internal cache
        who belongs to these guilds then, the cached property :py:attr:`flask_discord.User.guilds` is updated.

        Parameters
        ----------
        cache : bool
            Determines if the :py:attr:`flask_discord.User.guilds` cache should be updated with the new guilds.

        Returns
        -------
        list[flask_discord.Guild, ...]
            List of instances of :py:class:`flask_discord.Guild` to which this user belogs.

        """
        guilds = super().fetch_from_api()

        if cache:
            user = current_app.discord.users_cache.get(session.get("DISCORD_USER_ID"))
            try:
                user.guilds = {guild.id: guild for guild in guilds}
            except AttributeError:
                pass

        return guilds
