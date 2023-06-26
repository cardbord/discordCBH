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