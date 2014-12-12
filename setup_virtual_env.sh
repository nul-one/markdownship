#!/bin/bash

virtualenv env
source env/bin/activate
pip install -r requirements.txt
pushd src
  ./setup.py sdist
  pip install dist/markdownship*.tar.gz --upgrade
popd

