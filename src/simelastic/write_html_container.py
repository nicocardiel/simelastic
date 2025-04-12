# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

from .container3D import Cuboid3D

def write_html_container(f, container):
    """
    Write the container configuration in the HTML file.
    """
    if isinstance(container, Cuboid3D):
        xmin = container.xmin
        xmax = container.xmax
        ymin = container.ymin
        ymax = container.ymax
        zmin = container.zmin
        zmax = container.zmax
    else:
        raise ValueError(f'container: {type(container)} not implemented')

    f.write(f"""
        var box = new THREE.Geometry();
        box.vertices.push( new THREE.Vector3( {xmin}, {ymin}, {zmin} ) );
        box.vertices.push( new THREE.Vector3( {xmax}, {ymax}, {zmax} ) );
        var boxMesh = new THREE.Line( box );
        scene.add( new THREE.BoxHelper( boxMesh, 'white' ) );
        
        var light = new THREE.DirectionalLight( 0xffffff, .8 );
        light.position.set( lightx, lighty, lightz );
        camera.add( light );
        scene.add( camera );
        
        var ambient = new THREE.AmbientLight( 0x555555 );
        scene.add( ambient );

""")