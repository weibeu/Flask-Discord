from .. import configs


class User(object):

    def __init__(self, payload):
        self._payload = payload
        self.id = self._payload["id"]
        self.username = self._payload["username"]
        self.discriminator = self._payload["discriminator"]
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
        return self.username

    @property
    def avatar_url(self):
        return configs.USER_AVATAR_BASE_URL.format(user_id=self.id, avatar_hash=self.avatar_hash)

    @property
    def is_avatar_animated(self):
        return self.avatar_hash.startswith("a_")

    def to_json(self):
        return self._payload


class Bot(User):

    pass
