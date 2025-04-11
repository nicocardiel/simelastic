# -*- coding: utf-8 -*-
#
# Copyright 2023 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

import math
import numpy as np

from .ball import Ball, BallCollection
from .container3D import Container3D
from .vector3D import Vector3D

from .ball import DEFAULT_BALL_RADIUS


def random_balls_in_empty_container(
        container=None,
        nballs=1,
        radius=None,
        random_speed=0,
        rgbcolor=None,
        seed=1234,
        debug=False
):
    if not isinstance(container, Container3D):
        raise ValueError(f'container: {container} is not a Container3D instance')

    rng = np.random.default_rng(seed)

    if radius is None:
        radius = DEFAULT_BALL_RADIUS

    balls = BallCollection()
    nb = 0
    ntrials = 0
    vx, vy, vz = 0, 0, 0   # avoid PyCharm warning
    while nb < nballs:
        if (ntrials == 0) and (random_speed > 0):
            phi = rng.uniform(0, 2 * np.pi, 1)[0]
            theta = math.asin(rng.uniform(-1, 1, 1)[0])
            vx = random_speed * math.cos(theta) * math.cos(phi)
            vy = random_speed * math.cos(theta) * math.sin(phi)
            vz = random_speed * math.sin(theta)
        position = container.new_xyz_for_ball(rng, ball_radius=radius)
        velocity = Vector3D(vx, vy, vz)
        if rgbcolor is None:
            rgbcolor = Vector3D(0.8, 0.8, 0.8)
        elif isinstance(rgbcolor, Vector3D):
            pass
        elif isinstance(rgbcolor, str):
            if rgbcolor == 'random':
                rgbcolor = Vector3D(rng.uniform(0, 1, 1)[0],
                                    rng.uniform(0, 1, 1)[0],
                                    rng.uniform(0, 1, 1)[0])
            else:
                raise ValueError(f'Unexpected rgbcolor: {rgbcolor}')
        else:
            raise ValueError(f'Unexpected rgbcolor: {rgbcolor}')
        b = Ball(
            position=position,
            radius=radius,
            velocity=velocity,
            rgbcolor=rgbcolor,
            container=container
        )
        ntrials += 1
        if debug:
            print(f'Inserting ball #{nb} (trial#{ntrials})')
        if balls.add_single(b, warning=False):
            nb += 1
            ntrials = 0
        if ntrials > 100 * nballs:
            raise ValueError('Too many attempts to insert ball within container')

    if not debug:
        print(f'{nballs} balls randomly inserted in empty container {container.type}')

    return balls
