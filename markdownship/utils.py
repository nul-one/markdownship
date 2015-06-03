"""Collection of file operating wrapper functions.
"""

import codecs
from os import path, makedirs, walk


def trim_path(path_str):
    '''Returns path without leading or trailing slashes.'''
    while path_str[-1:] is path.sep:
        path_str = path_str[:-1]
    while path_str[:1] is path.sep:
        path_str = path_str[1:]
    return path_str


class afile(object):
    def __init__(self, path=None):
        self.path = path

    @staticmethod
    def find_mkd(root_path):
        """Searches for files with .md and .mkd extensions and returns a list
        of afile objects."""
        mkd_file_list = []
        for root, dirs, files in walk(root_path):
            for f in files:
                mkd_file = afile(path.join(root, f))
                if mkd_file.is_markdown() and mkd_file.getname()[:1] is not "_":
                    mkd_file_list.append(mkd_file)
        return mkd_file_list
        
    def getname(self):
        '''Return name of the file without dir path.'''
        return path.basename(self.path)

    def getbasename(self):
        '''Return name of the file without dir path or extension.'''
        name_split = self.getname().split('.')
        basename = '.'.join(name_split[:len(name_split)-1])
        if basename:
            return basename
        else:
            return self.getname()

    def getdir(self):
        return path.dirname(self.path)

    def read(self):
        try:
            with codecs.open(self.path, mode="r", encoding="utf-8") as myfile:
                data=myfile.read()
                return data
        except Exception, err:
            raise Exception("Error reading file: " + self.path)

    def write(self, data=""):
        if self.path and not path.exists(self.getdir()):
            makedirs(self.getdir())
        try:
            with codecs.open(self.path, mode="w", encoding="utf-8") as myfile:
                myfile.write(data)
        except Exception, err:
            raise Exception("Error writting file: " + self.path)

    def is_markdown(self):
        if self.path.lower().endswith(".md") or \
                self.path.lower().endswith(".mkd") or \
                self.path.lower().endswith(".markdown"):
            return True
        return False

    def relativepath(self, root_path=""):
        '''Returns path relative to root_path.'''
        root_path = trim_path(root_path)
        full_path = trim_path(self.path)
        relative_path = full_path[len(root_path):]
        return trim_path(relative_path)



if __name__ == "__main__":
    import doctest
    doctest.testmod()

