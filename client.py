import asyncio
import struct


class RCONClient:
    def __init__(self, host, auth):
        split = host.split(':')

        self.host = split[0]
        self.port = int(split[1]) if len(split) > 1 else 25575

        self.auth = auth

        self._reader = None
        self._writer = None

        self._setup_task = asyncio.get_event_loop().create_task(self._setup())

    async def _setup(self):
        print('setting up')
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)

        await self._send(3, self.auth)

    async def _read(self, n_bytes):
        print('reading')
        data = b''

        while len(data) < n_bytes:
            data += await self._reader.read(n_bytes - len(data))

        return data

    async def _send(self, _type, msg):  # for _types: 3=login/authenticate, 2=command, 0=cmd response, -1=invalid auth
        print('sending')
        out_msg = struct.pack('<li', 0, _type) + msg.encode('utf8') + b'\x00\x00'
        out_len = struct.pack('<i', len(out_msg))
        self._writer.write(out_len + out_msg)

        in_len = struct.unpack('<i', await self._read(4))
        in_msg = await self._read(in_len[0])

        in_id = struct.unpack('<ii', in_msg[:8])[0]
        in_data, in_pad = in_msg[8:-2], in_msg[-2:]

        if in_id == -1: raise Exception('Invalid authentication')
        if in_pad != b'\x00\x00': raise Exception('Invalid response')

        return in_data.decode('utf8')

    async def send_command(self, msg):
        await self._setup_task
        return await self._send(2, msg)

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()
