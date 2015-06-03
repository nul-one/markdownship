"""
Functions for creating tables of contents.
"""

import markdown
from os import path, listdir, walk
from markdownship import config, afile, convert

toc_name = "toc"

def create(
        root_path,
        url=None,
        is_local=True,
        level=0,
        prepend_path="",
        debug=False ):
    """Returns tables of contents for files under root directory as html."""
    html = ""
    if level == 0:
        html = "<div id='toc'>\n"
    html += level * '    ' + "<ul>\n"
    if url and prepend_path is "":
        prepend_path=url
    indent = level * '    '
    list_dirs = sorted(
        [x for x in listdir(root_path) if path.isdir(path.join(root_path,x))\
        and (level != 0 or x != config.data_dir)])
    list_files = sorted(
        [x for x in listdir(root_path) if path.isfile(path.join(root_path,x))\
        and afile(x).is_markdown() \
        and path.splitext(path.basename(x))[0] != "index" ])
    for f in list_files:
        link_path = path.join(prepend_path, path.splitext(f)[0]+".html")
        link_name = path.splitext(f)[0].replace('_',' ')
        link = '<a href="' + link_path + '">' + link_name + '</a>'
        html += indent + '    <li>' + link + '</li>\n'
    for d in list_dirs:
        link=""
        if is_local:
            link_path = path.join(prepend_path, d, "index.html")
            link_name = d.replace('_',' ')
        else:
            link_path = path.join(prepend_path, d)
            link_name = d.replace('_',' ')
        link = '<a href="' + link_path + '">' + link_name + '</a>'
        html += indent + '    <li>\n'
        html += indent + '    ' + link + '\n'
        html += create(
            path.join(root_path, d),
            url=url,
            is_local=is_local,
            level=level+1,
            prepend_path=path.join(prepend_path, d),
            debug = debug )
        html += indent + '    </li>\n'
    html += indent + "</ul>\n"
    if level == 0:
        html += "</div>\n"
    if debug:
        print "Create toc"
        print "    prepend_path : " + str(prepend_path)
        print "    level                : " + str(level)
        print "    url                    : " + str(url)
        print "    list_dirs        :", list_dirs
        print "    list_files     :", list_files
        print ""
    return html



def create_from_data(root_path, debug=False):
    """Create html toc from toc.mkd file in data dir."""
    toc_html = None
    data_dir_path = path.join(root_path, config.data_dir)
    toc_mkd_files = [ x for x in afile.find_mkd(data_dir_path) \
        if x.getbasename() == toc_name ]
    if len(toc_mkd_files) > 0:
        if len(toc_mkd_files) == 1:
            toc_afile = toc_mkd_files[0]
            if debug:
                print "Creating toc from", toc_afile.path
            toc_html = create_from_afile(toc_afile, debug=debug)
        else:
            print "Error: more than one toc file found."
    return toc_html


def create_from_afile(toc_afile, debug=False):
    """Create html toc from custom .mkd afile."""
    toc_html = None
    if debug:
        print "Creating toc from", toc_afile.path
    toc_data = toc_afile.read()
    toc_html = "<div id='toc'>\n" + convert.to_html(toc_data) + "</div>\n"
    return toc_html

        



