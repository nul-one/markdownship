"""
Functions for creating tables of contents.
"""

import markdown
from markdownship import config, afile, convert
from os import path, listdir, walk

footer_name = "footer"

def create(
        root_path,
        url=None,
        is_local=True,
        level=0,
        prepend_path="",
        debug=False ):
    """Create html footer from footer.mkd file in data dir."""
    footer_html = ""
    data_dir_path = path.join(root_path, config.data_dir)
    footer_mkd_files = [ x for x in afile.find_mkd(data_dir_path) \
        if x.getbasename() == footer_name ]
    if len(footer_mkd_files) > 0:
        if len(footer_mkd_files) == 1:
            footer_mkd_path = path.join(data_dir_path, footer_mkd_files[0].path)
            if debug:
                print "Creating footer from", footer_mkd_path
            footer_data = afile(footer_mkd_path).read()
            footer_html = convert.to_html(footer_data)
        else:
            print "Error: more than one footer file found."
    if    len(footer_mkd_files) != 1:
        if debug:
            print "Creating default footer."
        footer_html = convert.to_html(config.default_footer)
    if footer_html:
        footer_html = "<div id='footer'>\n" + footer_html + "\n</div>\n"
    return footer_html

