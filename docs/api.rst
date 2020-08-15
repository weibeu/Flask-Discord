API Reference
=============

This sections has reference to all of the available classes, their
attributes and available methods.


Discord OAuth2 Client
---------------------

.. autoclass:: quart_discord.DiscordOAuth2Session
    :members:
    :inherited-members:

.. autoclass:: quart_discord._http.DiscordOAuth2HttpClient
    :members:
    :inherited-members:


Models
------

.. autoclass:: quart_discord.models.Guild
    :members:
    :inherited-members:

.. autoclass:: quart_discord.models.User
    :members:
    :inherited-members:

.. autoclass:: quart_discord.models.Bot
    :members:
    :inherited-members:

.. autoclass:: quart_discord.models.Integration
    :members:
    :inherited-members:

.. autoclass:: quart_discord.models.UserConnection
    :members:
    :inherited-members:


Utilities
---------

.. autodecorator:: quart_discord.requires_authorization


Exceptions
----------

.. autoclass:: quart_discord.HttpException
    :members:

.. autoclass:: quart_discord.RateLimited
    :members:

.. autoclass:: quart_discord.Unauthorized
    :members:

.. autoclass:: quart_discord.AccessDenied
    :members:
