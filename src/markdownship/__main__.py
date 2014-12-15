#!/usr/bin/env python

import argparse
from . import mkd_to_html
import markdownship.file as file


def get_arguments():
  parser = argparse.ArgumentParser(
    prog = "markdownship",
    version = "0.1.0",
    description="Markdown to HTML converter." )
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

  data = file.read(args.mkd_path)

  output = ""
  if args.template:
    template = file.read(args.template)
    mkd_tag = args.markdown_tag
    output = mkd_to_html(data, template, mkd_tag)
  else:
    output = mkd_to_html(data)

  if args.out:
    file.write(args.out, output)
  else:
    print output



if __name__ == "__main__":
  main()

