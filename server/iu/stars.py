from iu.objects import GameObject


class Star(GameObject):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "planets": []
        }

    def generate_planets(self):
        pass


class RedDwarf(Star):
    RELATIVE_FREQUENCY = 150


class YellowDwarf(Star):
    RELATIVE_FREQUENCY = 80

class RedGiant(Star):
    RELATIVE_FREQUENCY = 3

class BlueGiant(Star):
    RELATIVE_FREQUENCY = 1


STAR_CHOICES = [
    (cls, cls.RELATIVE_FREQUENCY)
    for cls in Star.__subclasses__()
]