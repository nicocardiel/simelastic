# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_header(f, outtype=None, frameinfo=None, fontsize=20):
    """
    Write the header of the HTML file.
    """

    if outtype is None:
        raise ValueError(f'Undefined outtype')

    if frameinfo is None:
        frameinfo = ''
    else:
        frameinfo = f' ({frameinfo})'
    f.write(f"""<!DOCTYPE html>
<html>
<head>
<title>Elastic Collisions in 3D{frameinfo}</title>""")
    f.write(f"""<meta charset=utf-8>
<meta name=viewport content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
<meta name=author content="Paul Masson (modified by Nicolas Cardiel)">
<style>
    body {{ margin: 0px; overflow: hidden; }}
    #display_nframe       {{ position: absolute; margin: .25in; left:  0.0in; color: white; font-size: {fontsize}pt; }}
    #display_kinetic      {{ position: absolute; margin: .25in; left:  2.0in; color: white; font-size: {fontsize}pt; }}
    #display_time         {{ position: absolute; margin: .25in; left:  4.0in; color: white; font-size: {fontsize}pt; }}
    #display_camera_phi   {{ position: absolute; margin: .25in; left:  6.0in; color: white; font-size: {fontsize}pt; }}
    #display_camera_theta {{ position: absolute; margin: .25in; left:  8.0in; color: white; font-size: {fontsize}pt; }}
    #display_camera_r     {{ position: absolute; margin: .25in; left: 10.0in; color: white; font-size: {fontsize}pt; }}
</style>
</head>

<body>

<div id=display_nframe>Frame = <span id=disp_nframe></span></div>
<div id=display_kinetic>&Sigma;<i>K</i> = <span id=disp_kinetic></span></div>
<div id=display_time>Time = <span id=disp_time></span></div>
<div id=display_camera_phi>phi = <span id=disp_camera_phi></span></div>
<div id=display_camera_theta>theta = <span id=disp_camera_theta></span></div>
<div id=display_camera_r>r = <span id=disp_camera_r></span></div>

<!-- See https://exploratoria.github.io/exhibits/mechanics/elastic-collisions-in-3d/ -->
<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r100/build/three.min.js"></script>
""")
    
    if outtype == 'html':
        f.write("""<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r100/examples/js/controls/OrbitControls.js"></script>
""")
