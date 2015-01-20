"""
Functions for creating tables of contents.
"""

import markdown
import markdownship.file as file
from os import path, listdir, walk

def create(root_path, website=False, level=0, prepend_path="", debug=False):
  """Returns tables of contents for files under root directory as html."""
  html = level*"  " + "<ul>\n"
  indent = level * '  '
  list_dirs = sorted(
    [x for x in listdir(root_path) if path.isdir(path.join(root_path,x))])
  list_files = sorted(
    [x for x in listdir(root_path) if path.isfile(path.join(root_path,x))\
    and file.is_markdown(x) \
    and path.splitext(path.basename(x))[0] != "index" ])
  for f in list_files:
    link_path = path.join(prepend_path, path.splitext(f)[0]+".html")
    link_name = path.splitext(f)[0]
    link = '<a href="' + link_path + '">' + link_name + '</a>'
    html += indent + '  <li>' + link + '</li>\n'
  for d in list_dirs:
    link=""
    if website:
      link_path = path.join(prepend_path, d)
      link_name = d
    else:
      link_path = path.join(prepend_path, d, "index.html")
      link_name = d
    link = '<a href="' + link_path + '">' + link_name + '</a>'
    html += indent + '  <li>\n'
    html += indent + '  ' + link + '\n'
    html += create(
      path.join(root_path, d),
      website,
      level+1,
      path.join(prepend_path, d),
      debug )
    html += indent + '  </li>\n'
  html += indent + "</ul>\n"
  if debug:
    print "  -- create toc"
    print "     root_path    : " + str(level)
    print "     level        : " + str(level)
    print "     website      : " + str(website)
    print "     prepend_path : " + str(prepend_path)
    print "     list_dirs    :", list_dirs
    print "     list_files   :", list_files
  return html


