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

    def __init__(self, payload):
        self._payload = payload
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
        return configs.GUILD_ICON_BASE_URL.format(guild_id=self.id, icon_hash=self.icon_hash)
