from aiomcrcon import Client
import asyncio


async def main():
    password = input("Password? ")
    command = input("Command? ")

    async with Client("xenonmc.ml", 25566, password) as client:
        response = await client.send_cmd(command)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
