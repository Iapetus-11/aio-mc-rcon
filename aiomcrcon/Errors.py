"""
Contains all the custom errors that can be raised by the client
"""


class ConnectionFailedError(Exception):
    """Raised when the client cannot connect to the given server"""

    def __init__(self, reason):
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


class ClientClosedError(Exception):
    """Raised when a function is used when the client is supposed to be closed"""

    def __str__(self):
        return 'The client is closed'

class ClientNotSetupError(Exception):
    """Raised when a function is used when the client setup() function hasn't been called"""

    def __str__(self):
        return 'The client hasn\'t been setup. (Looks like you forgot to call the setup() coroutine)'
