#!/usr/bin/env python

from distutils.core import setup
import markdownship

setup(
  name = 'markdownship',
  description = markdownship.__doc__.strip(),
  url = 'https://automateship.com',
  download_url = \
    'https://github.com/automateship/markdownship/archive/master.zip',
  version = markdownship.__version__,
  author = markdownship.__author__,
  author_email = 'github@phlogisto.com',
  license = markdownship.__licence__,
  packages = ['markdownship', ],
  install_requires = [
    'argparse==1.2.1',
    'markdown==2.3.1',
    'pygments==2.0.1',
    ],
  )

