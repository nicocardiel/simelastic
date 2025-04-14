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
import pickle
import sys

from .ball import Ball, BallCollection
from .container3D import Cuboid3D
from .random_balls_in_container import random_balls_in_empty_container
from .run_simulation import run_simulation
from .time_rendering import time_rendering
from .vector3D import Vector3D
from .version import version


def main():
    """Generate simulation of elastic collisions in 3D space.

    If nexample is 0, a pickle file (previously generated by this program
    is loaded to generate the HTML/mp4 output file.

    If nexample is different from 0, a simulation is generated
    (and saved as a pickle file if requested). 
    
    """
    parser = argparse.ArgumentParser(description=f"Simulation of elastic collisions (version {version})")
    parser.add_argument("-n", "--nexample", help="Example number", type=int, default=0)
    parser.add_argument("-p", "--pickle", help="Input/Output pickle file name", type=str, default="None")
    parser.add_argument("-o", "--output", help="Output HTML/MP4 file name", type=str, default="None")
    parser.add_argument("-t", "--tstep", help="Time step for rendering (default 1.0)", type=float, default=1.0)
    parser.add_argument("--ndelay_start", help="Delay start (default 500)", type=int, default=500)
    parser.add_argument("--debug", help="Debug mode (default False)", action="store_true")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()
        raise SystemExit()

    nexample = args.nexample

    if nexample == 0:
        if args.pickle.lower() == 'none':
            print('ERROR: no input pickle file name provided')
            raise SystemExit()
        if args.output.lower() == 'none':
            print('ERROR: no output HTML or MP4 file name provided')
            raise SystemExit()
        with open(args.pickle, 'rb') as f:
            pickle_object = pickle.load(f)
        print(f'Number of snapshots: {len(pickle_object['dict_snapshots'])}')
        time_rendering(
            dict_snapshots=pickle_object['dict_snapshots'],
            container=pickle_object['container'],
            tstep=args.tstep,
            ndelay_start=args.ndelay_start,
            outfilename=args.output,
            debug=args.debug
        )
        raise SystemExit('End of program')
    else:
        if args.pickle.lower() == 'none' and args.output.lower() == 'none':
            msg = 'ERROR: no output pickle and no output HTML file name provided'
            raise SystemExit(msg)

    dict_snapshots = None
    if nexample == 1:
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
            debug=args.debug
        )

    elif nexample == 2:
        box = Cuboid3D(xmin=-8, xmax=8)
        balls = random_balls_in_empty_container(
            container=box,
            nballs=100,
            random_speed=0.1,
            rgbcolor='random',
            debug=args.debug
        )
        balls.dict[0].rgbcolor = Vector3D(1.0, 0.0, 0.0)
        dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=args.debug
        )

    elif nexample == 3:
        xmin = -8
        xmax = 8
        box1 = Cuboid3D(xmin=xmin, xmax=4)
        box2 = Cuboid3D(xmin=4, xmax=xmax)
        box = Cuboid3D(xmin=xmin, xmax=xmax)
        balls1 = random_balls_in_empty_container(
            container=box1,
            nballs=50,
            random_speed=0.02,
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            debug=args.debug
        )
        balls2 = random_balls_in_empty_container(
            container=box2,
            nballs=20,
            random_speed=0.1,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            debug=args.debug
        )
        balls = balls1 + balls2
        dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=args.debug
        )
        for idball in balls.dict:
            b = balls.dict[idball]
            b.container = box
        dict_snapshots = run_simulation(
            dict_snapshots=dict_snapshots,
            balls=balls,
            time_interval=1000,
            debug=args.debug
        )

    elif nexample == 4:
        xmin = -8
        xmax = 8
        box1 = Cuboid3D(xmin=xmin, xmax=-1, ymin=-2, ymax=2, zmin=-2, zmax=2)
        box2 = Cuboid3D(xmin=-1, xmax=1, ymin=-2, ymax=2, zmin=-2, zmax=2)
        box3 = Cuboid3D(xmin=1, xmax=xmax, ymin=-2, ymax=2, zmin=-2, zmax=2)
        box = Cuboid3D(xmin=xmin, xmax=xmax, ymin=-2, ymax=2, zmin=-2, zmax=2)
        balls1 = random_balls_in_empty_container(
            container=box1,
            nballs=70,
            radius=0.4,
            random_speed=0.00,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            debug=args.debug
        )
        balls2 = random_balls_in_empty_container(
            container=box2,
            nballs=20,
            radius=0.4,
            random_speed=0.10,
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            debug=args.debug
        )
        balls3 = random_balls_in_empty_container(
            container=box3,
            nballs=70,
            radius=0.4,
            random_speed=0.00,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            debug=args.debug
        )
        balls = balls1 + balls2 + balls3
        dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=1000,
            debug=args.debug
        )
        for idball in balls.dict:
            b = balls.dict[idball]
            b.container = box
        dict_snapshots = run_simulation(
            dict_snapshots=dict_snapshots,
            balls=balls,
            time_interval=1000,
            debug=args.debug
        )

    elif nexample == 5:
        xmin = -18
        xmax = 18
        box1 = Cuboid3D(xmin=xmin, xmax=-1, ymin=-1, ymax=1, zmin=-1, zmax=1)
        box2 = Cuboid3D(xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=-1, zmax=1)
        box3 = Cuboid3D(xmin=1, xmax=xmax, ymin=-1, ymax=1, zmin=-1, zmax=1)
        box = Cuboid3D(xmin=xmin, xmax=xmax, ymin=-1, ymax=1, zmin=-1, zmax=1)
        radius = 0.28
        balls1 = random_balls_in_empty_container(
            container=box1,
            nballs=170,
            radius=radius,
            random_speed=0.00,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            rgbcolor_on_speed=Vector3D(0.0, 1.0, 0.0),
            debug=args.debug
        )
        balls2 = random_balls_in_empty_container(
            container=box2,
            nballs=20,
            radius=radius,
            random_speed=0.10,
            rgbcolor=Vector3D(1.0, 0.0, 0.0),
            debug=args.debug
        )
        balls3 = random_balls_in_empty_container(
            container=box3,
            nballs=170,
            radius=radius,
            random_speed=0.00,
            rgbcolor=Vector3D(0.0, 0.0, 1.0),
            rgbcolor_on_speed=Vector3D(0.0, 1.0, 0.0),
            debug=args.debug
        )
        balls = balls1 + balls2 + balls3
        dict_snapshots = run_simulation(
            dict_snapshots=None,
            balls=balls,
            time_interval=20,
            debug=args.debug
        )
        for idball in balls.dict:
            b = balls.dict[idball]
            b.container = box
        dict_snapshots = run_simulation(
            dict_snapshots=dict_snapshots,
            balls=balls,
            time_interval=50,
            debug=args.debug
        )

    else:
        print('ERROR: undefined example number')

    if dict_snapshots is not None:
        print(f'Number of snapshots: {len(dict_snapshots)}')
        if args.pickle.lower() != 'none':
            pickle_object = {'dict_snapshots': dict_snapshots, 'container': box}
            with open(args.pickle, 'wb') as f:
                pickle.dump(pickle_object, f)
            print(f'Pickle file {args.pickle} saved')
        if args.output.lower() != 'none':
            time_rendering(
                dict_snapshots=dict_snapshots,
                container=box,
                tstep=args.tstep,
                outfilename=args.output,
                debug=args.debug
            )

    print('End of program')


if __name__ == "__main__":

    main()
