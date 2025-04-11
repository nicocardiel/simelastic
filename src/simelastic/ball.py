# -*- coding: utf-8 -*-
#
# Copyright 2023-2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

import copy
import math
import numpy as np

from .container3D import Container3D, Cuboid3D
from .vector3D import Vector3D

from .default_parameters import DEFAULT_BALL_RADIUS


class Ball:
    def __init__(
            self,
            position=None,
            velocity=None,
            radius=None,
            mass=None,
            rgbcolor=None,
            container=None,
            check_within_container=True
    ):
        if position is None:
            self.position = Vector3D()
        elif isinstance(position, Vector3D):
            self.position = position
        else:
            raise ValueError(f'position={position} is not a Vector3D instance')

        if velocity is None:
            self.velocity = Vector3D()
        elif isinstance(velocity, Vector3D):
            self.velocity = velocity
        else:
            raise ValueError(f'velocity={velocity} is not a Vector3D instance')

        if radius is None:
            self.radius = DEFAULT_BALL_RADIUS
        else:
            self.radius = radius

        if mass is None:
            self.mass = 1.0
        else:
            self.mass = mass

        if rgbcolor is None:
            self.rgbcolor = Vector3D(1, 0, 0)
        elif isinstance(rgbcolor, Vector3D):
            self.rgbcolor = rgbcolor
        else:
            raise ValueError(f'rgbcolor={rgbcolor} is not a Vector3D instance')

        if container is None:
            container = Cuboid3D()
        elif isinstance(container, Container3D):
            pass
        else:
            raise ValueError(f'container={container} is not a Container3D instance')

        # check ball fits within container
        if check_within_container:
            if container.can_host_ball(self.position, self.radius):
                self.container = container
            else:
                raise ValueError(f'new ball with position: {repr(self.position)} ' +
                                 f'and radius: {self.radius} ' +
                                 f'outside container={repr(container)}')
        else:
            self.container = container

    def __str__(self):
        output = '<Ball instance>\n'
        output += f'    position = {repr(self.position)}\n'
        output += f'    velocity = {repr(self.velocity)}\n'
        output += f'    radius = {self.radius}\n'
        output += f'    mass = {self.mass}\n'
        output += f'    rgbcolor = {repr(self.rgbcolor)},\n'
        output += f'    container = {repr(self.container)}'
        return output

    def __repr__(self):
        output = f'Ball(\n'
        output += f'    position = {repr(self.position)},\n'
        output += f'    velocity = {repr(self.velocity)},\n'
        output += f'    radius = {self.radius},\n'
        output += f'    mass = {self.mass},\n'
        output += f'    rgbcolor = {repr(self.rgbcolor)},\n'
        output += f'    container = {repr(self.container)}\n'
        output += ')'
        return output

    def distance2ball(self, newball):
        dist = math.sqrt(
            (self.position.x - newball.position.x) ** 2 +
            (self.position.y - newball.position.y) ** 2 +
            (self.position.z - newball.position.z) ** 2
        )
        return dist

    def collision_with_container(self):
        return self.container.collision_with_container(self)

    def update_position(self, t, nround=12):
        self.position.x = np.round(self.position.x + self.velocity.x * t, nround)
        self.position.y = np.round(self.position.y + self.velocity.y * t, nround)
        self.position.z = np.round(self.position.z + self.velocity.z * t, nround)

    def time_to_collision_with_ball(self, newball, nround=12):
        vx_relative = self.velocity.x - newball.velocity.x
        vy_relative = self.velocity.y - newball.velocity.y
        vz_relative = self.velocity.z - newball.velocity.z
        if (vx_relative == 0) and (vy_relative == 0) and (vz_relative == 0):
            tmin = np.inf
        else:
            delta_x = self.position.x - newball.position.x
            delta_y = self.position.y - newball.position.y
            delta_z = self.position.z - newball.position.z
            dcol = self.radius + newball.radius
            a = vx_relative ** 2 + vy_relative ** 2 + vz_relative ** 2
            b = 2 * delta_x * vx_relative + \
                2 * delta_y * vy_relative + \
                2 * delta_z * vz_relative
            c = delta_x ** 2 + delta_y ** 2 + delta_z ** 2 - dcol ** 2
            delta = b * b - 4 * a * c
            if delta <= 0:
                tmin = np.inf
            else:
                tmin1 = (-b + math.sqrt(delta)) / (2 * a)
                if tmin1 < 0:
                    tmin1 = np.inf
                tmin2 = (-b - math.sqrt(delta)) / (2 * a)
                if tmin2 < 0:
                    tmin2 = np.inf
                tmin = np.min([tmin1, tmin2])
                derivative = 2 * a * tmin + b
                if derivative >= 0:
                    tmin = np.inf
        return np.round(tmin, nround)

    def update_collision_with(self, newball, nround=12):
        delta_x = self.position.x - newball.position.x
        delta_y = self.position.y - newball.position.y
        delta_z = self.position.z - newball.position.z
        vx_relative = self.velocity.x - newball.velocity.x
        vy_relative = self.velocity.y - newball.velocity.y
        vz_relative = self.velocity.z - newball.velocity.z
        relativeposition12 = Vector3D(delta_x, delta_y, delta_z)
        relativevelocity12 = Vector3D(vx_relative, vy_relative, vz_relative)
        dotnum = relativeposition12.dot(relativevelocity12)
        dotden = relativeposition12.dot(relativeposition12)
        factor = dotnum / dotden
        corr1 = 2 * newball.mass / (self.mass + newball.mass) * factor
        corr2 = -2 * self.mass / (self.mass + newball.mass) * factor
        self.velocity.x = np.round(self.velocity.x - corr1 * delta_x, nround)
        self.velocity.y = np.round(self.velocity.y - corr1 * delta_y, nround)
        self.velocity.z = np.round(self.velocity.z - corr1 * delta_z, nround)
        newball.velocity.x = np.round(newball.velocity.x - corr2 * delta_x, nround)
        newball.velocity.y = np.round(newball.velocity.y - corr2 * delta_y, nround)
        newball.velocity.z = np.round(newball.velocity.z - corr2 * delta_z, nround)


class BallCollection:
    def __init__(self):
        self.nballs = 0
        self.dict = dict()

    def __str__(self):
        output = '<BallCollection instance>\n'
        output += f'    nballs = {self.nballs}'
        return output

    def __add__(self, bc):
        if isinstance(bc, BallCollection):
            nballs_bc = bc.nballs
            if nballs_bc == 0:
                return self
            for i in range(nballs_bc):
                newball = bc.dict[i]
                if self.check_ball_overlap(newball, warning=True):
                    self.dict[self.nballs] = copy.deepcopy(newball)
                    self.nballs += 1
                else:
                    raise ValueError('Overlap between balls')
        elif isinstance(bc, Ball):
            if self.check_ball_overlap(bc, warning=True):
                self.dict[self.nballs] = copy.deepcopy(bc)
                self.nballs += 1
        else:
            raise ValueError(f'bc: {type(bc)} is not a BallCollection instance')
        return self

    def add_single(self, newball, warning=True):
        if not isinstance(newball, Ball):
            raise ValueError(f'newball: {newball} is not a Ball instance')
        if self.check_ball_overlap(newball, warning=warning):
            self.dict[self.nballs] = copy.deepcopy(newball)
            self.nballs += 1
            return True
        else:
            return False

    def add_list(self, ball_list):
        if not isinstance(ball_list, list):
            raise ValueError(f'ball_list: {ball_list} is not a list')
        for newball in ball_list:
            if not isinstance(newball, Ball):
                raise ValueError(f'newball: {newball} is not a Ball instance')
            if self.check_ball_overlap(newball):
                self.dict[self.nballs] = copy.deepcopy(newball)
                self.nballs += 1

    def check_ball_overlap(self, newball, warning=True):
        if self.nballs == 0:
            return True
        for idball in self.dict:
            b = self.dict[idball]
            if b.distance2ball(newball) < b.radius + newball.radius:
                if warning:
                    print(f'newball: {repr(newball)} ' +
                          f'overlaps with previous ball #{idball}: {repr(b)}')
                return False
        return True
