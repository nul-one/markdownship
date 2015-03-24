"""
Functions for creating tables of contents.
"""

import markdown
import markdownship.file as file
import markdownship.convert as convert
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
      header_mkd_path = path.join(data_dir_path, header_mkd_files[0])
      header_file = file.read(header_mkd_path)
      header_html = convert.to_html(header_file)
      if debug:
        print "Creating header from", header_mkd_path
      return header_html
    else:
      print "Error: more than one header file found."
  return ""

