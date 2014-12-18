#!/usr/bin/env python

import argparse, markdownship
from markdownship import file, toc
from markdownship.convert import *


def get_arguments():
  parser = argparse.ArgumentParser(
    prog = "markdownship",
    version = markdownship.__version__,
    description="Markdown to HTML converter." )
  parser.add_argument(
    'markdown', type=str,
    help='Input markdown file or directory.')
  parser.add_argument(
    '-t', '--template', dest="template", action="store", type=str,
    help="Path to template file. When used, output will have contents of\
          template file with %%markdown%% string replaced with html\
          representation of input markdown file.")
  parser.add_argument(
    '-o', '--out', dest="out", action="store", type=str,
    help="Output file name when converting single file, or directory path when\
          converting recursively.")
  parser.add_argument(
    '-m', '--markdown-tag', dest="markdown_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by html\
          representation of markdown file. Defaults to %%markdown%%")
  parser.add_argument(
    '-c', '--toc', dest="toc", action="store_true",
    help="Generate table of contents on converted directory.")
  parser.add_argument(
    '-d', '--debug', dest="debug", action="store_true",
    help="Enable debug mode with print output of each action.")
  parser.set_defaults(
    out=None,
    template=None,
    markdown_tag="%markdown%",
    toc=False,
    debug=False,
  )
  return parser.parse_args()


def main():
  args = get_arguments()

  template = None

  if args.template:
    template = file.read(args.template)

  if os.path.isfile(args.markdown):
    # convert one file
    if args.out:
      # with defined output
      if template:
        mkd_file_to_html_file(
          mkd_file = args.markdown,
          html_file = args.out,
          template = template,
          mkd_tag = args.markdown_tag,
          debug = args.debug,
          )
      else:
        mkd_file_to_html_file(
          mkd_file = args.markdown,
          html_file = args.out,
          debug = args.debug,
          )
    else:
      # without defined output
      if template:
        print mkd_to_html(
          mkd = file.read(args.markdown),
          template = template,
          mkd_tag = args.markdown_tag,
          debug = args.debug,
          )
      else:
        print mkd_to_html(
          mkd = file.read(args.markdown),
          debug = args.debug,
          )
  elif os.path.isdir(args.markdown):
    # convert directory
    if args.out:
      # with defined output
      if template:
        mkdtree_to_htmltree(
          source_path = args.markdown,
          target_path = args.out,
          template = template,
          mkd_tag = args.markdown_tag,
          debug = args.debug,
          )
        if args.toc:
          toc.create(
            root_path=args.out,
            template=template,
            mkd_tag = args.markdown_tag,
            debug=False
          )
      else:
        mkdtree_to_htmltree(
          source_path = args.markdown,
          target_path=args.out,
          debug = args.debug,
          )
        if args.toc:
          toc.create(
            root_path=args.out,
            template=template,
            mkd_tag = args.markdown_tag,
            debug=False
          )
    else:
      # without defined output
      if template:
        mkdtree_to_htmltree(
          source_path = args.markdown,
          template = template,
          mkd_tag = args.markdown_tag,
          debug = args.debug,
          )
        if args.toc:
          toc.create(
            root_path = os.path.curdir(),
            template=template,
            mkd_tag = args.markdown_tag,
            debug=False
          )
      else:
        mkdtree_to_htmltree(
          source_path = args.markdown,
          debug = args.debug,
          )
        if args.toc:
          toc.create(
            root_path = os.path.curdir(),
            template=template,
            mkd_tag = args.markdown_tag,
            debug=False
          )
  else:
    print "'"+args.markdown+"'", "is not file or dir"




if __name__ == "__main__":
  main()












