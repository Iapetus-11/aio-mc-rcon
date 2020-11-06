# Aio-MC-RCON
An async RCON client written in Python for Minecraft Java Edition servers

## Example Usage
```py
import aiomcrcon
import asyncio

async def main():
  client = aiomcrcon.Client('1.2.3.4:25575', 'super-secret-password')

  output = await client.send_cmd('list')
  print(output)

  await client.close()

asyncio.run(main())
```

## Documentation
### aiomcrcon.**Client**(host: *str*, auth: *str*)
* Note: It is highly recommended to call the close() coroutine on the client when the client is done being used
* Arguments:
  * `host: str` The hostname/ip of the server to connect to, if no port is specified, the default port (25575) is used.
  * `auth: str` The authentication/password for the rcon server (This is `rcon.password` in the `server.properties` file)
* Coroutines:
  * `send_cmd(cmd: str)` - where `cmd` is the command to be sent to the server
  * `close()` - close the connection to the Minecraft server

### Exceptions
#### aiomcrcon.**InvalidAuthError**
* Raised when 
