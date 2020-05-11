from flask import current_app
from abc import ABC


class DiscordModelsBase(ABC):

    @staticmethod
    def _request(*args, **kwargs):
        """A shorthand to :py:func:flask_discord.request`. It uses Flask current_app local proxy to get the
        Flask-Discord client.

        """
        return current_app.discord.request(*args, **kwargs)

    def to_json(self):
        """A utility method which returns raw payload object as it was received from discord.

        Returns
        -------
        dict
            A dict representing raw payload object received from discord.

        """
        return self._payload
