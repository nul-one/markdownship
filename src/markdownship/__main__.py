#!/usr/bin/env python

import argparse
import markdown
import sys

def read_file(file_name):
  try:
    with open(file_name, "r") as myfile:
      data=myfile.read()
      return data
  except Exception, err:
    print "Error reading file: " + file_name
    sys.exit(1)


def write_file(file_name, data):
  try:
    with open(file_name, "w") as myfile:
      myfile.write(data)
      return True
  except Exception, err:
    print(str(err))
    return False


def mkd_to_html(mkd, template=None):
  html = markdown.markdown(
    mkd,
    extensions=[
      'markdown.extensions.tables',
      'markdown.extensions.codehilite',
      'markdown.extensions.footnotes',
      'markdown.extensions.toc',
      ]
  )
  if template:
    return template['contents'].replace(template['tag'], html)
  else:
    return html
  
  
def get_arguments():
  parser = argparse.ArgumentParser(description='Markdown to HTML converter.')
  parser.add_argument(
    'mkd_path', type=str,
    help='Input markdown file or directory.')
  parser.add_argument(
    '-t', '--template', dest="template", action="store", type=str,
    help="Path to template file. When used, output will have contents of\
          template file with %%MKD%% string replaced with html representation\
          of input markdown file.")
  parser.add_argument(
    '-o', '--out', dest="out", action="store", type=str,
    help="Output file name when converting single file, or directory path when\
          converting recursively.")
  parser.add_argument(
    '-m', '--markdown-tag', dest="markdown_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by html\
          representation of markdown file. Defaults to %%MARKDOWN%%")
  parser.set_defaults(
    out=None,
    template=None,
    markdown_tag="%MARKDOWN%",
  )
  return parser.parse_args()


def main():
  args = get_arguments()

  data = read_file(args.mkd_path)

  output = ""
  if args.template:
    template = {}
    template['contents'] = read_file(args.template)
    template['tag'] = args.markdown_tag
    output = mkd_to_html(data, template)
  else:
    output = mkd_to_html(data)

  if args.out:
    write_file(args.out, output)
  else:
    print output



if __name__ == "__main__":
  main()

