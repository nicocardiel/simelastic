from abc import ABC, abstractmethod
import copy
import math
import numpy as np

from .vector3D import Vector3D

from .default_parameters import DEFAULT_BALL_RADIUS
from .default_parameters import DEFAULT_CUBOID3D_XMIN, DEFAULT_CUBOID3D_XMAX
from .default_parameters import DEFAULT_CUBOID3D_YMIN, DEFAULT_CUBOID3D_YMAX
from .default_parameters import DEFAULT_CUBOID3D_ZMIN, DEFAULT_CUBOID3D_ZMAX
from .default_parameters import DEFAULT_CYLINDER_RADIUS, DEFAULT_CYLINDER_HEIGHT


class Container3D(ABC):

    def __init__(self):
        self.type = None

    @abstractmethod
    def new_xyz_for_ball(self, rng, ball_radius=None):
        raise NotImplementedError("no .new_random_ball method")

    @abstractmethod
    def can_host_ball(self, ball_position=None, ball_radius=None):
        raise NotImplementedError("no .can_host_ball method")

    @abstractmethod
    def collision_with_container(self, ball=None, nround=12):
        raise NotImplementedError("no .collision_with_container method")


class Cuboid3D(Container3D):
    def __init__(
            self,
            xmin=DEFAULT_CUBOID3D_XMIN, xmax=DEFAULT_CUBOID3D_XMAX,
            ymin=DEFAULT_CUBOID3D_YMIN, ymax=DEFAULT_CUBOID3D_YMAX,
            zmin=DEFAULT_CUBOID3D_ZMIN, zmax=DEFAULT_CUBOID3D_ZMAX
    ):
        super().__init__()
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        self.type = 'Cuboid3D'
        
    def __str__(self):
        return f'<{self.type} instance>\n' + \
              f'    xmin = {self.xmin}\n' + \
              f'    xmax = {self.xmax}\n' + \
              f'    ymin = {self.ymin}\n' + \
              f'    ymax = {self.ymax}\n' + \
              f'    zmin = {self.zmin}\n' + \
              f'    zmax = {self.zmax}'
    
    def __repr__(self):
        return f'{self.type}(xmin={self.xmin}, xmax={self.xmax}, ' + \
               f'ymin={self.ymin}, ymax={self.ymax}, ' + \
               f'zmin={self.zmin}, zmax={self.zmax})'

    def new_xyz_for_ball(self, rng, ball_radius=None):
        if ball_radius is None:
            ball_radius = DEFAULT_BALL_RADIUS
        diameter = 2 * ball_radius
        if diameter > self.xmax - self.xmin:
            raise ValueError(f'The ball diameter: {diameter} is larger than the container X size')
        if diameter > self.ymax - self.ymin:
            raise ValueError(f'The ball diameter: {diameter} is larger than the container Y size')
        if diameter > self.zmax - self.zmin:
            raise ValueError(f'The ball diameter: {diameter} is larger than the container Z size')
        x = rng.uniform(self.xmin + ball_radius, self.xmax - ball_radius, 1)[0]
        y = rng.uniform(self.ymin + ball_radius, self.ymax - ball_radius, 1)[0]
        z = rng.uniform(self.zmin + ball_radius, self.zmax - ball_radius, 1)[0]
        return Vector3D(x, y, z)

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
    def __init__(
            self,
            radius=DEFAULT_CYLINDER_RADIUS,
            height=DEFAULT_CYLINDER_HEIGHT,
            base_center_position=Vector3D(0, 0, 0)
    ):
        super().__init__()
        self.radius = radius
        self.height = height
        if isinstance(base_center_position, Vector3D):
            self.base_center_position = base_center_position
        else:
            raise ValueError(f'base_center_position: {base_center_position} is not a Vector3D instance')
        self.type = 'VerticalCylinder3D'
            
    def __str__(self):
        return f'<{self.type} instance>\n' + \
              f'    radius = {self.radius}\n' + \
              f'    height = {self.height}\n' + \
              f'    base_center_position = {self.base_center_position}'
    
    def __repr__(self):
        return f'{self.type}(radius={self.radius}, ' + \
               f'height={self.height}, ' + \
               f'base_center_position={repr(self.base_center_position)})'

    def new_xyz_for_ball(self, rng, ball_radius=None):
        if ball_radius is None:
            ball_radius = DEFAULT_BALL_RADIUS
        if ball_radius > self.radius:
            raise ValueError(f'The ball radius: {ball_radius} does not fit within the cylinder radius: {self.radius}')
        if 2 * ball_radius > self.height:
            raise ValueError(f'The ball diameter: {2 * ball_radius} does not fit ' +
                             f'within the cylinder height: {self.height}')
        loop = True
        x, y = 0, 0   # avoid PyCharm warning
        while loop:
            x = rng.uniform(-self.radius, self.radius, 1)[0]
            y = rng.uniform(-self.radius, self.radius, 1)[0]
            rdist = math.sqrt(x * x + y * y)
            if rdist < self.radius - ball_radius:
                loop = False
        z = rng.uniform(ball_radius, self.height - ball_radius, 1)[0]
        xx = self.base_center_position.x + x
        yy = self.base_center_position.y + y
        zz = self.base_center_position.z + z
        return Vector3D(xx, yy, zz)

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
        raise ValueError('Still undefined function')
