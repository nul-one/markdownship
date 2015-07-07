"""
Functions for converting markdown data and files to html format.
"""

import markdown
from markdownship import config, afile
from os import path, makedirs, walk


def to_html(mkd, debug=False):
    """Convert markdown data string to html div."""
    unicode_mkd = unicode(mkd)
    mkd_html = markdown.markdown(
        unicode_mkd,
        extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.codehilite',
            'markdown.extensions.footnotes',
            'markdown.extensions.toc',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite(guess_lang=False)',
            ]
    )
    return mkd_html


def afile_to_html(
        mkd_afile=None,
        html_afile=None,
        template=None,
        toc_data="",
        header_data="",
        footer_data="",
        url="",
        dummy=False,
        debug=False ):
    """Convert markdown file to html file."""
    if debug:
        if not dummy:
            print "-- converting:", mkd_afile.path, "to", html_afile.path
        else:
            print "-- dummy converting:", html_afile.path
            
    html=""
    mkd_data=""
    html_data=""
    if not dummy:
        mkd_data = mkd_afile.read()
    if not html_afile:
        html_name = mkd_afile.getbasename()+".html"
        html_afile = afile(path.join(path.curdir, html_name))
    html_data = to_html(
        mkd=mkd_data,
        debug=debug ) or ""
    html_data = "<div id='markdown'>\n" + html_data + "\n</div>\n"
    html = template.replace(config.markdown_tag, html_data)
    html = html.replace(config.header_tag, header_data)
    html = html.replace(config.footer_tag, footer_data)
    html = html.replace(config.toc_tag, toc_data)
    html = html.replace(config.url_tag, url)
    html = html.replace(config.data_tag, url+'/'+config.data_dir)
    if html_afile:
        html_afile.write(html)
    else:
        return html


def tree_to_html(
        source_path,
        target_path=None,
        template=None,
        toc_data=None,
        header_data=None,
        footer_data=None,
        url=None,
        debug=False ):
    """Convert markdown files under source_path to html files in target_path.
    """
    #TODO: fix circular dependency
    from markdownship import toc
    if debug:
        print "Converting", source_path, "dir to", target_path
    for mkd_afile in afile.find_mkd(source_path):
        mkd_relative_path = mkd_afile.relativepath(source_path)
        html_relative_path = path.splitext(mkd_relative_path)[0]+".html"
        html_file_path = path.join(target_path, html_relative_path)

        custom_toc_data = None
        custom_toc_afile = \
          afile( path.join(mkd_afile.getdir(), config.custom_toc_file_name) )
        try:
            if debug:
                print "Creating custom toc from:", custom_toc_afile.path
                print "    for:", mkd_afile.path
            custom_toc_data = \
                toc.create_from_afile(custom_toc_afile, debug=debug)
        except:
            if debug:
                print "Failed custom toc from: " + custom_toc_afile.path
        if custom_toc_data is not None:
            final_toc_data = custom_toc_data
        else:
            final_toc_data = toc_data
        afile_to_html(
            #mkd_file = path.join(source_path,mkd_file),
            mkd_afile = mkd_afile,
            html_afile = afile(html_file_path),
            template = template,
            toc_data = final_toc_data,
            header_data = header_data,
            footer_data = footer_data,
            url = url,
            debug = debug )
    if debug:
        print "Done"
        print ""


def add_missing_toc(
        target_path,
        template,
        toc_data=None,
        header_data="",
        footer_data="",
        url="",
        debug=False ):
    """Add missing index file for every dir under target_path.
    """
    if debug:
        print "Adding missing index (toc) files"
    for root, dirs, files in walk(target_path):
        for d in dirs:
            toc_dir = path.join(root, d)
            html_afile = afile(path.join(toc_dir, "index.html"))
            if debug:
                print "--", html_afile.path
            afile_to_html(
                html_afile=html_afile,
                template=template,
                toc_data=toc_data,
                url=url,
                header_data=header_data,
                footer_data=footer_data,
                dummy=True,
                debug=debug )
    if debug:
        print "Done"
        print ""


def create_dirs(
        source_path,
        target_path,
        debug=False ):
    """Create directory structure of html to reflect markdown dir structure.
    """
    if debug:
        print "Adding missing dirs"
    for root, dirs, files in walk(source_path):
        for d in dirs:
            usefull_path = afile(path.join(root, d)).relativepath(source_path)
            target_path = path.join(target_path, usefull_path)
            if not path.exists(target_path):
                if debug:
                    print "-- making dir:", target_path
                makedirs(target_path)
    if debug:
        print "Done"
        print ""


