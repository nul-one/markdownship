"""
Functions for converting markdown data and files to html format.
"""

import markdown
from  markdownship import file
from markdownship import toc
from os import path, walk


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
    mkd_file,
    html_file=None,
    template=None,
    mkd_tag=None,
    toc_tag=None,
    website=False,
    dummy=False,
    debug=False ):
  """Convert markdown file to html file."""
  if debug:
    print "-- converting", mkd_file, "to", html_file
    print "   mkd_file  :", mkd_file
    print "   html_file :", html_file
    print "   mkd_tag   :", mkd_tag
    print "   toc_tag   :", toc_tag
  html=""
  mkd_data=""
  html_data=""
  toc_data=""
  if not dummy:
    mkd_data = file.read(mkd_file)
  if not html_file:
    mkd_name = path.basename(mkd_file)
    html_name = path.splitext(mkd_name)[0]+".html"
    html_file = path.join(path.curdir, html_name)
  html_data = to_html(
    mkd=mkd_data,
    debug=debug ) or ""
  if toc_tag:
    toc_data = toc.create(
      root_path=path.dirname(mkd_file),
      website=website,
      level=0,
      debug=debug ) or ""
  html = template.replace(mkd_tag, html_data)
  html = html.replace(toc_tag, toc_data)
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
    website=False,
    debug=False ):
  """Convert every markdown file under source_path to html file in target_path.
  """
  if not target_path:
    target_path = path.curdir
  for mkd_file in file.find_mkd(source_path):
    html_relative_path = path.splitext(mkd_file)[0]+".html"
    html_file = path.join(target_path, html_relative_path)
    file_to_html(
      mkd_file = path.join(source_path,mkd_file),
      html_file = html_file,
      template = template,
      mkd_tag = mkd_tag,
      toc_tag = toc_tag,
      website = website,
      debug = debug )
    add_missing_toc(
      source_path=source_path,
      target_path=target_path,
      template=template,
      mkd_tag=mkd_tag,
      toc_tag=toc_tag,
      debug=debug )


def add_missing_toc(
    source_path,
    target_path,
    template,
    mkd_tag=None,
    toc_tag=None,
    website=False,
    debug=False ):
  for root, dirs, files in walk(target_path):
    for d in dirs:
      if not path.isfile(path.join(target_path, d, "index.html")):
        file_to_html(
          mkd_file=path.join(source_path, d, "index.mkd"),
          html_file=path.join(target_path, d, "index.html"),
          template=template,
          mkd_tag=mkd_tag,
          toc_tag=toc_tag,
          dummy=True,
          debug=debug )

