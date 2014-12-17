"""Collection of file operating wrapper functions.
"""

import os

def read(file_name):
  """Read a file on path file_name and return a string with it's contents."""
  try:
    with open(file_name, "r") as myfile:
      data=myfile.read()
      return data
  except Exception, err:
    raise Exception("Error reading file: " + file_name)


def write(file_name, data):
  """Write data string to a file on path file_name."""
  try:
    with open(file_name, "w") as myfile:
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

