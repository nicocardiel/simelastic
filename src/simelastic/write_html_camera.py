# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_camera(f, fcamera, outtype=None):
    """
    Write the camera configuration in the HTML file.
    """

    if outtype is None:
        raise ValueError(f'Undefined outtype')
    
    camera_phi, camera_theta, camera_r, camera_lookat_x, camera_lookat_y, camera_lookat_z = fcamera
    
    f.write(f"""<script>

        var deg2rad = Math.PI/180;

        // ---------------------------

        var renderer = new THREE.WebGLRenderer( {{ antialias: true }} );
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setClearColor( 0x000000, 1 );
        document.body.appendChild( renderer.domElement );

        var camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 100 );
        camera.up.set( 0, 0, 1 );
        var camera_x = {camera_r} * Math.cos({camera_phi} * deg2rad) * Math.cos({camera_theta} * deg2rad)
        var camera_y = {camera_r} * Math.sin({camera_phi} * deg2rad) * Math.cos({camera_theta} * deg2rad)
        var camera_z = {camera_r} * Math.sin({camera_theta} * deg2rad)
        camera.position.set( camera_x, camera_y, camera_z );
        camera.lookAt( {camera_lookat_x}, {camera_lookat_y}, {camera_lookat_z} );
""")
    
    if outtype == 'html':
        f.write("""
        var controls = new THREE.OrbitControls( camera, renderer.domElement );

        window.addEventListener( 'resize', function() {
                renderer.setSize( window.innerWidth, window.innerHeight );
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
        } );
 
""")