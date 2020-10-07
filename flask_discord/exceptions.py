class HttpException(Exception):
    """Base Exception class representing a HTTP exception."""


class RateLimited(HttpException):
    """A HTTP Exception raised when the application is being rate limited.
    It provides the ``response`` attribute which can be used to get more details of the actual response from
    the Discord API with few more shorthands to ``response.json()``.

    Attributes
    ----------
    json : dict
        The actual JSON data received. Shorthand to ``response.json()``.
    message : str
        A message saying you are being rate limited.
    retry_after : int
        The number of milliseconds to wait before submitting another request.
    is_global : bool
        A value indicating if you are being globally rate limited or not

    """

    def __init__(self, json, headers):
        self.json = json
        self.headers = headers
        self.message = self.json["message"]
        self.is_global = self.json["global"]
        self.retry_after = self.json["retry_after"]
        super().__init__(self.message)


class Unauthorized(HttpException):
    """A HTTP Exception raised when user is not authorized."""


class AccessDenied(HttpException):
    """Exception raised when user cancels OAuth authorization grant."""
