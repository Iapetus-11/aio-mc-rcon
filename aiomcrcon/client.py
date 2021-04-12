
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
        except TimeoutError
