import copy
import numpy as np
import sys

from .ball import BallCollection


def run_simulation(
        dict_snapshots=None,
        balls=None,
        time_interval=None,
        time_resolution=2,
        debug=False
):
    if not isinstance(balls, BallCollection):
        raise ValueError(f'balls: {balls} is not an instance of BallCollection')
    nballs = balls.nballs

    if dict_snapshots is None:
        dict_snapshots = dict()
        # insert time = 0
        dict_snapshots[0] = copy.deepcopy(balls)
        tstart = 0
    else:
        if not isinstance(dict_snapshots, dict):
            raise ValueError(f'dict_snapshots: {dict_snapshots} is not a Python dictionary')
        tstart = max(dict_snapshots.keys())

    ttotal = tstart

    print(f'Running simulation from time {tstart} to {tstart + time_interval}...')
    # main loop
    while ttotal < tstart + time_interval:
        # collision with container: minimum time to next collision
        # of any ball with the container walls; several balls can hit
        # the walls at the same minimum time
        tmp_container_tmin = []
        tmp_container_balls = []
        for i in range(nballs):
            b = balls.dict[i]
            tmin, b_after_collision_with_container = b.collision_with_container()
            tmp_container_tmin.append(tmin)
            tmp_container_balls.append(b_after_collision_with_container)
        tmp_container_tmin = np.array(tmp_container_tmin)
        tmin_container = min(tmp_container_tmin)

        # next collision with another ball
        tmp_dict_t_ij = dict()
        if nballs > 1:
            for i in range(nballs):
                b1 = balls.dict[i]
                for j in range(i + 1, nballs):
                    b2 = balls.dict[j]
                    tmin = b1.time_to_collision_with_ball(b2)
                    tmp_dict_t_ij[tmin] = (i, j)
        tmp_t_keys = np.array([tdum for tdum in tmp_dict_t_ij.keys()])
        tmin_ball_ball = min(tmp_t_keys)

        # next event: collision with container or with another ball?
        if np.isinf(tmin_container) and np.isinf(tmin_ball_ball):
            break

        if tmin_container <= tmin_ball_ball:
            tmin = tmin_container
            affected_balls = np.argwhere(np.array(tmp_container_tmin) <= tmin).flatten()
            for i in balls.dict:
                if i in affected_balls:
                    balls.dict[i] = tmp_container_balls[i]
                else:
                    balls.dict[i].update_position(tmin)
        else:
            tmin = tmin_ball_ball
            # update location of all balls
            for i in balls.dict:
                balls.dict[i].update_position(tmin)
            # update colliding balls
            ii, jj = tmp_dict_t_ij[tmin]
            b1 = balls.dict[ii]
            b2 = balls.dict[jj]
            b1.update_collision_with(b2)

        ttotal += tmin
        ftime = round(ttotal, time_resolution)
        dict_snapshots[ftime] = copy.deepcopy(balls)
        if not debug:
            sys.stdout.write(f'\rtime: {ftime}')
            sys.stdout.flush()

    if not debug:
        print(' ')

    return dict_snapshots
