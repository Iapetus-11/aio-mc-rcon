import aiomcrcon
import asyncio


async def main():
    password = input("Password? ")
    command = input("Command? ")

    client = aiomcrcon.Client("xenonmc.ml", 25566, password)

    try:
        await client.connect()
    except aiomcrcon.RCONConnectionError:
        print("An error occurred whilst connecting to the server...")
        return
    except aiomcrcon.IncorrectPasswordError:
        print("The provided password was incorrect...")
        return

    try:
        response = await client.send_cmd(command)
    except aiomcrcon.ClientNotConnectedError:
        print("The client was not connected to the server for some reason?")
        return

    print(response)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
