"""
Rough and dirty implementation of an RCON server for testing the Client against.
In the future, this may become part of the actual library, but for now I don't
want to put forth the effort of writing quality code.
"""

from __future__ import annotations

import asyncio
import struct

from aiomcrcon.client import MessageType


class Server:
    packet_HEADER_FORMAT = "<iii"
    packet_HEADER_SIZE = struct.calcsize(packet_HEADER_FORMAT)

    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.password = password

        self.server: asyncio.Server | None = None
        self.client_tasks: list[asyncio.Task] = []

    @classmethod
    async def read_bytes(cls, reader: asyncio.StreamReader, n: int) -> bytes:
        out = b""

        while len(out) < n:
            received = await reader.read(n - len(out))

            if not received:
                break

            out += received

        return out

    @classmethod
    async def read_packet(cls, reader: asyncio.StreamReader) -> tuple[int, int, bytes] | None:
        header_data = await cls.read_bytes(reader, cls.packet_HEADER_SIZE)

        if not header_data:
            return None

        packet_length: int
        packet_id: int
        packet_type: int
        packet_length, packet_id, packet_type = struct.unpack(
            cls.packet_HEADER_FORMAT,
            header_data,
        )

        # Compensate for the bytes we've already read as part of the header
        packet_length -= cls.packet_HEADER_SIZE - struct.calcsize("<i")

        packet_data = await cls.read_bytes(reader, packet_length)

        if not packet_data.endswith(b"\0\0"):
            raise Exception("Expected request data to end with two null bytes")

        return (packet_id, packet_type, packet_data[:-2])

    @classmethod
    async def write_packet(
        cls, writer: asyncio.StreamWriter, packet_id: int, packet_type: int, message: bytes
    ) -> int:
        packet_data = struct.pack("<ii", packet_id, packet_type) + message + b"\0\0"

        packet = struct.pack("<i", len(packet_data)) + packet_data

        writer.write(packet)
        await writer.drain()

    async def client_loop(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        authenticated = False

        while self.server is not None and not writer.is_closing():
            packet = await self.read_packet(reader)

            if packet is None:
                await asyncio.sleep(0.25)
                continue

            (packet_id, packet_type, packet_data) = packet

            if not authenticated:
                if packet_type != MessageType.LOGIN:
                    # Honestly not sure what the actual behavior is...
                    await self.write_packet(writer, -1, MessageType.RESPONSE, b"")
                    break

                if packet_data != self.password.encode("utf8"):
                    await self.write_packet(writer, -1, MessageType.RESPONSE, b"")
                    break

                authenticated = True

            # Echoooooooo
            await self.write_packet(writer, packet_id, MessageType.RESPONSE, packet_data)

        writer.close()
        await writer.wait_closed()

    async def on_client_connected(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.client_tasks.append(asyncio.create_task(self.client_loop(reader, writer)))

    async def start(self) -> None:
        self.server = await asyncio.start_server(
            self.on_client_connected,
            host=self.host,
            port=self.port,
        )

    async def close(self) -> None:
        self.server.close()

        for task in self.client_tasks:
            task.cancel()

        self.server = None
