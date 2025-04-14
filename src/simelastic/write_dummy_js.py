# -*- coding: utf-8 -*-
#
# Copyright 2023 Nicolás Cardiel
#
# This file is part of simelastic
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE
#

def write_dummy_js(jsfile=None):
    """Create a dummy JavaScript file for renderized."""
    if jsfile is None:
        raise ValueError(f'Undefined jsfile')
    
    f = open(jsfile, 'wt')
    f.write("""// renderize HTML file and export result to PNG file
const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 700 }); // Set the desired width and height
""")
    f.write(f"""await page.goto('file://{jsfile.parent.absolute()}/dummy.html'""")
    f.write(""", {waitUntil: 'networkidle2'});
    // console.log(await page.title());
    await page.screenshot({ path: 'image.png' });
    await browser.close();
})();
// end of code""")
    f.close()