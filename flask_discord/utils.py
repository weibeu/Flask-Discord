"""Few utility functions and decorators."""
import functools

from . import exceptions
from flask import current_app


# Decorators.

def requires_authorization(view):
    """A decorator for flask views which raises exception :py:class:`flask_discord.Unauthorized` if the user
    is not authorized from Discord OAuth2.

    """

    # TODO: Add support to validate scopes.

    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not current_app.discord.authorized:
            raise exceptions.Unauthorized
        return view(*args, **kwargs)

    return wrapper
