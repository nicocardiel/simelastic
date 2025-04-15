# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_camera(f, fcamera):
    """
    Write the camera configuration in the HTML file.
    """

    camera_phi, camera_theta, camera_r, camera_lookat_x, camera_lookat_y, camera_lookat_z = fcamera
    
    f.write(f"""
<script>

        var deg2rad = Math.PI/180;

        // camera location
        var camera_phi = {camera_phi} * deg2rad; 
        var camera_theta = {camera_theta} * deg2rad;
        var camera_r = {camera_r};
        // ligth location
        var lightx = -5;
        var lighty = 5;
        var lightz = 0;
""")