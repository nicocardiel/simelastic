from abc import ABC, abstractmethod
import copy
import math
import numpy as np

from ball import Ball
from vector3D import Vector3D


class Container3D(ABC):

    @abstractmethod
    def can_host_ball(self, ball_position=None, ball_radius=None):
        raise NotImplementedError("no .can_host_ball method")

    @abstractmethod
    def collision_with_container(self, ball=None, nround=12):
        raise NotImplementedError("no .collision_with_container method")


class Cuboid3D(Container3D):
    def __init__(self, xmin=-5, xmax=5, ymin=-5, ymax=5, zmin=-5, zmax=5):
        # super().__init__()
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
    def __str__(self):
        return '<Cuboid3D instance>\n' + \
              f'    xmin = {self.xmin}\n' + \
              f'    xmax = {self.xmax}\n' + \
              f'    ymin = {self.ymin}\n' + \
              f'    ymax = {self.ymax}\n' + \
              f'    zmin = {self.zmin}\n' + \
              f'    zmax = {self.zmax}'
    
    def __repr__(self):
        return f'Cuboid3D(xmin={self.xmin}, xmax={self.xmax}, ' + \
               f'ymin={self.ymin}, ymax={self.ymax}, ' + \
               f'zmin={self.zmin}, zmax={self.zmax})'
     
    def can_host_ball(self, ball_position=None, ball_radius=None):
        if not isinstance(ball_position, Vector3D):
            raise ValueError(f'position:{ball_position} is not a Vector3D instance')
        if ball_radius is None:
            raise ValueError(f'invalid ball radius: {ball_radius}')
        result = True
        if ball_position.x - ball_radius < self.xmin:
            result = False
        else:
            if ball_position.x + ball_radius > self.xmax:
                result = False
            else:
                if ball_position.y - ball_radius < self.ymin:
                    result = False
                else:
                    if ball_position.y + ball_radius > self.ymax:
                        result = False
                    else:
                        if ball_position.z - ball_radius < self.zmin:
                            result = False
                        else:
                            if ball_position.z + ball_radius > self.zmax:
                                result = False                
        return result
    
    def collision_with_container(self, ball=None, nround=12):
        if not isinstance(ball, Ball):
            raise ValueError(f'ball: {ball} is not a Ball instance')
        # collision with wall at x=xmax or x=xmin
        if ball.velocity.x == 0:
            tx = np.infty
        elif ball.velocity.x > 0:
            tx = (self.xmax - ball.radius - ball.position.x) / ball.velocity.x
        else:
            tx = (self.xmin + ball.radius - ball.position.x) / ball.velocity.x
        # collision with wall at y=ymax or y=ymin
        if ball.velocity.y == 0:
            ty = np.infty
        elif ball.velocity.y > 0:
            ty = (self.ymax - ball.radius - ball.position.y) / ball.velocity.y
        else:
            ty = (self.ymin + ball.radius - ball.position.y) / ball.velocity.y
        # collision with wall at z=zmax or z=zmin
        if ball.velocity.z == 0:
            tz = np.infty
        elif ball.velocity.z > 0:
            tz = (self.zmax - ball.radius - ball.position.z) / ball.velocity.z
        else:
            tz = (self.zmin + ball.radius - ball.position.z) / ball.velocity.z
        # time before collision
        tx = np.round(tx, nround)
        ty = np.round(ty, nround)
        tz = np.round(tz, nround)
        tmin = np.min([tx, ty, tz])
        # future ball just after collision
        future_ball = copy.deepcopy(ball)
        if not np.isinf(tmin):
            future_ball.update_position(tmin)
            # reverse velocity accordingly
            if tx == tmin:
                future_ball.velocity.x = -future_ball.velocity.x
            if ty == tmin:
                future_ball.velocity.y = -future_ball.velocity.y
            if tz == tmin:
                future_ball.velocity.z = -future_ball.velocity.z
        return tmin, future_ball


class VerticalCylinder3D(Container3D):
    def __init__(self, radius=5, height=10, base_center_position=Vector3D(0, 0, 0)):
        # super().__init__()
        self.radius = radius
        self.height = height
        if isinstance(base_center_position, Vector3D):
            self.base_center_position = base_center_position
        else:
            raise ValueError(f'base_center_position: {base_center_position} is not a Vector3D instance')
            
    def __str__(self):
        return '<VerticalCylinder3D instance>\n' + \
              f'    radius = {self.radius}\n' + \
              f'    height = {self.height}\n' + \
              f'    base_center_position = {self.base_center_position}'
    
    def __repr__(self):
        return f'VerticalCylinder3D(radius={self.radius}, ' + \
               f'height={self.height}, ' + \
               f'base_center_position={repr(self.base_center_position)})'
    
    def can_host_ball(self, ball_position=None, ball_radius=None):
        if not isinstance(ball_position, Vector3D):
            raise ValueError(f'position: {ball_position} is not a Vector3D instance')
        if ball_radius is None:
            raise ValueError(f'invalid ball radius: {ball_radius}')
        result = True
        if ball_position.z + ball_radius > self.base_center_position.z + self.height:
            result = False
        else:
            if ball_position.z - ball_radius < self.base_center_position.z:
                result = False
            else:
                # distance to cylinder axis
                rdist = math.sqrt(
                    (ball_position.x - self.base_center_position.x)**2 +
                    (ball_position.y - self.base_center_position.y)**2
                )
                if rdist + ball_radius > self.radius:
                    result = False
        return result
    
    def collision_with_container(self, ball=None, nround=12):
        if not isinstance(ball, Ball):
            raise ValueError(f'ball: {ball} is not a Ball instance')
        raise ValueError('Still undefined function')
