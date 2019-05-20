class HttpException(Exception):
    """Base Exception class representing a HTTP exception."""


class Unauthorized(HttpException):
    """A HTTP Exception raised when user is not authorized."""
