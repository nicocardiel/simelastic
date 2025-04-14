# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_ball_definition(f, snapshot):
    """
    Write the ball definition in the HTML file.
    """

    nballs = len(snapshot.dict)

    f.write(f"""
        // ---------------------------
        
        var count = {nballs};
        var balls = [];
""")

    for i in range(nballs):
        b = snapshot.dict[i]
        f.write(f"""
        var geometry = new THREE.SphereGeometry( {b.radius}, 36, 36 );
        var material = new THREE.MeshPhongMaterial();
        material.color = new THREE.Color().setRGB( {b.rgbcolor.x}, {b.rgbcolor.y}, {b.rgbcolor.z} );
        var ball = new THREE.Mesh( geometry, material );
        ball.position.set( {b.position.x}, {b.position.y}, {b.position.z} );
        ball.v = new THREE.Vector3( {b.velocity.x}, {b.velocity.y}, {b.velocity.z} );
        ball.radius = {b.radius};
        ball.mass = {b.mass};
        balls.push( ball );
        scene.add( ball );
""")