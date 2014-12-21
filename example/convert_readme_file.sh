#!/bin/sh

example_dir=$(dirname "$([ "$0" = "/*" ] && echo "$0" || echo "${PWD}/${0#./}")")
python -m markdownship -T $example_dir/../README.mkd -o $example_dir/../README.html -c


