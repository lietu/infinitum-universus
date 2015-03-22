import random
import logging
import uuid as _uuid


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
