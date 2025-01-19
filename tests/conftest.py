import pytest

from aiomcrcon.client import Client
from rcon_server import Server


@pytest.fixture
async def dummy_server(unused_tcp_port):
    server = Server(
        host="localhost",
        port=unused_tcp_port,
        password="hunter2",
    )

    await server.start()

    yield server

    await server.close()


@pytest.fixture
def client(dummy_server):
    return Client(
        host=dummy_server.host,
        port=dummy_server.port,
        password=dummy_server.password,
    )
