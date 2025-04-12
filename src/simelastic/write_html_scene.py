# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_scene(f):
    """
    Write the scene of the HTML file.
    """
    f.write("""
        // ---------------------------

        var scene = new THREE.Scene();

        var renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setSize( window.innerWidth, window.innerHeight );
        renderer.setClearColor( 0x000000, 1 );
        document.body.appendChild( renderer.domElement );

        var camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 100 );
        camera.up.set( 0, 0, 1 );
        var camera_x = camera_r * Math.cos(camera_phi) * Math.cos(camera_theta)
        var camera_y = camera_r * Math.sin(camera_phi) * Math.cos(camera_theta)
        var camera_z = camera_r * Math.sin(camera_theta)
        camera.position.set( camera_x, camera_y, camera_z );
        camera.lookAt( 0, 0, 0 );

        var controls = new THREE.OrbitControls( camera, renderer.domElement );

        window.addEventListener( 'resize', function() {
                renderer.setSize( window.innerWidth, window.innerHeight );
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
        } );

""")