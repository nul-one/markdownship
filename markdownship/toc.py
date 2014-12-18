"""
Functions for creating tables of contents.
"""


import markdown
import markdownship.file as file
from markdownship.convert import mkd_to_html
import os

def create(root_path, template=None, mkd_tag=None, debug=False):
  """Creates tables of contents for each directory as index.html file"""
  for path, dirs, files in os.walk(root_path):
    index_mkd = ""
    for d in dirs:
      link = os.path.join(os.path.curdir, os.path.join(d,"index.html"))
      index_mkd += "["+d.upper()+"]("+link+")  \n"
    for f in files:
      if f.lower().endswith(".html") and f != "index.html":
        link = os.path.join(os.path.curdir, os.path.splitext(f)[0]+".html")
        index_mkd += "["+os.path.splitext(f)[0]+"]("+link+")  \n"
    index_html = mkd_to_html(
      index_mkd,
      template = template,
      mkd_tag = mkd_tag,
      debug = debug
      )
    file.write(os.path.join(path, "index.html"), index_html)


