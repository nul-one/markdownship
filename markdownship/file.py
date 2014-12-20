"""Collection of file operating wrapper functions.
"""

import os, codecs


def read(file_name):
  """Read a file on path file_name and return a string with it's contents."""
  try:
    with codecs.open(file_name, mode="r", encoding="utf-8") as myfile:
      data=myfile.read()
      return data
  except Exception, err:
    raise Exception("Error reading file: " + file_name)


def write(file_name, data):
  """Write data string to a file on path file_name.
     Create directories if needed."""
  file_dir = os.path.dirname(file_name)
  if file_dir and not os.path.exists(file_dir):
    os.makedirs(file_dir)
  try:
    with codecs.open(file_name, mode="w", encoding="utf-8") as myfile:
      myfile.write(data)
  except Exception, err:
    raise Exception("Error writting file: " + file_name)


def find_mkd(root_path):
  """Searches for files with .md and .mkd extensions and returns a list of
  relative paths to "root_path". """
  mkd_file_list = []
  for root, dirs, files in os.walk(root_path):
    for file in files:
      if file.lower().endswith((".md", ".mkd")):
        relative_file_path = os.path.join(root, file)[len(root_path):]
        mkd_file_list.append(relative_file_path)
  return mkd_file_list
  


if __name__ == "__main__":
  import doctest
  doctest.testmod()

