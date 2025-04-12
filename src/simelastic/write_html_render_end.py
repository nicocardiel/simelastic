# -*- coding: utf-8 -*-
#
# Copyright 2025 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_html_render_end(f):
    """
    Write the end of the HTML file.
    """
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