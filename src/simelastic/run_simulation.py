import copy
import numpy as np
import sys

from .ball import BallCollection


def run_simulation(
        dict_snapshots=None,
        balls=None,
        time_interval=None,
        time_resolution=100,
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

    # main loop
    while ttotal < tstart + time_interval:
        if debug:
            print(50 * '-')

        # collision with container: minimum time to next collision
        # of any ball with the container walls; several balls can hit
        # the walls at the same minimum time
        tmp_container_tmin = []
        tmp_container_balls = []
        for i in range(nballs):
            b = balls.dict[i]
            tmin, b_after_collision_with_container = b.collision_with_container()
            if debug:
                print(i, tmin)
            tmp_container_tmin.append(tmin)
            tmp_container_balls.append(b_after_collision_with_container)
        tmp_container_tmin = np.array(tmp_container_tmin)
        tmin_container = tmp_container_tmin.min()

        # next collision with another ball
        tmp_dict_t_ij = dict()
        if nballs > 1:
            for i in range(nballs):
                b1 = balls.dict[i]
                for j in range(i + 1, nballs):
                    b2 = balls.dict[j]
                    tmin = b1.time_to_collision_with_ball(b2)
                    tmp_dict_t_ij[tmin] = (i, j)
                    if debug:
                        print(i, j, tmin)
        if debug:
            print(tmp_dict_t_ij)
        tmp_t_keys = np.array([tdum for tdum in tmp_dict_t_ij.keys()])
        tmin_ball_ball = tmp_t_keys.min()

        # next event: collision with container or with another ball?
        if debug:
            print(f'Time to next collision with wall: {tmin_container}')
            print(f'Time to next ball-ball collision: {tmin_ball_ball}')

        if np.isinf(tmin_container) and np.isinf(tmin_ball_ball):
            break

        if tmin_container <= tmin_ball_ball:
            tmin = tmin_container
            affected_balls = np.argwhere(np.array(tmp_container_tmin) <= tmin).flatten()
            if debug:
                print(f'tmin: {tmin}')
                print(f'ball-wall collision -> affected_balls: {affected_balls}')

            for i in balls.dict:
                if i in affected_balls:
                    if debug:
                        print(f'Computing collision of ball {i} with wall')
                        print(balls.dict[i])
                    balls.dict[i] = tmp_container_balls[i]
                    if debug:
                        print(50 * '.')
                        print(balls.dict[i])
                else:
                    balls.dict[i].update_position(tmin)
        else:
            tmin = tmin_ball_ball
            # update location of all balls
            for i in balls.dict:
                if debug:
                    print(f'Updating position of ball {i} after time {tmin}')
                    print(balls.dict[i])
                balls.dict[i].update_position(tmin)
                if debug:
                    print(balls.dict[i])
            # update colliding balls
            ii, jj = tmp_dict_t_ij[tmin]
            if debug:
                print(f'tmin: {tmin}')
                print(f'Computing collision of ball {ii} with ball {jj}')
            b1 = balls.dict[ii]
            b2 = balls.dict[jj]
            if debug:
                print(b1)
                print(b2)
            b1.update_collision_with(b2)
            if debug:
                print(50 * '.')
                print(b1)
                print(b2)

        # print(balls.dict)

        ttotal += tmin

        if debug:
            print(f'ttotal: {ttotal}')
            input('Stop here!')

        itime = int(ttotal * time_resolution + 0.5)
        dict_snapshots[itime] = copy.deepcopy(balls)
        if not debug:
            sys.stdout.write(f'\ritime: {itime / time_resolution}')
            sys.stdout.flush()

    print(' ')

    return dict_snapshots
