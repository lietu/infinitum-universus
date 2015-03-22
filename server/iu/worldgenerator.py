"""
Based on https://www.ailis.de/~k/uploads/software/galaxygen/galaxygen.py
by Klaus Reimer
"""

import random
import math


class StarGenerator(object):
    def __init__(self):
        # Number of stars in the core (Example: 2000)
        self.hub_stars = 5000

        # Number of stars in the disk (Example: 4000)
        self.disk_stars = 15000

        # Radius of the disk (Example: 90.0)
        self.disk_radius = 1400000000000.0

        # Radius of the hub (Example: 45.0)
        self.hub_radius = 857000000000.0

        # Number of arms (Example: 3)
        self.arms = 3

        # Tightness of winding (Example: 0.5)
        self.arm_rotations = 1

        # Arm width in degrees (Not affected by number of arms or rotations)
        # Example: 65.0
        self.arm_width = 50

        # Maximum outlier distance from arms (Example: 25.0)
        self.fuzz = 35.0

    def generate_stars(self, add_star):
        # omega is the separation (in degrees) between each arm
        # Prevent div by zero error:
        rotation = random.randint(0, 360)

        if self.arms:
            omega = 360.0 / self.arms
        else:
            omega = 0.0
        i = 0
        while i < self.disk_stars:
            # Choose a random distance from center
            distance = self.hub_radius + random.random() * self.disk_radius

            # This is the 'clever' bit, that puts a star at a given distance
            # into an arm: First, it wraps the star round by the number of
            # rotations specified. By multiplying the distance by the number of
            # rotations the rotation is proportional to the distance from the
            # center, to give curvature
            theta = (
                (
                    360.0 * self.arm_rotations *
                    (distance / self.disk_radius)
                )

                # Then move the point further around by a random factor up to
                # arm width
                + random.random() * self.arm_width

                # Then multiply the angle by a factor of omega, putting the
                # point into one of the arms
                + (rotation + omega * random.randrange(0, self.arms) % 360.0)

                # Add a further random factor, 'fuzzin' the edge of the arms
                + random.randrange(-self.fuzz, self.fuzz)
            )

            # Convert to cartesian
            x = math.cos(theta * math.pi / 180.0) * distance
            y = math.sin(theta * math.pi / 180.0) * distance

            # Add star
            add_star(x, y)

            # Process next star
            i += 1

        # Now generate the Hub. This places a point on or under the curve
        # maxHubZ - s d^2 where s is a scale factor calculated so that z = 0 is
        # at maxHubR (s = maxHubZ / maxHubR^2) AND so that minimum hub Z is at
        # maximum disk Z. (Avoids edge of hub being below edge of disk)

        i = 0
        while i < self.hub_stars:
            # Choose a random distance from center
            distance = random.random() * self.hub_radius

            # Any rotation (points are not on arms)
            theta = random.random() * 360

            # Convert to cartesian
            x = math.cos(theta * math.pi / 180.0) * distance
            y = math.sin(theta * math.pi / 180.0) * distance

            # Add star
            add_star(x, y)

            # Process next star
            i += 1
