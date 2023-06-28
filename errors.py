from enum import IntEnum

class DiscordException(Exception):
    """
    Base class of all exceptions
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

class Forbidden(HTTPException):
    """
    The process is forbidden
    """
class CommandCreationException(ClientException):
    """
    The command could not be registered/created successfully
    """