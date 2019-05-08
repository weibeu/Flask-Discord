from .user import User


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
    user : User
        Object representing user of this integration.
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
        self.user = User(self._payload.get("user", dict()))
        self.account = self._payload.get("account")
        self.synced_at = self._payload.get("synced_at")


class UserConnection(object):
    """Class representing connections in discord account of the user.

    Attributes
    ----------
    id : int
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

    def __init__(self, payload):
        self._payload = payload
        self.id = int(self._payload.get("id", 0))
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
