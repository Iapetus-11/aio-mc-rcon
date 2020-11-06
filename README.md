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
