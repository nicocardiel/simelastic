import numpy as np

from .ball import Ball, BallCollection
from .container3D import Container3D

from .ball import DEFAULT_BALL_RADIUS


def random_balls_in_empty_container(container, nballs=1, radius=None, seed=1234, debug=False):
    if not isinstance(container, Container3D):
        raise ValueError(f'container: {container} is not a Container3D instance')

    rng = np.random.default_rng(seed)

    if radius is None:
        radius = DEFAULT_BALL_RADIUS

    balls = BallCollection()
    nb = 0
    ntrials = 0
    while nb < nballs:
        position = container.new_xyz_for_ball(rng)
        b = Ball(position=position, radius=radius, container=container)
        ntrials += 1
        if debug:
            print(f'Inserting ball #{nb} (trial#{ntrials})')
        if balls.add_single(b, warning=False):
            nb += 1
            ntrials = 0
        if ntrials > 10 * nballs:
            raise ValueError('Too many attempts to insert ball within container')

    return balls
