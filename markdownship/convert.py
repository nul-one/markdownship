"""
Functions for converting markdown data and files to html format.
"""

import markdown
from  markdownship import file
from markdownship import toc
from os import path, makedirs, walk


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
    mkd_tag=None,
    toc_tag=None,
    toc_data=None,
    url_tag=None,
    url=None,
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
  html = template.replace(mkd_tag, html_data)
  if toc_data and toc_tag:
    html = html.replace(toc_tag, toc_data)
  if url and url_tag:
    html = html.replace(url_tag, url)
  if html_file:
    file.write(html_file, html)
  else:
    return html


def tree_to_html(
    source_path,
    target_path=None,
    template=None,
    mkd_tag=None,
    toc_tag=None,
    toc_data=None,
    url_tag=None,
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
      mkd_tag = mkd_tag,
      toc_tag = toc_tag,
      toc_data = toc_data,
      url_tag = url_tag,
      url = url,
      debug = debug )
  if debug:
    print "Done"
    print ""


def add_missing_toc(
    target_path,
    template,
    mkd_tag=None,
    toc_tag=None,
    toc_data=None,
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
        mkd_tag=mkd_tag,
        toc_tag=toc_tag,
        toc_data=toc_data,
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
      _, usefull_path = path.split(root[len(source_path):])
      target_dir = path.join(target_path, usefull_path, d)
      if not path.exists(target_dir):
        if debug:
          print "-- making dir:", target_dir
        makedirs(target_dir)
  if debug:
    print "Done"
    print ""


