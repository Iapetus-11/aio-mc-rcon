"""
Contains a class for storing the different types of packets used by RCON
"""


class PacketTypes:
    """Packet types that can be sent or received"""

    LOGIN = 3
    COMMAND = 2
    COMMAND_RESPONSE = 0
    INVALID_AUTH = -1
