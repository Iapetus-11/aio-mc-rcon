
class TimeoutError(Exception):
    """Raised when a timeout occurs"""

    def __init__(self, reason='TimeoutError'):
        self.reason = reason

    def __str__(self):
        return self.reason


class InvalidAuthError(Exception):
    """Raised when the password is incorrect"""

    def __str__(self):
        return 'The provided authentication/password was invalid'


class InvalidDataReceivedError(Exception):
    """Raised when the client receives invalid data from the server"""

    def __str__(self):
        return 'Invalid data was received from the server'
