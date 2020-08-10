"""Few utility functions and decorators."""

import functools

from . import exceptions
from flask import current_app


class JSONBool(object):

    def __init__(self, value):
        self.value = bool(value)

    def __bool__(self):
        return self.value

    def __str__(self):
        return "true" if self else "false"

    @classmethod
    def from_string(cls, value):
        if value.lower() == "true":
            return cls(True)
        if value.lower() == "false":
            return cls(False)
        raise ValueError


def json_bool(value):
    if isinstance(value, str):
        return str(JSONBool.from_string(value))
    return str(JSONBool(value))


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
