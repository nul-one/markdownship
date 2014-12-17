import markdown
import markdownship.file as file
import os

def mkd_to_html(mkd, template=None, mkd_tag=None, debug=False):
  """Convert mkd data to html data."""
  unicode_mkd = unicode(mkd)
  html = markdown.markdown(
    unicode_mkd,
    extensions=[
      'markdown.extensions.tables',
      'markdown.extensions.codehilite',
      'markdown.extensions.footnotes',
      'markdown.extensions.toc',
      ]
  )
  if template and mkd_tag:
    return template.replace(mkd_tag, html)
  else:
    return html
  

def mkd_file_to_html_file(
    mkd_file,
    html_file=None,
    template=None,
    mkd_tag=None,
    debug = False ):
  """Convert mkd file to html file."""
  mkd_data = file.read(mkd_file)
  if not html_file:
    mkd_name = os.path.basename(mkd_file)
    html_name = os.path.splitext(mkd_name)[0]+".html"
    html_file = os.path.join(os.path.curdir, html_name)
  html_data = mkd_to_html(
    mkd_data,
    template = template,
    mkd_tag = mkd_tag
    )
  if debug:
    print "-- converting", mkd_file, "to", html_file
  file.write(html_file, html_data)


def mkdtree_to_htmltree(
    mkd_root_path,
    html_root_path=os.path.curdir,
    template=None,
    mkd_tag=None,
    debug = False ):
  """Convert mkd tree to  html tree."""
  for mkd_file in file.find_mkd(mkd_root_path):
    html_relative_path = os.path.splitext(mkd_file)[0]+".html"
    html_file = os.path.join(html_root_path, html_relative_path)
    mkd_file_to_html_file(
      os.path.join(mkd_root_path,mkd_file),
      html_file = html_file,
      template = template,
      mkd_tag = mkd_tag,
      debug = debug
      )






