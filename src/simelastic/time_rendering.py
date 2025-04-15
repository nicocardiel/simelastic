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
import numpy as np
import os
from pathlib import Path
import shutil
import subprocess
from tqdm import tqdm

from .container3D import Container3D
from .write_dummy_js import write_dummy_js
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
        ndelay_start=0,
        outfilename=None,
        fcamera=None,
        dummydir=None,
        debug=False
):
    if not isinstance(dict_snapshots, dict):
        raise ValueError(f'dict_snapshots: {dict_snapshots} is not a Python dictionary')
    if not isinstance(container, Container3D):
        raise ValueError(f'container: {container} is not a Container3D instance')
    if outfilename is None:
        raise ValueError(f'Undefined outfilename')
    else:
        outfilename = Path(outfilename)
        if outfilename.suffix.lower() == '.html':
            outtype = 'html'
        elif outfilename.suffix.lower() == '.mp4':
            outtype = 'mp4'
        else:
            raise ValueError(f'outfilename: {outfilename} is not a HTML or MP4 file')
        print(f'Output file type: {outtype}')
        
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
    nframes = len(tarray)

    print(f'tmin............: {tmin}')
    print(f'tmax............: {tmax}')
    print(f'tstep...........: {tstep}')
    print(f'number of frames: {nframes}')

    # define constant camera values when time functions are not provided
    if fcamera is None:
        def fcamera(t):
            camera_phi = 45
            camera_theta = 30
            camera_r = 25
            camera_lookat_x = 0
            camera_lookat_y = 0
            camera_lookat_z = 0
            return camera_phi, camera_theta, camera_r, camera_lookat_x, camera_lookat_y, camera_lookat_z

    dummykey = list(dict_snapshots.keys())[0]
    nballs = dict_snapshots[dummykey].nballs

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
        # interpolation functions
        fxval = np.interp(tarray, tvalues, xval)
        fyval = np.interp(tarray, tvalues, yval)
        fzval = np.interp(tarray, tvalues, zval)
        frcol = np.interp(tarray, tvalues, rcol)
        fgcol = np.interp(tarray, tvalues, gcol)
        fbcol = np.interp(tarray, tvalues, bcol)
        finterp_balls.append([fxval, fyval, fzval, frcol, fgcol, fbcol])

    if outtype == 'html':
        print(f'Creating HTML output: {outfilename}')
        f = open(outfilename, 'wt')
        write_html_header(f, outtype=outtype)
        write_html_camera(f, fcamera(tmin))
        write_html_scene(f, outtype=outtype)
        write_html_container(f, container)
        print(f'- Defining balls')
        write_html_ball_definition(f, snapshot=dict_snapshots[0])
        write_html_render_start(f, ndelay_start)
        print('- Creating frames')
        for k in tqdm(range(nframes)):
            t = tarray[k]
            f.write(f'                if ( nframe == {k + 1} )' + ' {\n')
            camera_phi, camera_theta, camera_r, camera_lookat_x, camera_lookat_y, camera_lookat_z = fcamera(t)
            f.write(f'                    camera.position.set( {camera_r} * Math.cos( {camera_phi} * deg2rad ) * Math.cos( {camera_theta} * deg2rad ),\n')
            f.write(f'                                         {camera_r} * Math.sin( {camera_phi} * deg2rad ) * Math.cos( {camera_theta} * deg2rad ),\n')
            f.write(f'                                         {camera_r} * Math.sin( {camera_theta} * deg2rad ) );\n')
            f.write(f'                    camera.lookAt( {camera_lookat_x}, {camera_lookat_y}, {camera_lookat_z} );\n')
            f.write(f'                    var frametime = {t};\n')
            f.write('                    disp_time.innerHTML = frametime.toString();')
            for i in range(nballs):
                fxval, fyval, fzval, frcol, fgcol, fbcol = finterp_balls[i]
                f.write(f'                    balls[{i}].position.set( {fxval[k]}, {fyval[k]}, {fzval[k]} );\n')
                f.write(f'                    balls[{i}].material.color =  new THREE.Color().setRGB( {frcol[k]}, {fgcol[k]}, {fbcol[k]});\n')
            f.write('                }\n')
        write_html_render_end(f, outtype=outtype)
        f.close()

    elif outtype == 'mp4':
        # install puppeteer
        command_line_list = ['npm', 'install', 'puppeteer']
        if debug:
            print(f'Installing puppeteer...')
            print(' '.join(command_line_list))
        sp = subprocess.run(command_line_list, capture_output=True, text=True)
        if sp.returncode != 0:
            print(f'Error installing puppeteer: {sp.stderr}')
            raise SystemExit()
        else:
            if debug:
                print(sp.stdout)
                print('Puppeteer installed!')
        # create dummydir
        if dummydir is None:
            dummydir = Path('dummydir')
        else:
            dummydir = Path(f'{dummydir}')
        if dummydir.exists():
            print(f'Directory {dummydir} already exists. All its content will be deleted.')
            rmdir = input('Do you want to continue (y/[n])? ')
            if rmdir.lower() == 'y':
                shutil.rmtree(dummydir)
            else:
                raise SystemExit('End of program')
        os.mkdir(dummydir)
        # generate dummy JavaScript file
        jsfile = Path('./dummy.js')
        write_dummy_js(jsfile=jsfile)
        # renderize each frame
        nzeros = len(str(nframes))
        for k in tqdm(range(nframes)):
            t = tarray[k]
            # generate dummy HTML file
            f = open('dummy.html', 'wt')
            write_html_header(f, outtype=outtype, frameinfo=f'Frame {k}, t={t}')
            write_html_camera(f, fcamera(t))
            write_html_scene(f, outtype=outtype)
            write_html_container(f, container)
            snapshot = copy.deepcopy(dict_snapshots[0])
            for i in range(nballs):
                fxval, fyval, fzval, frcol, fgcol, fbcol = finterp_balls[i]
                b = snapshot.dict[i]
                b.position.x = fxval[k]
                b.position.y = fyval[k]
                b.position.z = fzval[k]
                b.rgbcolor.x = frcol[k]
                b.rgbcolor.y = fgcol[k]
                b.rgbcolor.z = fbcol[k]
            write_html_ball_definition(f, snapshot=snapshot)
            write_html_render_end(f, nframe=k, outtype=outtype)
            f.close()
            # renderize HTML file
            command_line_list = ['node', jsfile.name]
            sp = subprocess.run(command_line_list, capture_output=True, text=True)
            if sp.returncode != 0:
                print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
                raise SystemExit()
            command_line_list = ['mv', 'image.png', f'dummydir/frame_{str(k).zfill(nzeros)}.png']
            sp = subprocess.run(command_line_list, capture_output=True, text=True)
            if sp.returncode != 0:
                print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
                raise SystemExit()
        # create mp4 file
        command_line_list = ['ffmpeg', 
                             '-y',  # overwrite output file
                             '-framerate', '1', 
                             '-i', f'dummydir/frame_%0{nzeros}d.png', 
                             '-vcodec', 'libx264', '-r', '30', '-crf', '0',
                             '-preset', 'veryslow',
                               outfilename.name]
        print(' '.join(command_line_list))
        sp = subprocess.run(command_line_list, capture_output=True, text=True)
        if sp.returncode != 0:
            print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
            raise SystemExit()
        print(f'File {outfilename} created!')

    else:
        raise ValueError(f'outtype: {outtype} is not a HTML or MP4 file')
    