from os.path import isfile, join, isdir
from os import listdir, rmdir
from argparse import ArgumentParser


class _DirectoryCleanerNode:
    def __init__(self, path: str, parent=None):
        self.path: str = path
        self.parent: _DirectoryCleanerNode = parent
        self.files: set = set()
        self.dirs: set = set()

        for item in listdir(self.path):
            item_path = join(self.path, item)
            if isfile(item_path):
                self.files.add(item_path)
            else:
                self.dirs.add(item_path)
                _DirectoryCleanerNode(item_path, self)

        if not self.files and not self.dirs:
            if self.parent:
                self.parent._remove_dir(self.path)
            rmdir(self.path)

    def _remove_dir(self, dir_path: str) -> None:
        self.dirs.remove(dir_path)


def clean(dir_path: str) -> None:
    if not isdir(dir_path):
        raise NotADirectoryError(f"{dir_path} is not a directory")
    _DirectoryCleanerNode(dir_path)


if __name__ == '__main__':
    parser = ArgumentParser(description="remove all empty directories starting at a given path")
    parser.add_argument("directory")
    args = parser.parse_args()
    clean(args.directory)
