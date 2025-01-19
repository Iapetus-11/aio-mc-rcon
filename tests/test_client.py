import asyncio
import random
from unittest.mock import Mock
import pytest

from aiomcrcon import Client
from aiomcrcon.client import MessageType
from aiomcrcon.errors import ClientNotConnectedError, IncorrectPasswordError, RCONConnectionError


async def test_success_send_msg(monkeypatch, client: Client):
    req_id = random.randint(0, 2147483647)

    monkeypatch.setattr(random, "randint", lambda *_: req_id)

    async with client:
        (msg, response_id) = await client._send_msg(MessageType.COMMAND, "say Hello, world!")
        assert msg == "say Hello, world!"
        assert response_id != -1


@pytest.mark.parametrize(
    "command",
    [
        "",
        "test",
        "test something longer test something longer",
        "test\n new\n lines",
        "a" * 1446,
    ],
)
async def test_success_send_cmd(client: Client, command):
    async with client:
        (response, response_id) = await client.send_cmd(command)

        assert response == command
        assert response_id != -1


async def test_incorrect_password(client: Client):
    client.password = "nottherealpassword123"

    with pytest.raises(IncorrectPasswordError):
        await client.connect()


async def test_client_not_connected(client: Client):
    with pytest.raises(ClientNotConnectedError):
        await client.send_cmd("say Hello, world!")


async def test_server_offline(unused_tcp_port):
    client = Client(
        host="localhost",
        port=unused_tcp_port,
        password="password123",
    )

    with pytest.raises(RCONConnectionError):
        await client.connect()


async def test_server_timeout(monkeypatch, client):
    monkeypatch.setattr(asyncio, "open_connection", Mock(side_effect=TimeoutError))

    with pytest.raises(RCONConnectionError):
        await client.connect()
