from .user import User


class Integration(object):

    def __init__(self, payload):
        self._payload = payload
        self.id = self._payload.get("id")
        self.name = self._payload.get("name")
        self.type = self._payload.get("type")
        self.enabled = self._payload.get("enabled")
        self.syncing = self._payload.get("syncing")
        self.role_id = self._payload.get("role_id")
        self.expire_behaviour = self._payload.get("expire_behaviour")
        self.expire_grace_period = self._payload.get("expire_grace_period")
        self.user = User(self._payload.get("user", dict()))
        self.account = self._payload.get("account")
        self.synced_at = self._payload.get("synced_at")


class UserConnection(object):

    def __init__(self, payload):
        self._payload = payload
        self.id = self._payload.get("id")
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
        return bool(self.visibility)
