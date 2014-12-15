import markdown

def mkd_to_html(mkd, template=None, mkd_tag=None):
  html = markdown.markdown(
    mkd,
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
  
  
