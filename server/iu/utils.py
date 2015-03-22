import random
import logging
import uuid as _uuid
from iu.distances import LIGHT_YEAR

ROMAN_NUMBERS = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
    13: "XIII"
}


def _get_logger():
    _logger = logging.getLogger("iu")
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s'
    ))
    _logger.addHandler(ch)
    return _logger


def roman(number):
    return ROMAN_NUMBERS[number]


class Map(object):
    def __init__(self):
        self.granularity = 10 * LIGHT_YEAR
        self.data = {}

    def add_item(self, item):
        x, y = self._get_map_position(item.position)

        if not x in self.data:
            self.data[x] = {}

        if not y in self.data[x]:
            self.data[x][y] = []

        self.data[x][y].append(item)

    def get_items(self, corner1, corner2):
        map_x_1, map_y_1 = self._get_map_position(corner1)
        map_x_2, map_y_2 = self._get_map_position(corner2)

        found = []

        minx = min(map_x_1, map_x_2)
        maxx = max(map_x_1, map_x_2)

        miny = min(map_y_1, map_y_2)
        maxy = max(map_y_1, map_y_2)

        for x in range(minx, maxx + 1):
            if x not in self.data:
                continue

            for y in range(miny, maxy + 1):
                if y not in self.data[x]:
                    continue

                for item in self.data[x][y]:
                    if within_bounds(item.position, corner1, corner2):
                        found.append(item)

        return found

    def _get_map_position(self, coords):
        return (
            int(coords.x / self.granularity),
            int(coords.y / self.granularity)
        )


class Coords(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }

    def clone(self):
        return Coords(self.x, self.y)


def uuid():
    return str(_uuid.uuid4())


def within_bounds(item, coords1, coords2):
    """
    Check if given item is within the plane specified by the two corner Coords
    :param Coords item:
    :param Coords coords1:
    :param Coords coords2:
    :return bool:
    """

    minx = min(coords1.x, coords2.x)
    maxx = max(coords1.x, coords2.x)

    miny = min(coords1.y, coords2.y)
    maxy = max(coords1.y, coords2.y)

    if item.x >= minx and item.x <= maxx and item.y >= miny and item.y <= maxy:
        return True

    return False


def weighted_choice(choices):
    """
    Pick a weighted value off

    :param list choices: Each item is a tuple of choice and weight
    :return:
    """

    total = sum(weight for choice, weight in choices)
    selection = random.uniform(0, total)
    counter = 0
    for choice, weight in choices:
        if counter + weight > selection:
            return choice
        counter += weight
    assert False, "Shouldn't get here"


logger = _get_logger()
