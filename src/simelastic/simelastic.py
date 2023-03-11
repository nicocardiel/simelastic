from .container3D import Cuboid3D
from .random_balls_in_container import random_balls_in_empty_container
from .run_simulation import run_simulation
from .time_rendering import time_rendering
from .version import version


def main():
    print(f'Inside main function of simelastic version {version}')

    box = Cuboid3D()

    balls = random_balls_in_empty_container(
        container=box,
        nballs=50,
        random_speed=0.1,
        debug=False
    )

    dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=False
    )

    time_rendering(
            dict_snapshots=dict_snapshots,
            container=box,
            outfilename='zzz.html',
            debug=True
    )

if __name__ == "__main__":

    main()
