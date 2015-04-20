#!/usr/bin/env python

import argparse, markdownship, sys, importlib, pkgutil, pkg_resources, shutil
from markdownship import config, templates, toc, header, footer
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
    '-o', '--out', dest="out", action="store", type=str,
    help="Output file name when converting single file, or directory path when\
          converting recursively.")
  parser_build.add_argument(
    '-d', '--data', dest="data", action="store", type=str,
    help="Name of the data directory. Defaults to _data")
  parser_build.add_argument(
    '-t', '--template', dest="template_name", action="store", type=str,
    help="Template name.")
  parser_build.add_argument(
    '-T', '--custom-template', dest="custom_template", action="store", type=str,
    help="Path to custom template file.")
  parser_build.add_argument(
    '--no-toc', dest="no_toc", action="store_true",
    help="Do not create table of contents.")
  parser_build.add_argument(
    '-g', '--debug', dest="debug", action="store_true",
    help="Enable debug mode with print output of each action.")
  parser_build.set_defaults(
    out=None,
    url=None,
    data='_data',
    template_name=None,
    custom_template=None,
    list_templates=False,
    no_toc=False,
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
 
  template = None
  if args.custom_template:
    try:
      template = file.read(args.custom_template)
    except Exception, err:
      print "ERROR - Custom template: " + str(err)
      print "  Using existing templates instead."
  if template is None:
    template_name = args.template_name or "default"
    try:
      template = pkg_resources.resource_string(
        "markdownship.templates", template_name+".html.template")
    except Exception, err:
      print "ERROR - Template: " + str(err)
      print "  Using default template instead."
      template = pkg_resources.resource_string(
        "markdownship.templates", "default"+".html.template")

  if path.isfile(args.markdown):
    # convert one file
    html = file_to_html(
      mkd_file = args.markdown,
      html_file = args.out,
      template = template,
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
    header_data = header.create(
      root_path = args.markdown,
      url = url,
      is_local = is_local,
      data_dir = args.data,
      debug = args.debug ) or " "
    footer_data = footer.create(
      root_path = args.markdown,
      url = url,
      is_local = is_local,
      data_dir = args.data,
      debug = args.debug ) or " "
    toc_data = ""
    if not args.no_toc:
      toc_data = toc.from_file(
        root_path = args.markdown,
        data_dir = args.data,
        debug = args.debug )
      if toc_data is None:
        toc_data = toc.create(
          root_path = args.markdown,
          url = url,
          is_local = is_local,
          data_dir = args.data,
          debug = args.debug ) or " "
    create_dirs(
      source_path = args.markdown,
      target_path = out,
      debug = args.debug,
    )
    if not args.no_toc:
      add_missing_toc(
        target_path = out,
        template = template,
        toc_data = toc_data,
        header_data = header_data,
        footer_data = footer_data,
        debug = args.debug )
    data_src = path.join(args.markdown, args.data)
    data_tgt = path.join(out, args.data)
    if path.isdir(data_src):
      shutil.rmtree(data_tgt, True)
      shutil.copytree(data_src, data_tgt)
    tree_to_html(
      source_path = args.markdown,
      target_path = out,
      template = template,
      toc_data = toc_data,
      header_data = header_data,
      footer_data = footer_data,
      url = url,
      data_dir = args.data,
      debug = args.debug,
      )
  else:
    print "'"+args.markdown+"'", "is not file or dir"

if __name__ == "__main__":
  main()


