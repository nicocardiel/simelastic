# -*- coding: utf-8 -*-
#
# Copyright 2023-2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

from astropy.io import fits
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


def find_closest_on_the_right_side(x0, x_values, y_values):
    """Find the closest value in x_values that is less than or equal to x0.
    
    This function is necessary because velocities cannot be interpolated.
    If there are not values in x_values that are less than or equal to x0,
    the closest value that is greater than x0 is returned.
    """
    indices = np.where(x_values <= x0)[0]
    if len(indices) == 0:
        indices = np.where(x_values >= x0)[0]
        closest_index = indices[0]
    else:
        closest_index = indices[-1]
    return y_values[closest_index]


def time_rendering(
        dict_snapshots=None,
        container=None,
        tarray=None,
        ndelay_start=0,
        fontsize=20,
        outfilename=None,
        fcamera=None,
        workdir=None,
        width=1600,
        height=900,
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
        
    tvalues = np.array([t for t in dict_snapshots.keys()])
    if debug:
        print(f'Number of frames in dict_snapshots: {len(tvalues)}')

    if tarray is None:
        tmin = min(tvalues)
        tmax = max(tvalues)
        tstep = 1.0
        tarray = np.arange(tmin, tmax + tstep/2, tstep)
    else:
        tmin = tarray[0]
        tmax = tarray[-1]
    nframes = len(tarray)

    print(f'tmin............: {tmin}')
    print(f'tmax............: {tmax}')
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
        # ball position
        xval = [dict_snapshots[t].dict[i].position.x for t in dict_snapshots]
        yval = [dict_snapshots[t].dict[i].position.y for t in dict_snapshots]
        zval = [dict_snapshots[t].dict[i].position.z for t in dict_snapshots]
        # ball velocity
        vxval = [dict_snapshots[t].dict[i].velocity.x for t in dict_snapshots]
        vyval = [dict_snapshots[t].dict[i].velocity.y for t in dict_snapshots]
        vzval = [dict_snapshots[t].dict[i].velocity.z for t in dict_snapshots]
        # ball color
        rcol = [dict_snapshots[t].dict[i].rgbcolor.x for t in dict_snapshots]
        gcol = [dict_snapshots[t].dict[i].rgbcolor.y for t in dict_snapshots]
        bcol = [dict_snapshots[t].dict[i].rgbcolor.z for t in dict_snapshots]
        # interpolated functions
        fxval = np.interp(tarray, tvalues, xval)
        fyval = np.interp(tarray, tvalues, yval)
        fzval = np.interp(tarray, tvalues, zval)
        fvxval = np.array([find_closest_on_the_right_side(value, tvalues, vxval) for value in tarray])
        fvyval = np.array([find_closest_on_the_right_side(value, tvalues, vyval) for value in tarray])
        fvzval = np.array([find_closest_on_the_right_side(value, tvalues, vzval) for value in tarray])
        frcol = np.interp(tarray, tvalues, rcol)
        fgcol = np.interp(tarray, tvalues, gcol)
        fbcol = np.interp(tarray, tvalues, bcol)
        finterp_balls.append([fxval, fyval, fzval, fvxval, fvyval, fvzval, frcol, fgcol, fbcol])

    if outtype == 'html':
        print(f'Creating HTML output: {outfilename}')
        f = open(outfilename, 'wt')
        write_html_header(f, outtype=outtype, fontsize=fontsize)
        write_html_camera(f, fcamera(tmin), outtype=outtype)
        write_html_scene(f)
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
            f.write('                    disp_time.innerHTML = frametime.toFixed(4);')
            for i in range(nballs):
                fxval, fyval, fzval, fvxval, fvyval, fvzval, frcol, fgcol, fbcol = finterp_balls[i]
                f.write(f'                    balls[{i}].position.set( {fxval[k]}, {fyval[k]}, {fzval[k]} );\n')
                f.write(f'                    balls[{i}].material.color =  new THREE.Color().setRGB( {frcol[k]}, {fgcol[k]}, {fbcol[k]});\n')
            f.write('                }\n')
        # camera looking at last position
        f.write(f'                camera.lookAt( {camera_lookat_x}, {camera_lookat_y}, {camera_lookat_z} );\n')
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
        if workdir is None:
            workdir = Path('dummydir')
        else:
            workdir = Path(f'{workdir}')
        if workdir.exists():
            print(f'Directory {workdir} already exists. All its content will be deleted.')
            rmdir = input('Do you want to continue (y/[n])? ')
            if rmdir.lower() == 'y':
                shutil.rmtree(workdir)
            else:
                raise SystemExit('End of program')
        os.mkdir(workdir)
        # generate dummy JavaScript file
        jsfile = Path('./dummy.js')
        write_dummy_js(jsfile=jsfile, width=width, height=height)
        # renderize each frame
        nzeros = len(str(nframes))
        image2d_velocity = np.zeros((nframes, nballs))
        image2d_xpos = np.zeros((nframes, nballs))
        image2d_ypos = np.zeros((nframes, nballs))
        image2d_zpos = np.zeros((nframes, nballs))
        for k in tqdm(range(nframes)):
            t = tarray[k]
            # generate dummy HTML file
            f = open('dummy.html', 'wt')
            write_html_header(f, outtype=outtype, frameinfo=f'Frame {k}, t={t}', fontsize=fontsize)
            write_html_camera(f, fcamera(t), outtype=outtype)
            write_html_scene(f)
            write_html_container(f, container)
            snapshot = copy.deepcopy(dict_snapshots[0])
            for i in range(nballs):
                fxval, fyval, fzval, fvxval, fvyval, fvzval, frcol, fgcol, fbcol = finterp_balls[i]
                b = snapshot.dict[i]
                b.position.x = fxval[k]
                b.position.y = fyval[k]
                b.position.z = fzval[k]
                b.rgbcolor.x = frcol[k]
                b.rgbcolor.y = fgcol[k]
                b.rgbcolor.z = fbcol[k]
                image2d_xpos[k, i] = fxval[k]
                image2d_ypos[k, i] = fyval[k]
                image2d_zpos[k, i] = fzval[k]
                image2d_velocity[k, i] = np.sqrt(fvxval[k]**2 + fvyval[k]**2 + fvzval[k]**2)
            write_html_ball_definition(f, snapshot=snapshot)
            f.write('        // ---\n\n')
            f.write('        renderer.render(scene, camera);\n\n')
            f.write('        // ---\n\n')
            f.write(f'        var nframe = {k};\n')
            f.write('        disp_nframe.innerHTML = nframe.toString();\n')
            camera_phi, camera_theta, camera_r, camera_lookat_x, camera_lookat_y, camera_lookat_z = fcamera(t)
            f.write(f'        var phi = {camera_phi};\n')
            f.write(f'        var theta = {camera_theta};\n')
            f.write(f'        var r = {camera_r};\n')
            f.write(f'        camera.position.set( r * Math.cos( phi * deg2rad) * Math.cos( theta * deg2rad ),\n')
            f.write(f'                             r * Math.sin( phi * deg2rad) * Math.cos( theta * deg2rad ),\n')
            f.write(f'                             r * Math.sin( theta ) );\n')
            f.write(f'        camera.lookAt( {camera_lookat_x}, {camera_lookat_y}, {camera_lookat_z} );\n')
            f.write(f'        var frametime = {t};\n')
            f.write('        disp_time.innerHTML = frametime.toFixed(4);\n')
            f.write('        disp_camera_phi.innerHTML = phi.toFixed(2);\n')
            f.write('        disp_camera_theta.innerHTML = theta.toFixed(2);\n')
            f.write('        disp_camera_r.innerHTML = r.toFixed(4);\n')

            write_html_render_end(f, outtype=outtype)
            f.close()
            # renderize HTML file
            command_line_list = ['node', jsfile.name]
            sp = subprocess.run(command_line_list, capture_output=True, text=True)
            if sp.returncode != 0:
                print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
                raise SystemExit()
            command_line_list = ['mv', 'image.png', f'{workdir}/frame_{str(k).zfill(nzeros)}.png']
            sp = subprocess.run(command_line_list, capture_output=True, text=True)
            if sp.returncode != 0:
                print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
                raise SystemExit()
        # save FITS files with velocities
        print(f'Creating FITS file with velocities: {workdir}/velocities.fits')
        hdu = fits.PrimaryHDU(image2d_velocity)
        hdu.header['NFRAMES'] = (nframes, 'Number of time frames')
        hdu.header['NBALLS'] = (nballs, 'Number of balls')
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(f'{workdir}/velocities.fits', overwrite=True)
        # save FITS files with (X, Y, Z) positions
        print(f'Creating FITS file with X positions: {workdir}/xpositions.fits')
        hdu = fits.PrimaryHDU(image2d_xpos)
        hdu.header['NFRAMES'] = (nframes, 'Number of time frames')
        hdu.header['NBALLS'] = (nballs, 'Number of balls')
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(f'{workdir}/xpositions.fits', overwrite=True)
        print(f'Creating FITS file with Y positions: {workdir}/ypositions.fits')
        hdu = fits.PrimaryHDU(image2d_ypos)
        hdu.header['NFRAMES'] = (nframes, 'Number of time frames')
        hdu.header['NBALLS'] = (nballs, 'Number of balls')
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(f'{workdir}/ypositions.fits', overwrite=True)
        print(f'Creating FITS file with Z positions: {workdir}/zpositions.fits')
        hdu = fits.PrimaryHDU(image2d_zpos)
        hdu.header['NFRAMES'] = (nframes, 'Number of time frames')
        hdu.header['NBALLS'] = (nballs, 'Number of balls')
        hdulist = fits.HDUList([hdu])
        hdulist.writeto(f'{workdir}/zpositions.fits', overwrite=True)
        # create mp4 file
        command_line_list = ['ffmpeg', 
                             '-y',  # overwrite output file
                             '-framerate', '1', 
                             '-i', f'{workdir}/frame_%0{nzeros}d.png', 
                             '-vcodec', 'libx264', '-r', '30', '-crf', '0',
                             '-preset', 'veryslow',
                               outfilename.name]
        print(f'Creating MP4 file: {outfilename.name}')
        print(f"$ {' '.join(command_line_list)}")
        sp = subprocess.run(command_line_list, capture_output=True, text=True)
        if sp.returncode != 0:
            print(f'Error executing {' '.join(command_line_list)}: {sp.stderr}')
            raise SystemExit()
        print(f'File {outfilename} created!')

    else:
        raise ValueError(f'outtype: {outtype} is not a HTML or MP4 file')
    