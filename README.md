# Aio-MC-RCON ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/aio-mc-rcon/badge) ![PYPI Version](https://img.shields.io/pypi/v/aio-mc-rcon.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/aio-mc-rcon?color=0FAE6E)
An asynchronous RCON client/wrapper written in Python for Minecraft Java Edition servers!

## Installation
```
pip install -U aio-mc-rcon
```

## Example Usage
- See the [examples folder](https://github.com/Iapetus-11/aio-mc-rcon/tree/main/examples).

## Documentation
#### *class* aiomcrcon.**Client**(host: *str*, port: *int*, password: *str*):
- Arguments:
  - `host: str` - *The hostname / ip of the server to connect to.*
  - `port: int` - *The port of the server to connect to.*
  - `password: str` - *The password to connect, can be found as the value under `rcon.password` in the `server.properties` file.*
- Methods:
  - `connect(timeout: int = 2)` - *where `timeout` has a default value of 2 seconds.*
  - `send_cmd(cmd: str, timeout: int = 2)` - *where `cmd` is the command to be executed on the server and timeout has a default value of 2 seconds.*
  - `close()` - *closes the connection between the client and server.*

#### *exception* aiomcrcon.**RCONConnectionError**
- *Raised when the connection to the server fails.*

#### *exception* aiomcrcon.**IncorrectPasswordError**
- *Raised when the provided password/authentication is invalid.*

#### *exception* aiomcrcon.**ClientNotConnectedError**
- *Raised when the connect() method hasn't been called yet, and commands cannot be sent.*
