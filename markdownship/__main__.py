#!/usr/bin/env python

import argparse, markdownship, sys, importlib, pkgutil
from markdownship import config, templates
from markdownship.convert import *
from os import path

def get_arguments():
  parser = argparse.ArgumentParser(
    prog = "markdownship",
    version = markdownship.__version__,
    description="Markdown to HTML converter." )
  parser.add_argument(
    'markdown', type=str,
    help='Input markdown file or directory.')
  parser.add_argument(
    '-o', '--out', dest="out", action="store", type=str,
    help="Output file name when converting single file, or directory path when\
          converting recursively.")
  parser.add_argument(
    '--markdown-tag', dest="markdown_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by html\
          representation of markdown file. Defaults to %%markdown%%")
  parser.add_argument(
    '--toc-tag', dest="toc_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by table of\
          contents for current directory and below. Defaults to %%toc%%")
  parser.add_argument(
    '-c', '--toc', dest="toc", action="store_true",
    help="Generate table of contents on converted directory.")
  parser.add_argument(
    '-w', '--website', dest="website", action="store_true",
    help="Website friendly output.")
  parser.add_argument(
    '-t', '--template', dest="template_name", action="store", type=str,
    help="Template name.")
  parser.add_argument(
    '--list-templates', dest="list_templates", action="store_true",
    help="List available templates and exit. Will override all other options.")
  parser.add_argument(
    '-d', '--debug', dest="debug", action="store_true",
    help="Enable debug mode with print output of each action.")
  parser.set_defaults(
    out=None,
    markdown_tag="%markdown%",
    toc_tag="%toc%",
    website=False,
    template_name=None,
    list_templates=False,
    debug=False,
  )
  return parser.parse_args()


def main():
  args = get_arguments()
  if args.list_templates:
    pkgpath = path.dirname(templates.__file__)   
    for _, name, _ in pkgutil.iter_modules([pkgpath]):
      print name
    sys.exit()
 
  if path.isfile(args.markdown):
    # convert one file
    if not template_name:
      template_name = "default_no_toc"
    else:
      template_lib = importlib.import_module(
        "markdownship.templates."+args.template_name)
      template = template_lib.template
    html = file_to_html(
      mkd_file = args.markdown,
      html_file = args.out,
      template = template,
      mkd_tag = args.markdown_tag,
      toc_tag = None,
      debug = args.debug,
      )
    if not args.out:
      print html
  elif path.isdir(args.markdown):
    # convert directory
    if not template_name:
      template_name = "default"
    else:
      template_lib = importlib.import_module(
        "markdownship.templates."+args.template_name)
      template = template_lib.template
    tree_to_html(
      source_path = args.markdown,
      target_path = args.out,
      template = template,
      mkd_tag = args.markdown_tag,
      toc_tag = args.toc_tag,
      website = args.website,
      debug = args.debug,
      )
  else:
    print "'"+args.markdown+"'", "is not file or dir"

if __name__ == "__main__":
  main()


