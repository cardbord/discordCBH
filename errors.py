class CommandError(Exception):
    """
    Base class of all exceptions
    """
class IncorrectType(CommandError):
    """
    The object type was incorrect
    """
class IncorrectFormat(CommandError):
    """
    The object format was incorrect
    """
class HTTPError(CommandError):
    """
    The command request failed
    """
class CommandInvokeError(CommandError):
    """
    The command invoke has failed
    """