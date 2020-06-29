from flask import current_app
from abc import ABCMeta, abstractmethod


class DiscordModelsMeta(ABCMeta):

    ROUTE = str()

    def __init__(cls, name, *args, **kwargs):
        if not cls.ROUTE and name != "DiscordModelsBase":
            raise NotImplementedError(f"ROUTE must be specified in a Discord model: {name}.")
        super().__init__(name, *args, **kwargs)


class DiscordModelsBase(metaclass=DiscordModelsMeta):

    BOT = False
    MANY = False

    @abstractmethod
    def __init__(self, payload):
        self._payload = payload

    @staticmethod
    def _request(*args, **kwargs):
        """A shorthand to :py:func:flask_discord.request`. It uses Flask current_app local proxy to get the
        Flask-Discord client.

        """
        return current_app.discord.request(*args, **kwargs)

    @staticmethod
    def _bot_request(*args, **kwargs):
        """A shorthand to :py:func:flask_discord.bot_request`."""
        return current_app.discord.bot_request(*args, **kwargs)

    @classmethod
    def fetch_from_api(cls):
        """A class method which returns an instance or list of instances of this model by implicitly making an
        API call to Discord.

        Returns
        -------
        cls
            An instance of this model itself.
        [cls, ...]
            List of instances of this model when many of these models exist.

        """
        request_method = cls._bot_request if cls.BOT else cls._request
        payload = request_method(cls.ROUTE)
        if cls.MANY:
            return [cls(_) for _ in payload]
        return cls(payload)

    def to_json(self):
        """A utility method which returns raw payload object as it was received from discord.

        Returns
        -------
        dict
            A dict representing raw payload object received from discord.

        """
        return self._payload
