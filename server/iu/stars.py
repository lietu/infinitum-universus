import random
from iu.objects import GameObject
from iu.utils import uuid, roman

class Planet(GameObject):
    def __init__(self, id, name, orbit, star):
        self.id = id
        self.name = name
        self.orbit = orbit
        self.star = star

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "orbit": self.orbit
        }


class Star(GameObject):
    RELATIVE_FREQUENCY = 0
    PLANETS_MAX = 0
    PLANETS_CHANCE = 0
    HABITABLE_ZONE = (0, 0)

    ORBITS = [
        200, 400, 600, 800, 1200, 1600, 2400, 2800, 3200, 3600, 4000, 4400,
        4800, 5200, 5600, 6000, 6400, 6800, 7200, 7600, 8000, 8400, 8800, 9200,
        9600, 10000, 10400, 10800, 11200, 11600, 12000, 12400, 12800, 13200,
        13600, 14000, 14400, 14800, 15200, 15600, 16000
    ]

    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position
        self.planets = {}

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "position": self.position.to_dict()
        }

    def get_sensor_data(self):
        planets = {}

        for id in self.planets:
            planets[id] = self.planets[id].to_dict()

        return {
            "planets": planets
        }

    def generate_planets(self):
        if random.random() < self.PLANETS_CHANCE:
            planet_count = random.randint(1, self.PLANETS_MAX)
            orbits = sorted(random.sample(self.ORBITS, planet_count))
            for i in range(planet_count):
                id = "planet_{}".format(uuid())
                name = "{} {}".format(self.name, roman(i + 1))
                orbit = orbits[i]
                self.planets[id] = Planet(id, name, orbit, self)


class RedDwarf(Star):
    RELATIVE_FREQUENCY = 150
    PLANETS_MAX = 10
    PLANETS_CHANCE = 0.7


class YellowDwarf(Star):
    RELATIVE_FREQUENCY = 80
    PLANETS_MAX = 10
    PLANETS_CHANCE = 0.95

    HABITABLE_ZONE = (400, 800)


class RedGiant(Star):
    RELATIVE_FREQUENCY = 3
    PLANETS_MAX = 3
    PLANETS_CHANCE = 0.1


class BlueGiant(Star):
    RELATIVE_FREQUENCY = 1
    PLANETS_MAX = 3
    PLANETS_CHANCE = 0.1


STAR_CHOICES = [
    (cls, cls.RELATIVE_FREQUENCY)
    for cls in Star.__subclasses__()
]