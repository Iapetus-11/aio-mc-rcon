import asyncio

from .errors import RCONConnectionError


class Client:
    def __init__(self, host: str, port: int, password: str, timeout: float = 2) -> None:
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout

        self._reader = None
        self._writer = None

        self._ready = False

    async def connect(self):
        if self._ready:
            return

        try:
            self._reader, self._writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port))
        except (asyncio.TimeoutError, TimeoutError) as e:
            raise RCONConnectionError("A timeout occurred whilst attempting to connect to the server.", e)
        except ConnectionRefusedError as e:
            raise RCONConnectionError("The remote server refused the connection.", e)
        except Exception as e:
            raise RCONConnectionError("The connection failed for an unknown reason.", e)
