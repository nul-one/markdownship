"""
Functions for converting markdown data and files to html format.
"""

import markdown
from  markdownship import file
from markdownship import toc
from os import path, makedirs, walk
from markdownship import config


def to_html(mkd, debug=False):
  """Convert markdown data string to html string."""
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


def file_to_html(
    mkd_file=None,
    html_file=None,
    template=None,
    toc_data="",
    header_data="",
    footer_data="",
    url="",
    data_dir="",
    dummy=False,
    debug=False ):
  """Convert markdown file to html file."""
  if debug:
    print "-- converting:", mkd_file, "to", html_file
  html=""
  mkd_data=""
  html_data=""
  if not dummy:
    mkd_data = file.read(mkd_file)
  if not html_file:
    mkd_name = path.basename(mkd_file)
    html_name = path.splitext(mkd_name)[0]+".html"
    html_file = path.join(path.curdir, html_name)
  html_data = to_html(
    mkd=mkd_data,
    debug=debug ) or ""
  html = template.replace(config.markdown_tag, html_data)
  html = html.replace(config.header_tag, header_data)
  html = html.replace(config.footer_tag, footer_data)
  html = html.replace(config.toc_tag, toc_data)
  html = html.replace(config.url_tag, url)
  html = html.replace(config.data_tag, url+'/'+data_dir)
  if html_file:
    file.write(html_file, html)
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
    data_dir=None,
    debug=False ):
  """Convert every markdown file under source_path to html file in target_path.
  """
  if debug:
    print "Converting", source_path, "dir to", target_path
  for mkd_file in file.find_mkd(source_path):
    html_relative_path = path.splitext(mkd_file)[0]+".html"
    html_file = path.join(target_path, html_relative_path)
    file_to_html(
      mkd_file = path.join(source_path,mkd_file),
      html_file = html_file,
      template = template,
      toc_data = toc_data,
      header_data = header_data,
      footer_data = footer_data,
      url = url,
      data_dir = data_dir,
      debug = debug )
  if debug:
    print "Done"
    print ""


def add_missing_toc(
    target_path,
    template,
    toc_data=None,
    header_data=None,
    footer_data=None,
    debug=False ):
  """Add missing index file for every dir under target_path.
  """
  if debug:
    print "Adding missing index files"
  for root, dirs, files in walk(target_path):
    for d in dirs:
      target_dir = path.join(root, d)
      html_file = path.join(target_dir, "index.html")
      file_to_html(
        html_file=html_file,
        template=template,
        toc_data=toc_data,
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
      usefull_path = file.relative_path(
        source_path, path.join(root, file.trim_path(d)) )
      target_dir = path.join(target_path, usefull_path)
      if not path.exists(target_dir):
        if debug:
          print "-- making dir:", target_dir
        makedirs(target_dir)
  if debug:
    print "Done"
    print ""


