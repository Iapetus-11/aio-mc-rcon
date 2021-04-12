class RCONConnectionError(Exception):
    def __init__(self, msg: str = None, error: Exception = None):
        super().__init__(msg)

        self.message = msg
        self.error = error
