from .base import DiscordModelsBase

from .. import configs


class User(DiscordModelsBase):
    """Class representing Discord User.

    Attributes
    ----------
    id : int
        The discord ID of the user.
    username : str
        The discord username of the user.
    discriminator : int
        4 - digits discord tag of the user.
    avatar_hash : str
        Hash of users avatar.
    bot : bool
        A boolean representing whether the user belongs to an OAuth2 application.
    mfa_enabled : bool
        A boolean representing whether the user has two factor enabled on their account.
    locale : str
        The user's chosen language option.
    verified : bool
        A boolean representing whether the email on this account has been verified.
    email : str
        User's email ID.
    flags : int
        An integer representing the
        `user flags <https://discordapp.com/developers/docs/resources/user#user-object-user-flags>`_.
    premium_type : int
        An integer representing the
        `type of nitro subscription <https://discordapp.com/developers/docs/resources/user#user-object-premium-types>`_.

    """

    def __init__(self, payload):
        self._payload = payload
        self.id = int(self._payload["id"])
        self.username = self._payload["username"]
        self.discriminator = int(self._payload["discriminator"])
        self.avatar_hash = self._payload.get("avatar", self.discriminator)
        self.bot = self._payload.get("bot", False)
        self.mfa_enabled = self._payload.get("mfa_enabled")
        self.locale = self._payload.get("locale")
        self.verified = self._payload.get("verified")
        self.email = self._payload.get("email")
        self.flags = self._payload.get("flags")
        self.premium_type = self._payload.get("premium_type")

    def __str__(self):
        return f"{self.name}#{self.discriminator}"

    @property
    def name(self):
        """An alias to the username attribute."""
        return self.username

    @property
    def avatar_url(self):
        """A property returning direct URL to user's avatar."""
        return configs.USER_AVATAR_BASE_URL.format(user_id=self.id, avatar_hash=self.avatar_hash)

    @property
    def is_avatar_animated(self):
        """A boolean representing if avatar of user is animated. Meaning user has GIF avatar."""
        return self.avatar_hash.startswith("a_")


class Bot(User):
    """Class representing the client user itself.

    """

    pass
