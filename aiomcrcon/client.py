from __future__ import annotations

import asyncio
import random
import struct
import enum
import typing as t

from aiomcrcon.errors import ClientNotConnectedError, IncorrectPasswordError, RCONConnectionError


class MessageType(enum.IntEnum):
    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0


class Client:
    """The base class for creating an RCON client."""

    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.password = password

        self._reader = None
        self._writer = None

        self._ready = False

    async def __aenter__(self, timeout=2) -> Client:
        await self.connect(timeout)
        return self

    async def __aexit__(self, exc_type: type, exc: Exception, tb: t.Any) -> None:
        await self.close()

    async def connect(self, timeout: float = 2.0) -> None:
        """Sets up the connection between the client and server."""

        if self._ready:
            return

        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout
            )
        except (asyncio.TimeoutError, TimeoutError) as e:
            raise RCONConnectionError(
                "A timeout occurred whilst attempting to connect to the server.", e
            )
        except ConnectionRefusedError as e:
            raise RCONConnectionError("The remote server refused the connection.", e)
        except Exception as e:
            raise RCONConnectionError("The connection failed for an unknown reason.", e)

        await asyncio.wait_for(self._send_msg(MessageType.LOGIN, self.password), timeout)

        self._ready = True

    async def _read(self, n: int) -> bytes:
        out = b""

        while len(out) < n:
            received = await self._reader.read(n - len(out))

            if not received:
                break

            out += received

        return out

    async def _send_msg(self, msg_type: int, msg: str) -> tuple[str, int]:
        """Sends data to the server, and returns the response."""

        # randomly generate request id
        req_id = random.randint(0, 2147483647)

        # pack request id, packet type, and the actual message
        packet_data = struct.pack("<ii", req_id, msg_type) + msg.encode("utf8") + b"\x00\x00"

        # pack length of packet + rest of packet data
        packet = struct.pack("<i", len(packet_data)) + packet_data

        # send the data to the server
        self._writer.write(packet)
        await self._writer.drain()

        # read + unpack length of incoming packet
        in_len = struct.unpack("<i", await self._read(4))[0]

        # read rest of packet data
        in_data = await self._read(in_len)

        if len(in_data) != in_len or not in_data.endswith(b"\x00\x00"):
            raise ValueError("Invalid data received from server.")

        # decode the incoming request id and packet type
        in_req_id, in_type = struct.unpack("<ii", in_data[0:8])

        if in_req_id == -1:
            raise IncorrectPasswordError

        # decode the received message
        in_msg = in_data[8:-2].decode("utf8")

        return in_msg, in_req_id

    async def send_cmd(self, cmd: str, timeout: float = 2.0) -> tuple[str, int]:
        """Sends a command to the server."""

        if not self._ready:
            raise ClientNotConnectedError

        if len(cmd) > 1446:
            raise ValueError("Commands must be 1446 characters or less to be sent via RCON")

        return await asyncio.wait_for(self._send_msg(MessageType.COMMAND, cmd), timeout)

    async def close(self) -> None:
        """Closes the connection between the client and the server."""

        if self._ready:
            self._writer.close()
            await self._writer.wait_closed()

            self._reader = None
            self._writer = None

            self._ready = False
