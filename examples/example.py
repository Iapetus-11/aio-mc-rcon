from aiomcrcon import Client
import asyncio


async def main():
    password = input("Password? ")
    command = input("Command? ")

    client = Client("xenonmc.ml", 25566, password)
    await client.connect()

    response = await client.send_cmd(command)
    print(response)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
