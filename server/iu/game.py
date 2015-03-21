import iu.messages
from iu.utils import uuid
from iu.worldgenerator import StarGenerator


class GameObject(object):
    def update(self, time_elapsed):
        pass


class Player(GameObject):
    def __init__(self, id, connection_id):
        self.id = id
        self.connection_id = connection_id

        self.known_data = {}


class Star(GameObject):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "planets": []
        }

    def generate_planets(self):
        pass


class World(GameObject):
    LIGHT_SECOND = 1
    LIGHT_MINUTE = LIGHT_SECOND * 60
    LIGHT_HOUR = LIGHT_MINUTE * 60
    LIGHT_DAY = LIGHT_HOUR * 24
    LIGHT_YEAR = LIGHT_DAY * 365

    # Distance units in light seconds
    SIZE_X = 150000 * LIGHT_YEAR
    SIZE_Y = 150000 * LIGHT_YEAR

    def __init__(self):
        self.stars = []

    def generate(self):

        generator = StarGenerator()

        def add_star(x, y):
            star_id = "star_{}".format(uuid())
            star = Star(star_id, x, y)
            star.generate_planets()
            self.stars.append(star)

        generator.generateStars(add_star)

    def get_public_data(self):
        return {
            "width": self.SIZE_X,
            "height": self.SIZE_Y,
            "stars": [
                star.to_dict()
                for star in self.stars
            ],
        }

class Game(object):
    def __init__(self, logger):
        self.logger = logger

        self.players = {}
        self.world = World()
        self.messages = {}

        self.time_factor = 3600 * 24 * 365
        self.game_time = 0

        self.world.generate()

    def tick(self, real_time_elapsed):
        """
        Tick tock .. update everything in the game world

        :param float real_time_elapsed: How many seconds have elapsed in the
                                        real world since the last update.
        """

        game_time_elapsed = real_time_elapsed * self.time_factor

        self.world.update(game_time_elapsed)

        self.game_time += game_time_elapsed

        for player_id in self.players:
            player = self.players[player_id]
            player.update(game_time_elapsed)
            self.add_message(player, iu.messages.GameTime(self.game_time))

    def get_world_data(self):
        """
        Get all public info of the world
        :return:
        """

        return self.world.get_public_data()

    def register_player(self, player_id, connection_id):
        """
        Register a player connection
        :param player_id:
        :param connection_id:
        :return:
        """

        if not player_id in self.players:
            self.logger.info("New player with ID {}".format(
                player_id
            ))
            player = Player(player_id, connection_id)
            self.add_message(player, iu.messages.PlayerRegistered(
                player.id
            ))
            self.players[player_id] = player
        else:
            self.logger.info("Existing player {} reconnected".format(
                player_id
            ))
            player = self.players[player_id]
            self.add_message(player, iu.messages.ServerDisconnect(
                "Got new connection for player."
            ))
            player.connection_id = connection_id

        self.add_message(player, iu.messages.WorldData(
            self.get_world_data()
        ))

    def add_message(self, player, message):
        """
        Add a message to the outgoing message queue
        :param Player player:
        :param iu.messages.ServerMessage message:
        """

        connection_id = player.connection_id

        if not connection_id in self.messages:
            self.messages[connection_id] = []

        self.messages[connection_id].append(message)

    def get_messages(self):
        messages, self.messages = self.messages, {}
        return messages
