# Aio-MC-RCON
An async RCON client/wrapper written in Python for Minecraft Java Edition servers

## Installation
Via pip:
```python3 -m pip install -U aio-mc-rcon```
or
```pip3 install -U aio-mc-rcon```

## Example Usage
```py
import aiomcrcon
import asyncio

async def main():
  client = aiomcrcon.Client('1.2.3.4:25575', 'super-secret-password')

  await client.setup()

  output = await client.send_cmd('list')
  print(output)

  await client.close()

asyncio.run(main())
```

## Documentation
#### *class* aiomcrcon.**Client**(host: *str*, auth: *str*)
* Note: It is highly recommended to call the close() coroutine on the client when the client is done being used
* Arguments:
  * `host: str` The hostname/ip of the server to connect to, if no port is specified, the default port (25575) is used.
  * `auth: str` The authentication/password for the rcon server (This is `rcon.password` in the `server.properties` file)
  * `timeout: int` How long to wait in seconds for a connection to the server
* Coroutines:
  * `send_cmd(cmd: str)` - where `cmd` is the command to be sent to the server
  * `close()` - close the connection to the Minecraft server

#### *class* aiomcrcon.**PacketTypes**()
* Attributes:
  * `LOGIN: int` - The packet id / type for a LOGIN packet
  * `COMMAND: int` - The packet id / type for a COMMAND packet
  * `COMMAND_RESPONSE: int` - The packet id / type for a COMMAND_RESPONSE packet
  * `INVALID_AUTH: int` - The packet id / type for an INVALID_AUTH packet

#### *exception* aiomcrcon.**ConnectionFailedError** - Raised when the connection to the server failed

#### *exception* aiomcrcon.**InvalidAuthError** - Raised when the provided password/authentication is invalid

#### *exception* aiomcrcon.**InvalidDataReceivedError** - Raised when the data the server sends back is invalid

#### *exception* aiomcrcon.**ClientClosedError** - Raised when a function is called after the client has closed its connection to the server
