API Reference
=============

This sections has reference to all of the available classes, their
attributes and available methods.


Discord OAuth2 Client
---------------------

.. autoclass:: flask_discord.DiscordOAuth2Session
    :members:
    :inherited-members:

.. autoclass:: flask_discord._http.DiscordOAuth2HttpClient
    :members:
    :inherited-members:


Models
------

.. autoclass:: flask_discord.models.Guild
    :members:
    :inherited-members:

.. autoclass:: flask_discord.models.User
    :members:
    :inherited-members:

.. autoclass:: flask_discord.models.Bot
    :members:
    :inherited-members:

.. autoclass:: flask_discord.models.Integration
    :members:
    :inherited-members:

.. autoclass:: flask_discord.models.UserConnection
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

Config
----------

| ``DISCORD_CLIENT_ID`` Discord client ID is the id for you Discord app that will be used for the authentication
|
| ``DISCORD_CLIENT_SECRET`` Discord client secret is the secret found on the developer portal
|
| ``DISCORD_REDIRECT_URI`` URL to your callback endpoint the redirect url when a user has been authenticated
|
| ``DISCORD_BOT_TOKEN`` Required to access BOT resources; It is the token from a pot account connected to the application in the developer portal
|
| ``DISCORD_USERS_CACHE_MAX_LIMIT`` ??
