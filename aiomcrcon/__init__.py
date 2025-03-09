import importlib.metadata

from .client import MessageType, Client
from .errors import RCONConnectionError, ClientNotConnectedError, IncorrectPasswordError

__version__ = importlib.metadata.version("aio-mc-rcon")

__all__ = (
    "MessageType",
    "Client",
    "RCONConnectionError",
    "ClientNotConnectedError",
    "IncorrectPasswordError",
    "__version__",
)
