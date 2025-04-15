# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_render_end(f, outtype=None):
    """
    Write the end of the HTML file.
    """
    if outtype is None:
        raise ValueError(f'Undefined outtype')
    
    if outtype == 'html':
            f.write("""
                // ---

                var kinetic = 0;
                if ( count > 0 ) {
                        for ( var i = 0 ; i < count ; i++ ) {
                                var b = balls[i];
                                kinetic = kinetic + 0.5 * b.mass * ( b.v.length() * b.v.length() );
                        }
                }
                disp_nframe.innerHTML = nframe.toString();
                disp_kinetic.innerHTML = kinetic.toFixed(4);
                var x = camera.position.x;
                var y = camera.position.y;
                var z = camera.position.z;
                var r = Math.sqrt(x*x + y*y + z*z);
                var theta = Math.asin(z / r) / deg2rad;
                var phi = Math.atan2(y, x) / deg2rad;
                disp_camera_phi.innerHTML = phi.toFixed(2);
                disp_camera_theta.innerHTML = theta.toFixed(2);
                disp_camera_r.innerHTML = r.toFixed(4);

        }

        render();

""")
    else:
        f.write("""
        var kinetic = 0;
        if ( count > 0 ) {
                for ( var i = 0 ; i < count ; i++ ) {
                        var b = balls[i];
                        kinetic = kinetic + 0.5 * b.mass * ( b.v.length() * b.v.length() );
                }
        }
        disp_kinetic.innerHTML = kinetic.toFixed(4);
""")

    f.write("""
</script>

</body>
</html>
""")