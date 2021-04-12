class RCONConnectionError(Exception):
    """Raised when the Client.connect() method fails."""

    def __init__(self, msg: str = None, error: Exception = None):
        super().__init__(msg)

        self.message = msg
        self.error = error
