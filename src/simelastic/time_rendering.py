# -*- coding: utf-8 -*-
#
# Copyright 2023 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

import numpy as np
from scipy.interpolate import interp1d
from tqdm import tqdm

from .container3D import Container3D
from .write_html_ball_definition import write_html_ball_definition
from .write_html_camera import write_html_camera
from .write_html_container import write_html_container
from .write_html_header import write_html_header
from .write_html_render_start import write_html_render_start
from .write_html_render_end import write_html_render_end
from .write_html_scene import write_html_scene


def time_rendering(
        dict_snapshots=None,
        container=None,
        tmin=None,
        tmax=None,
        tstep=1,
        ndelay_start=500,
        outfilename=None,
        camera_phi=45,
        camera_theta=30,
        camera_r=25,
        debug=False
):
    if not isinstance(dict_snapshots, dict):
        raise ValueError(f'dict_snapshots: {dict_snapshots} is not a Python dictionary')
    if not isinstance(container, Container3D):
        raise ValueError(f'container: {container} is not a Container3D instance')
    if outfilename is None:
        raise ValueError(f'Undefined outfilename')
    if tstep is None:
        raise ValueError(f'Undefined tstep')

    tvalues = np.array([t for t in dict_snapshots.keys()])
    if debug:
        print(f'Number of frames in dict_snapshots: {len(tvalues)}')

    if tmin is None:
        tmin = min(tvalues)
    if tmax is None:
        tmax = max(tvalues)
    tarray = np.arange(tmin, tmax, tstep)

    if debug:
        print(f'tmin............: {tmin}')
        print(f'tmax............: {tmax}')
        print(f'tstep...........: {tstep}')
        print(f'number of frames: {len(tarray)}')

    nballs = dict_snapshots[tmin].nballs

    finterp_balls = []

    for i in range(nballs):
        # ball posistion
        xval = [dict_snapshots[t].dict[i].position.x for t in dict_snapshots]
        yval = [dict_snapshots[t].dict[i].position.y for t in dict_snapshots]
        zval = [dict_snapshots[t].dict[i].position.z for t in dict_snapshots]
        # ball color
        rcol = [dict_snapshots[t].dict[i].rgbcolor.x for t in dict_snapshots]
        gcol = [dict_snapshots[t].dict[i].rgbcolor.y for t in dict_snapshots]
        bcol = [dict_snapshots[t].dict[i].rgbcolor.z for t in dict_snapshots]
        # interpolation function
        f = interp1d(tvalues, np.array((xval, yval, zval, rcol, gcol, bcol)))
        finterp_balls.append(f)

    print(f'Creating: {outfilename}')
    f = open(outfilename, 'wt')

    write_html_header(f)
    write_html_camera(f, camera_phi, camera_theta, camera_r)
    write_html_scene(f)
    write_html_container(f, container)
    print(f'- Defining balls')
    write_html_ball_definition(f, nballs, dict_snapshots)

    write_html_render_start(f, ndelay_start)

    print('- Creating frames')
    for k in tqdm(range(len(tarray))):
        t = tarray[k]
        f.write(f'                if ( nframe == {k + 1} )' + ' {\n')
        for i in range(nballs):
            fball = finterp_balls[i]
            fvalues = fball(t)
            f.write(f'                    balls[{i}].position.set( {fvalues[0]}, {fvalues[1]}, {fvalues[2]} );\n')
            f.write(f'                    balls[{i}].material.color =  new THREE.Color().setRGB( {fvalues[3]}, {fvalues[4]}, {fvalues[5]});\n')
        f.write('                }\n')

    write_html_render_end(f)
    f.close()
