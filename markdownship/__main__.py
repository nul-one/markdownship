#!/usr/bin/env python

import argparse, markdownship, sys, importlib, pkgutil, pkg_resources
from markdownship import config, templates, toc
from markdownship.convert import *
from os import path

def get_arguments():
  parser = argparse.ArgumentParser(
    prog = "markdownship",
    version = markdownship.__version__,
    description="Markdown to HTML converter." )
  subparsers = parser.add_subparsers(
    description='available subcommands',
    dest='cmd',
    )
  subparsers.required = True
  parser_templates = subparsers.add_parser(
    'templates',
    description='List available templates and exit.')
  parser_build = subparsers.add_parser(
    'build',
    description='Convert mkd file or directory of files into html.'
    )
  parser_build.add_argument(
    'markdown', type=str,
    help='Input markdown file or directory.')
  parser_build.add_argument(
    '-u', '--url', dest='url', action='store', type=str,
    help='Define base url that will be used for links \
          (e.g. http://my.wiki.com/me/)')
  parser_build.add_argument(
    '--url-tag', dest="url_tag", action="store", type=str,
    help="Tag string in content that will later be replaced by base url.\
          Defaults to %%url%%")
  parser_build.add_argument(
    '-o', '--out', dest="out", action="store", type=str,
    help="Output file name when converting single file, or directory path when\
          converting recursively.")
  parser_build.add_argument(
    '--markdown-tag', dest="markdown_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by html\
          representation of markdown file. Defaults to %%markdown%%")
  parser_build.add_argument(
    '--toc-tag', dest="toc_tag", action="store", type=str,
    help="Tag string in template that will later be replaced by table of\
          contents for current directory and below. Defaults to %%toc%%")
  parser_build.add_argument(
    '-c', '--toc', dest="toc", action="store_true",
    help="Generate table of contents on converted directory.")
  parser_build.add_argument(
    '-t', '--template', dest="template_name", action="store", type=str,
    help="Template name.")
  parser_build.add_argument(
    '-d', '--debug', dest="debug", action="store_true",
    help="Enable debug mode with print output of each action.")
  parser_build.set_defaults(
    out=None,
    markdown_tag="%markdown%",
    toc_tag="%toc%",
    url_tag="%url%",
    url=None,
    template_name=None,
    list_templates=False,
    debug=False,
  )
  return parser.parse_args()


def main():
  args = get_arguments()
  if args.cmd == "templates":
    template_resources = pkg_resources.resource_listdir(
      "markdownship.templates", ".")
    templates = [ s[:-14] for s in template_resources
      if s.endswith(".html.template") ]
    for name in sorted(templates):
      print name
    sys.exit()
 
  if path.isfile(args.markdown):
    # convert one file
    template_name = args.template_name or "default_no_toc"
    template = pkg_resources.resource_string(
      "markdownship.templates", template_name+".html.template")
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
    is_local = True
    out = args.out or path.abspath(path.curdir)
    url = args.url or "file://"+out
    if args.url:
      is_local = False
    template_name = args.template_name or "default"
    template = pkg_resources.resource_string(
      "markdownship.templates", template_name+".html.template")
    toc_data = toc.create(
      root_path = args.markdown,
      url = url,
      is_local = is_local,
      debug = args.debug ) or ""
    add_missing_toc(
      target_path = out,
      template = template,
      mkd_tag = args.markdown_tag,
      toc_tag = args.toc_tag,
      toc_data = toc_data,
      debug = args.debug )
    tree_to_html(
      source_path = args.markdown,
      target_path = out,
      template = template,
      mkd_tag = args.markdown_tag,
      toc_tag = args.toc_tag,
      toc_data = toc_data,
      url_tag = args.url_tag,
      url = url,
      debug = args.debug,
      )
  else:
    print "'"+args.markdown+"'", "is not file or dir"

if __name__ == "__main__":
  main()


