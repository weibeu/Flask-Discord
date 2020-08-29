API Reference
=============

This sections has reference to all of the available classes, their
attributes and available methods.


Discord OAuth2 Client
---------------------

.. autoclass:: flask_discord.oauth2.DiscordOAuth2Session
    :members:
    :inherited-members:

.. autoclass:: flask_discord.oauth2._http.DiscordOAuth2HttpClient
    :members:
    :inherited-members:


Models
------

.. autoclass:: flask_discord.oauth2.models.Guild
    :members:
    :inherited-members:

.. autoclass:: flask_discord.oauth2.models.User
    :members:
    :inherited-members:

.. autoclass:: flask_discord.oauth2.models.Bot
    :members:
    :inherited-members:

.. autoclass:: flask_discord.oauth2.models.Integration
    :members:
    :inherited-members:

.. autoclass:: flask_discord.oauth2.models.UserConnection
    :members:
    :inherited-members:


Utilities
---------

.. autodecorator:: flask_discord.requires_authorization


Exceptions
----------

.. autoclass:: flask_discord.HttpException
    :members:

.. autoclass:: flask_discord.RateLimited
    :members:

.. autoclass:: flask_discord.Unauthorized
    :members:

.. autoclass:: flask_discord.AccessDenied
    :members:
