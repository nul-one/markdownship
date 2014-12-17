#!/usr/bin/env python

from distutils.core import setup

setup(
  name='markdownship',
  version="0.1.0",
  description='Markdown to html converter.',
  author='Predrag Mandic',
  author_email='predrag@phlogisto.com',
  packages=['markdownship', ],
  install_requires = [
    'argparse==1.2.1',
    'markdown==2.3.1',
    ],
  )

