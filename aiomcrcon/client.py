"""
Contains the base class for the RCON Client
"""

import asyncio
import struct

from .types import PacketTypes
from .errors import *


class Client:
    """Base remote console client"""

    # host is a string like '0.0.0.0' or '0.0.0.0:25575', auth is a string (rcon.password in server.properties)
    def __init__(self, host: str, auth: str, timeout: int = 5, *, loop = None) -> None:
        split = host.split(':')

        self.host = split[0]
        self.port = int(split[1]) if len(split) > 1 else 25575

        self.auth = auth

        self.timeout = timeout

        self._reader = None
        self._writer = None

        self._loop = asyncio.get_event_loop() if loop is None else loop

        self._setup = False
        self._closed = False

    async def setup(self) -> None:
        """Setup and login the client"""

        if self._closed:
            raise ClientClosedError

        if self._setup:
            return

        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port, loop=self._loop),
                timeout=self.timeout,
                loop=self._loop
            )
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

        try:
            await self._send(PacketTypes.LOGIN, self.auth)
        except Exception as e:
            self._closed = True
            raise e

        self._setup = True

    async def _read(self, n_bytes: int) -> bytes:
        """Read data from the server"""

        data = b''

        while len(data) < n_bytes:
            data += await self._reader.read(n_bytes - len(data))

        return data

    # for _types: 3=login/authenticate, 2=command, 0=cmd response, -1=invalid auth
    async def _send(self, _type: int, msg: str) -> tuple:  # returns ('response from server': str, packet type from server: int)
        """Send data to the server, returns the server response and response packet type"""

        out_msg = struct.pack('<li', 0, _type) + msg.encode('utf8') + b'\x00\x00'
        out_len = struct.pack('<i', len(out_msg))
        self._writer.write(out_len + out_msg)
        await self._writer.drain()

        in_msg = await self._read(struct.unpack('<i', await self._read(4))[0])
        if in_msg[-2:] != b'\x00\x00':
            raise InvalidDataReceivedError

        in_type = struct.unpack('<ii', in_msg[:8])[0]
        if in_type == PacketTypes.INVALID_AUTH:
            raise InvalidAuthError

        return in_msg[8:-2].decode('utf8'), in_type

    async def send_cmd(self, cmd: str) -> tuple:  # returns ('response from server': str, packet type from server: int)
        """Helper function for sending a command to the server"""

        if self._closed:
            raise ClientClosedError

        if not self._setup:
            raise ClientNotSetupError

        return await self._send(PacketTypes.COMMAND, cmd)

    async def close(self) -> None:
        """Close the client and the connection to the server"""

        if not self._closed and self._setup:
            self._writer.close()

            try:
                await self._writer.wait_closed()
            except TimeoutError:
                pass

            self._reader = None
            self._writer = None

            self._closed = True
