import typing as t


class RCONConnectionError(Exception):
    """Raised when the Client.connect() method fails."""

    def __init__(self, msg: t.Optional[str] = None, error: t.Optional[Exception] = None) -> None:
        super().__init__(msg)

        self.message = msg
        self.error = error


class ClientNotConnectedError(Exception):
    """Raised when an IO method is used when the Client isn't connected."""

    def __init__(self) -> None:
        super().__init__(
            "The client isn't connected. (Looks like you forgot to call the connect() coroutine!)"
        )


class IncorrectPasswordError(Exception):
    """Raised when the RCON authentication / password is incorrect."""

    def __init__(self) -> None:
        super().__init__(
            "The password provided to the client was incorrect according to the server."
        )
