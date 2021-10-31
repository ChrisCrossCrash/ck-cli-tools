class CkError(Exception):
    """Base class for exceptions in this module"""
    pass


class ChatIdMissingError(CkError):
    """Raised when trying to use a `Bot` method that requires `Bot.chat_id` when `Bot.chat_id` is None."""
    pass
