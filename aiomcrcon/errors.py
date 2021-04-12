class RCONConnectionError(Exception):
    """Raised when the Client.connect() method fails."""

    def __init__(self, msg: str = None, error: Exception = None):
        super().__init__(msg)

        self.message = msg
        self.error = error


class ClientNotConnectedError(Exception):
    """Raised when an IO method is used when the Client isn't connected."""

    def __str__(self):
        return "The client isn't connected. (Looks like you forgot to call the connect() coroutine!)"


class IncorrectPasswordError(Exception):
    """Raised when the RCON authentication / password is incorrect."""

    def __str__(self):
        return "The password provided to the client was incorect according to the server."
