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

from .container3D import Container3D, Cuboid3D


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
        xval = [dict_snapshots[t].dict[i].position.x for t in dict_snapshots]
        yval = [dict_snapshots[t].dict[i].position.y for t in dict_snapshots]
        zval = [dict_snapshots[t].dict[i].position.z for t in dict_snapshots]
        f = interp1d(tvalues, np.array((xval, yval, zval)))
        finterp_balls.append(f)

    print(f'Creating: {outfilename}')
    f = open(outfilename, 'wt')

    f.write("""
<!DOCTYPE html>
<html>
<head>
<title>Elastic Collisions in 3D</title>
<meta charset=utf-8>
<meta name=viewport content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
<meta name=author content="Paul Masson (modified by Nicolas Cardiel)">
<style>
        body { margin: 0px; overflow: hidden; }
        #display { position: absolute; margin: .25in; color: white; font-size: 20pt; }
</style>
</head>

<body>

<div id=display>
<i>E</i> = <span id=d1></span><br>
&Delta;<i>E</i> = <span id=d2></span><br>
Frame = <span id=d3></span>
</div>

<!-- See https://exploratoria.github.io/exhibits/mechanics/elastic-collisions-in-3d/ -->
<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r100/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r100/examples/js/controls/OrbitControls.js"></script>
""")

    f.write(f"""
<script>

        var deg2rad = Math.PI/180;

        // camera location
        var camera_phi = {camera_phi}; 
        var camera_theta = {camera_theta} * deg2rad;
        var delta_camera_phi = 0;
        var camera_r = {camera_r};
        // ligth location
        var lightx = -5;
        var lighty = 5;
        var lightz = 0;
""")

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

    print(f'- Defining balls')
    f.write(f"""
        // ---------------------------
        
        var count = {nballs};
        var balls = [];
""")

    for i in range(nballs):
        b = dict_snapshots[0].dict[i]
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

    f.write(f"""
        // ---------------------------

        var nframe = -{ndelay_start};
""")

    f.write("""
        function render() {
                requestAnimationFrame( render );
                renderer.render( scene, camera );

                nframe = nframe + 1;

                // ---

                if ( nframe <= 0 ) { 
                    // nothing
                };
""")

    print('- Creating frames')

    for k in tqdm(range(len(tarray))):
        t = tarray[k]
        f.write(f'                if ( nframe == {k + 1} )' + ' {\n')
        for i in range(nballs):
            fball = finterp_balls[i]
            fvalues = fball(t)
            f.write(f'                    balls[{i}].position.set( {fvalues[0]}, {fvalues[1]}, {fvalues[2]} );\n')
        f.write('                }\n')

    f.write("""
                // ---

                var kinetic1 = 0;
                var kinetic2 = 0;
                for ( var i = 0 ; i < count ; i++ ) {
                        var b = balls[i];
                        kinetic1 = kinetic1 + 0.5 * b.mass * ( b.v.x * b.v.x + b.v.y * b.v.y + b.v.z * b.v.z );
                        kinetic2 = kinetic2 + 0.5 * b.mass * ( b.v.length() * b.v.length() );
                }
                d1.innerHTML = kinetic1.toFixed(8);
                d2.innerHTML = kinetic2.toString();
                d3.innerHTML = nframe.toString();

        }

        render();

""")

    f.write("""
</script>

</body>
</html>
""")
    f.close()
