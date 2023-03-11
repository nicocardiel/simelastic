# import copy
# import math
# import numpy as np
# from scipy.interpolate import interp1d
# import sys
import copy

# from vector3D import Vector3D
# from container3D import Container3D, Cuboid3D, VerticalCylinder3D
# from ball import Ball, BallCollection

from .container3D import Cuboid3D
from .random_balls_in_container import random_balls_in_empty_container
from .run_simulation import run_simulation
from .version import version


def main():
    print(f'Inside main function of simelastic version {version}')

    box = Cuboid3D()

    balls = random_balls_in_empty_container(
        container=box,
        nballs=3,
        random_speed=0.1,
        debug=False
    )

    dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=False
    )


if __name__ == "__main__":

    main()
