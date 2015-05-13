"""
Functions for creating tables of contents.
"""

import markdown
from markdownship import file, convert, config
from os import path, listdir, walk

header_name = "header"

def create(
        root_path,
        url=None,
        is_local=True,
        data_dir=None,
        level=0,
        prepend_path="",
        debug=False ):
    """Create html header from header.mkd file in data dir."""
    header_html = ""
    data_dir_path = path.join(root_path, data_dir)
    header_mkd_files = sorted([ x for x in file.find_mkd(data_dir_path) \
        if x.startswith(header_name) ])
    if len(header_mkd_files) > 0:
        if len(header_mkd_files) == 1:
            if debug:
                print "Creating header from", header_mkd_path
            header_mkd_path = path.join(data_dir_path, header_mkd_files[0])
            header_file = file.read(header_mkd_path)
            header_html = convert.to_html(header_file)
        else:
            print "Error: more than one header file found."
    if    len(header_mkd_files) != 1:
        if debug:
            print "Creating default header."
        header_html = convert.to_html(config.default_header)
    if header_html:
        header_html = "<div id='header'>\n" + header_html + "\n</div>\n"
    return header_html

