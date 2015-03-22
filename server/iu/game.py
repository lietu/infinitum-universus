import math
import random
import iu.messages
from iu.objects import GameObject
from iu.stars import STAR_CHOICES
from iu.utils import uuid, weighted_choice, Coords, within_bounds
from iu.worldgenerator import StarGenerator


class Unit(GameObject):
    BASE_HEALTH = 0

    def __init__(self, owner, position):
        self.id = "{}_{}".format(
            self.__class__.__name__,
            uuid()
        )

        self.owner = owner
        self.position = position
        self.health = self.BASE_HEALTH
        self.target = None
        self.velocity = 0
        self.direction = Coords(0, 0)

        self.action_queue = []

    def to_dict(self):
        data = {
            "id": self.id,
            "type": self.__class__.__name__,
            "owner": self.owner.id,
            "position": self.position.to_dict(),
            "health": self.health
        }

        return data

    def set_target(self, target):
        if not self.target:
            self.set_active_target(target)
        else:
            self.action_queue.append(target)

    def set_active_target(self, target):
        self.target = target

        distance = (
            self.target.x - self.position.x,
            self.target.y - self.position.y
        )

        normal = math.sqrt(distance[0] ** 2.0 + distance[1] ** 2.0)

        self.direction.x = distance[0] / normal
        self.direction.y = distance[1] / normal

    def target_reached(self):
        if self.action_queue:
            self.set_active_target(self.action_queue.pop(0))
        else:
            self.set_velocity(0)
            self.target = None

    def set_velocity(self, velocity):
        """
        Set the unit's velocity towards it's target, in light seconds/s
        :param float velocity:
        :return:
        """
        self.velocity = velocity

    def update(self, time_elapsed):
        origin = self.position.clone()

        if self.target:
            target_reached = False
            distance = time_elapsed * self.velocity

            destination = Coords(
                self.position.x + (self.direction.x * distance),
                self.position.y + (self.direction.y * distance),
            )

            if within_bounds(self.target, origin, destination):
                destination = self.target
                target_reached = True

            self.position.x = destination.x
            self.position.y = destination.y

            if target_reached:
                self.target_reached()


class SpaceShip(Unit):
    BASE_HEALTH = 5


class Player(GameObject):
    def __init__(self, id, connection_id):
        self.id = id
        self.connection_id = connection_id
        self.known_data = {}
        self.units = {}

    def get_units(self):
        return self.units

    def click(self, x, y):
        target = Coords(x, y)
        for unit_id in self.units:
            self.units[unit_id].set_target(target)
            self.units[unit_id].set_velocity(1024)

    def get_data_update_message(self):
        return iu.messages.PlayerDataUpdate(
            units=self.get_units()
        )


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
            star_class = weighted_choice(STAR_CHOICES)
            star = star_class(star_id, x, y)
            star.generate_planets()
            self.stars.append(star)

        generator.generate_stars(add_star)

    def get_random_coords(self):
        return Coords(
            x=random.randint(self.SIZE_X * -0.5, self.SIZE_X * 0.5),
            y=random.randint(self.SIZE_Y * -0.5, self.SIZE_Y * 0.5)
        )

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

        self.connection_player = {}
        self.players = {}
        self.units = {}
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
        self.game_time += game_time_elapsed

        self.world.update(game_time_elapsed)

        for unit_id in self.units:
            self.units[unit_id].update(game_time_elapsed)

        for player_id in self.players:
            player = self.players[player_id]
            player.update(game_time_elapsed)
            self.add_message(player, iu.messages.GameTime(self.game_time))
            self.add_message(player, player.get_data_update_message())

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

        if not player_id or player_id not in self.players:
            player_id = "player_{}".format(uuid())

            self.logger.info("New player with ID {}".format(
                player_id
            ))
            player = Player(player_id, connection_id)
            self.add_message(player, iu.messages.PlayerRegistered(
                player.id
            ))
            self.players[player_id] = player

            ship = SpaceShip(player, Coords(0,0))
            player.units[ship.id] = ship
            self.units[ship.id] = ship
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

        self.add_message(player, iu.messages.PlayerDataUpdate(
            units=player.get_units()
        ))

        self.connection_player[connection_id] = player_id

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
