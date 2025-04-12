# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_render_start(f, ndelay_start=0):
    """
    Write the start of the HTML file.
    """
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