
class PacketTypes:
    """Packet types that can be sent or received"""

    def __init__(self):
        self.LOGIN = 3
        self.COMMAND = 2
        self.COMMAND_RESPONSE = 0
        self.INVALID_AUTH = -1
