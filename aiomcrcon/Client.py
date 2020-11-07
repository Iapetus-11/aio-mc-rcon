import asyncio
import struct

from .Types import PacketTypes
from .Errors import ConnectionFailedError, InvalidAuthError, InvalidDataReceivedError, ClientClosedError


class Client:
    """Base remote console client"""

    def __init__(self, host: str, auth: str, timeout: int = 5, *, loop = None) -> None:  # host is a string like '0.0.0.0' or '0.0.0.0:25575', auth is a string (rcon.password in server.properties)
        split = host.split(':')

        self.host = split[0]
        self.port = int(split[1]) if len(split) > 1 else 25575

        self.auth = auth

        self.timeout = timeout

        self._reader = None
        self._writer = None

        self._loop = asyncio.get_event_loop() if loop is None else loop

        self._setup_task = self._loop.create_task(self._setup())

        self._closed = False

    async def _setup(self) -> None:
        try:
            result = await asyncio.gather(
                asyncio.wait_for(
                    asyncio.open_connection(self.host, self.port, loop=self._loop), timeout=self.timeout, loop=self._loop
                ),
                loop=self._loop, return_exceptions=True
            )

            result = result[0]

            if isinstance(result, Exception):
                raise result

            self._reader, self._writer = result
        except TimeoutError:
            self._closed = True
            raise ConnectionFailedError('A timeout occurred while attempting to connect to the server')
        except asyncio.TimeoutError:
            self._closed = True
            raise ConnectionFailedError('A timeout occurred while attempting to connect to the server')
        except ConnectionRefusedError:
            self._closed = True
            raise ConnectionFailedError('The connection was refused by the server')
        except Exception as e:
            self._closed = True
            raise ConnectionFailedError(f'The connection failed for an unknown reason: {e}')

        await self._send(PacketTypes.LOGIN, self.auth)

    async def _read(self, n_bytes: int) -> bytes:
        data = b''

        while len(data) < n_bytes:
            data += await self._reader.read(n_bytes - len(data))

        return data

    # for _types: 3=login/authenticate, 2=command, 0=cmd response, -1=invalid auth
    async def _send(self, _type: int, msg: str) -> tuple:  # returns ('response from server': str, packet type from server: int)
        out_msg = struct.pack('<li', 0, _type) + msg.encode('utf8') + b'\x00\x00'
        out_len = struct.pack('<i', len(out_msg))
        self._writer.write(out_len + out_msg)
        await self._writer.drain()

        in_msg = await self._read(struct.unpack('<i', await self._read(4))[0])
        if in_msg[-2:] != b'\x00\x00': raise InvalidDataReceivedError

        in_type = struct.unpack('<ii', in_msg[:8])[0]
        if in_type == PacketTypes.INVALID_AUTH: raise InvalidAuthError

        return in_msg[8:-2].decode('utf8'), in_type

    async def send_cmd(self, cmd: str) -> tuple:  # returns ('response from server': str, packet type from server: int)
        if self._closed:
            raise ClientClosedError

        if not self._setup_task.done():
            await self._setup_task

        return await self._send(PacketTypes.COMMAND, cmd)

    async def close(self) -> None:
        if not self._closed:
            self._writer.close()
            await self._writer.wait_closed()

            self._reader = None
            self._writer = None

            self._closed = True
