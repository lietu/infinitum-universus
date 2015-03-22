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
    DATA_KEYS = ["id"]

    def __init__(self, id):
        self.id = id


class WorldData(ServerMessage):
    DATA_KEYS = ["data"]

    def __init__(self, data):
        self.data = data


class PlayerDataUpdate(ServerMessage):
    DATA_KEYS = ["units", "known_data"]

    def __init__(self, units, known_data):
        self.units = {}
        self.known_data = known_data

        for id in units:
            self.units[id] = units[id].to_dict()


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

    def process(self):
        self.game.register_player(self.player_id, self.connection_id)


class PlayerClick(ClientMessage):
    VALID_DATA_KEYS = ["x", "y"]

    def __init__(self, game, connection_id, data):
        self.connection_id = connection_id
        self.x = None
        self.y = None

        super(PlayerClick, self).__init__(game, connection_id, data)

    def process(self):
        player_id = self.game.connection_player[self.connection_id]
        self.game.players[player_id].click(self.x, self.y)


CLIENT_MESSAGES = {}
for subclass in ClientMessage.__subclasses__():
    CLIENT_MESSAGES[subclass.__name__] = subclass
