class Container3D:
    def __init__(self):
        pass
    
    def can_host_ball(self, position=None, radius=None):
        if not isinstance(position, Vector3D):
            raise ValueError(f'position:{position} is not a Vector3D instance')
        return self._can_host_ball(position, radius)
        
    def collision_with_container(self, ball=None):
        if not isinstance(ball, Ball):
            raise ValueError(f'ball: {ball} is not a Ball instance')
        return self._collision_with_container(ball)


class Cuboid3D(Container3D):
    def __init__(self, xmin=-5, xmax=5, ymin=-5, ymax=5, zmin=-5, zmax=5):
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
     
    def _can_host_ball(self, ball_position, ball_radius):
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
    
    def _collision_with_container(self, ball, nround=12):
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
    
    def _can_host_ball(self, ball_position, ball_radius):
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
    
    def _collision_with_container(self, ball):
        raise ValueError('Still undefined function')
