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

from .ball import Ball, BallCollection
from .container3D import Cuboid3D
from .random_balls_in_container import random_balls_in_empty_container
from .run_simulation import run_simulation
from .time_rendering import time_rendering
from .vector3D import Vector3D
from .version import version


def main():
    parser = argparse.ArgumentParser(description=f"Simulation of elastic collisions (version {version})")
    parser.add_argument("-n", "--nexample", help="example number", type=int)
    parser.add_argument("-o", "--output", help="output HTML file name", type=str, default="zzz.html")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        raise SystemExit()

    nexample = args.nexample

    if nexample == 0:
        box = Cuboid3D()
        b1 = Ball(
            position=Vector3D(4.5, 0.0, 0.0),
            velocity=Vector3D(-0.1, 0.0, 0.0),
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            container=box
        )
        b2 = Ball(
            position=Vector3D(0.0, 4.5, 0.0),
            velocity=Vector3D(0.0, -0.1, 0.0),
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            container=box
        )
        balls = BallCollection()
        balls.add_list([b1, b2])
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

    elif nexample == 1:
        box = Cuboid3D(xmin=-8, xmax=8)
        balls = random_balls_in_empty_container(
            container=box,
            nballs=50,
            random_speed=0.05,
            rgbcolor='random',
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

    elif nexample == 2:
        xmin = -8
        xmax = 8
        box1 = Cuboid3D(xmin=xmin, xmax=0)
        box2 = Cuboid3D(xmin=0, xmax=xmax)
        box = Cuboid3D(xmin=xmin, xmax=xmax)
        balls1 = random_balls_in_empty_container(
            container=box1,
            nballs=50,
            random_speed=0.05,
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            debug=False
        )
        balls2 = random_balls_in_empty_container(
            container=box2,
            nballs=20,
            random_speed=0.01,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            debug=False
        )
        balls = balls1 + balls2
        dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=False
        )
        for idball in balls.dict:
            b = balls.dict[idball]
            b.container = box
        dict_snapshots = run_simulation(
            dict_snapshots=dict_snapshots,
            balls=balls,
            time_interval=1000,
            debug=False
        )
        time_rendering(
            dict_snapshots=dict_snapshots,
            container=box,
            tstep=1.0,
            outfilename=args.output,
            debug=True
        )

    else:
        print('ERROR: undefined example number')


if __name__ == "__main__":

    main()
