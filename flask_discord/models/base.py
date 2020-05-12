from flask import current_app
from abc import ABCMeta, abstractmethod


class DiscordModelsMeta(ABCMeta):

    ROUTE = str()

    def __init__(cls, name, *args, **kwargs):
        if not cls.ROUTE and name != "DiscordModelsBase":
            raise NotImplementedError(f"ROUTE must be specified in a Discord model: {name}.")
        super().__init__(name, *args, **kwargs)


class DiscordModelsBase(metaclass=DiscordModelsMeta):

    @abstractmethod
    def __init__(self, payload):
        self._payload = payload

    @staticmethod
    def _request(*args, **kwargs):
        """A shorthand to :py:func:flask_discord.request`. It uses Flask current_app local proxy to get the
        Flask-Discord client.

        """
        return current_app.discord.request(*args, **kwargs)

    @classmethod
    def fetch_from_api(cls):
        """A class method which returns instance of this model by implicitly making an API call to Discord."""
        return cls(cls._request(cls.ROUTE))

    def to_json(self):
        """A utility method which returns raw payload object as it was received from discord.

        Returns
        -------
        dict
            A dict representing raw payload object received from discord.

        """
        return self._payload
