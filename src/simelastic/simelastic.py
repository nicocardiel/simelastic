# -*- coding: utf-8 -*-
#
# Copyright 2023 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

import argparse
import sys

from .container3D import Cuboid3D
from .random_balls_in_container import random_balls_in_empty_container
from .run_simulation import run_simulation
from .time_rendering import time_rendering
from .version import version


def main():
    parser = argparse.ArgumentParser(description=f"Simulation of elastic collisions (version {version})")
    parser.add_argument("-n", "--nexample", help="example number", type=int)
    parser.add_argument("-o", "--output", help="output HTML file name", type=str, default="zzz.html")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        raise SystemExit()


    if args.nexample == 0:
        box = Cuboid3D(xmin=-8, xmax=8)

        balls = random_balls_in_empty_container(
            container=box,
            nballs=50,
            random_speed=0.05,
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
            tstep=0.5,
            outfilename=args.output,
            debug=True
        )
    else:
        print('ERROR: undefined example number')


if __name__ == "__main__":

    main()
