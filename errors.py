from enum import IntEnum

class DiscordException(Exception):
    """
    Base class of all non-exit exceptions
    """
class IncorrectType(DiscordException):
    """
    The object type was incorrect
    """
class IncorrectFormat(DiscordException):
    """
    The object format was incorrect
    """
class HTTPException(DiscordException):
    """
    The HTTP request failed
    """
    class Forbidden(DiscordException):
        """
        The process is forbidden
        """
    class NotFound(DiscordException):
        """
        The data/location could not be found
        """
    class RateLimited(DiscordException):
        """
        Discord has limited the rate of requests that can be sent by the client 
        """
class ClientException(DiscordException):
    """
    An exception occured within the client
    """
class CommandInvokeException(ClientException):
    """
    The command invoke has failed
    """
class HTTPResponseException(IntEnum):
    not_found = 404
    unauthorized = 401
    forbidden = 403
    bad_request = 400
    method_not_allowed = 405
    not_acceptable = 406
    rate_limited = 429

    internal_server_error = 500
    bad_gateway = 502
    service_unavailable = 503
    gateway_timeout = 504


class CommandCreationException(ClientException):
    """
    The command could not be registered/created successfully
    """
class DiscordError(RuntimeError):
    """
    Base class of all exit-based exceptions
    (shouldn't be needed unless in very specific instances)
    """
class ClientError(DiscordError):
    """
    A fatal error occured within the client
    """
class CommandCreationError(DiscordError):
    """
    A fatal error occured within command creation/registration
    """