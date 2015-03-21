from iu.utils import uuid


class ServerMessage(object):
    DATA_KEYS = []

    def to_dict(self):
        """
        Convert data in this object to a JSON encodable dictionary
        :return dict:
        """
        data = {
            "type": self.__class__.__name__
        }

        for key in self.__class__.DATA_KEYS:
            data[key] = getattr(self, key)

        return data


class ServerDisconnect(ServerMessage):
    DATA_KEYS = ["message"]

    def __init__(self, message):
        self.message = message


class PlayerRegistered(ServerMessage):
    DATA_KEYS = ["player_id"]

    def __init__(self, player_id):
        self.player_id = player_id


class WorldData(ServerMessage):
    DATA_KEYS = ["data"]

    def __init__(self, data):
        self.data = data


class GameTime(ServerMessage):
    DATA_KEYS = ["time"]

    def __init__(self, time):
        self.time = time


class ClientMessage(object):
    VALID_DATA_KEYS = []

    def __init__(self, game, connection_id, data):
        self.game = game
        self.connection_id = connection_id

        for key in data:
            if key in self.__class__.VALID_DATA_KEYS:
                setattr(self, key, data[key])

    def process(self):
        raise NotImplementedError("Message without processing")


class RegisterPlayer(ClientMessage):
    VALID_DATA_KEYS = ["player_id"]

    def __init__(self, game, connection_id, data):
        self.player_id = None
        self.connection_id = connection_id

        super(RegisterPlayer, self).__init__(game, connection_id, data)

        if not self.player_id:
            self.player_id = "player_{}".format(uuid())

    def process(self):
        self.game.register_player(self.player_id, self.connection_id)


CLIENT_MESSAGES = {
    "RegisterPlayer": RegisterPlayer
}
