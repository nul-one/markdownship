"""Collection of file operating wrapper functions.
"""


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


if __name__ == "__main__":
  import doctest
  doctest.testmod()

