import asyncio
import struct

from .Types import PacketTypes
from .Errors import InvalidAuthError, InvalidDataReceivedError


class Client:
    """Base remote console client"""

    def __init__(self, host, auth):
        split = host.split(':')

        self.host = split[0]
        self.port = int(split[1]) if len(split) > 1 else 25575

        self.auth = auth

        self._reader = None
        self._writer = None

        self._setup_task = asyncio.get_event_loop().create_task(self._setup())

    async def _setup(self):
        try:
            self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        except TimeoutError:
            raise TimeoutError('A timeout occurred while attempting to connect to the server')

        await self._send(PacketTypes.LOGIN, self.auth)

    async def _read(self, n_bytes):
        data = b''

        while len(data) < n_bytes:
            data += await self._reader.read(n_bytes - len(data))

        return data

    async def _send(self, _type, msg):  # for _types: 3=login/authenticate, 2=command, 0=cmd response, -1=invalid auth
        out_msg = struct.pack('<li', 0, _type) + msg.encode('utf8') + b'\x00\x00'
        out_len = struct.pack('<i', len(out_msg))
        self._writer.write(out_len + out_msg)

        in_msg = await self._read(struct.unpack('<i', await self._read(4))[0])
        if in_msg[-2:] != b'\x00\x00': raise InvalidDataReceivedError

        in_type = struct.unpack('<ii', in_msg[:8])[0]
        if in_type == PacketTypes.INVALID_AUTH: raise InvalidAuthError

        return in_msg[8:-2].decode('utf8'), in_type

    async def send_cmd(self, msg):
        if not self._setup_task.done():
            await self._setup_task

        return await self._send(PacketTypes.COMMAND, msg)

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()
