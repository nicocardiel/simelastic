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
    
    f.write(f"""
        // ---------------------------

        var scene = new THREE.Scene();
""")
