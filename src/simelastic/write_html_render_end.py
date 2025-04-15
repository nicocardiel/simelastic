# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_render_end(f, nframe=None, outtype=None):
    """
    Write the end of the HTML file.
    """
    if outtype is None:
        raise ValueError(f'Undefined outtype')
    
    if outtype == 'html':
            f.write("""
                // ---

                var kinetic1 = 0;
                var kinetic2 = 0;
                if ( count > 0 ) {
                        for ( var i = 0 ; i < count ; i++ ) {
                                var b = balls[i];
                                kinetic1 = kinetic1 + 0.5 * b.mass * ( b.v.x * b.v.x + b.v.y * b.v.y + b.v.z * b.v.z );
                                kinetic2 = kinetic2 + 0.5 * b.mass * ( b.v.length() * b.v.length() );
                        }
                }
                disp_e.innerHTML = kinetic1.toFixed(8);
                disp_delta_e.innerHTML = kinetic2.toFixed(8);
                disp_nframe.innerHTML = nframe.toString();
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
        if nframe is None:
            raise ValueError(f'Undefined nframe')
        
        f.write("""        
        // ---

        renderer.render(scene, camera);

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
""")
        f.write(f"""
        var nframe = {nframe};
        d3.innerHTML = nframe.toString();
""")

    f.write("""
</script>

</body>
</html>
""")