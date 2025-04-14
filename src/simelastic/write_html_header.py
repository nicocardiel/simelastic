# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_header(f, outtype=None, frameinfo=None):
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
    
    f.write("""<meta charset=utf-8>
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
""")
    if outtype == 'html':
        f.write("""<script src="https://cdn.jsdelivr.net/gh/mrdoob/three.js@r100/examples/js/controls/OrbitControls.js"></script>
""")
