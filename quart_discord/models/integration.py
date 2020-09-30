class Integration(object):
    """"Class representing discord server integrations.

    Attributes
    ----------
    id : int
        Integration ID.
    name : str
        Name of integration.
    type : str
        Integration type (twitch, youtube, etc).
    enabled : bool
        A boolean representing if this integration is enabled.
    syncing : bool
        A boolean representing if this integration is syncing.
    role_id : int
        ID that this integration uses for subscribers.
    expire_behaviour : int
        An integer representing the behaviour of expiring subscribers.
    expire_grace_period : int
        An integer representing the grace period before expiring subscribers.
    account : dict
        A dictionary representing raw
        `account <https://discordapp.com/developers/docs/resources/guild#integration-account-object>`_ object.
    synced_at : ISO8601 timestamp
        Representing when this integration was last synced.

    """

    def __init__(self, payload):
        self._payload = payload
        self.id = int(self._payload.get("id", 0))
        self.name = self._payload.get("name")
        self.type = self._payload.get("type")
        self.enabled = self._payload.get("enabled")
        self.syncing = self._payload.get("syncing")
        self.role_id = int(self._payload.get("role_id", 0))
        self.expire_behaviour = self._payload.get("expire_behaviour")
        self.expire_grace_period = self._payload.get("expire_grace_period")
        # self.user = User(self._payload.get("user", dict()))
        self.account = self._payload.get("account")
        self.synced_at = self._payload.get("synced_at")
