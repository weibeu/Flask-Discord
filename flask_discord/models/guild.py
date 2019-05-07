from .. import configs


class Guild(object):

    def __init__(self, payload):
        self._payload = payload
        self.id = self._payload["id"]
        self.name = self._payload["name"]
        self.icon_hash = self._payload.get("icon")
        self.is_owner = self._payload.get["owner"]
        self.permissions_value = self._payload.get("permissions")

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        return configs.GUILD_ICON_BASE_URL.format(guild_id=self.id, icon_hash=self.icon_hash)
