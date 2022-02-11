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


Types
-----

.. autoclass:: flask_discord.types.Permissions
    :members:
    :inherited-members:


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

Configuration Values
--------------------

Flask Discord attempts to fetch expected configuration keys from the config of initialized flask app.

.. py:data:: DISCORD_CLIENT_ID

Client ID of your Discord application. Can be retrieved from your Discord developers dashboard. This can be also passed as ``client_id`` to :py:class:`flask_discord.DiscordOAuth2Session` constructor.

.. py:data:: DISCORD_CLIENT_SECRET

The client secret of your Discord application. Can also be retrieved from your Discord developers dashboard. This can be also passed as ``client_secret`` to :py:class:`flask_discord.DiscordOAuth2Session` constructor.

.. py:data:: DISCORD_REDIRECT_URI

The default URL to use to redirect user to after authorization. This should be exactly same as what you've specified in Redirects in Discord developers dashboard OAuth2 section. This can be also passed as ``redirect_uri`` to :py:class:`flask_discord.DiscordOAuth2Session` constructor.

.. py:data:: DISCORD_BOT_TOKEN

The bot token of the application. This is required when you also need to access bot scope resources beyond the normal resources provided by the OAuth. This can be also passed as ``bot_token`` to :py:class:`flask_discord.DiscordOAuth2Session` constructor.

.. py:data:: DISCORD_USERS_CACHE_MAX_LIMIT

Flask Discord has an internal caching layer to prevent rate limits. This specifies the max number of users to be cached using the default Last Frequently Used cache implementation. Defaults to ``100``.
