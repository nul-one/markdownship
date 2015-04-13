"""
Functions for creating tables of contents.
"""

import markdown
import markdownship.file as file
import markdownship.convert as convert
from os import path, listdir, walk

footer_name = "footer"

def create(
    root_path,
    url=None,
    is_local=True,
    data_dir=None,
    level=0,
    prepend_path="",
    debug=False ):
  """Create html footer from footer.mkd file in data dir."""
  footer_html = ""
  data_dir_path = path.join(root_path, data_dir)
  footer_mkd_files = sorted([ x for x in file.find_mkd(data_dir_path) \
    if x.startswith(footer_name) ])
  if len(footer_mkd_files) > 0:
    if len(footer_mkd_files) == 1:
      footer_mkd_path = path.join(data_dir_path, footer_mkd_files[0])
      footer_file = file.read(footer_mkd_path)
      footer_html = convert.to_html(footer_file)
      if debug:
        print "Creating footer from", footer_mkd_path
      return footer_html
    else:
      print "Error: more than one footer file found."
  return ""

