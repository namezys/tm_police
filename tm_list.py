'''
Created on Mar 1, 2015

@author: namezys

Show state of disabled backup of Time Machine
'''

import os
from argparse import ArgumentParser
from tm_police.ctrl import find_tm_disabled_parent


DESCR = """Check disable of Time Machine backup of given files and search
closest parent with disable flag"""


def main():
    parser = ArgumentParser(description=DESCR)
    parser.add_argument("-p", "--parent", action="store_true",
                        help="Show parent with given property")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Print all paths. Otherwise print only\
                            path with disabled backup")
    parser.add_argument("paths", nargs="*", help="path for check")
    args = parser.parse_args()

    paths = args.paths
    if not paths:
        paths = os.listdir(".")
    elif len(paths) == 1:
        paths = [os.path.join(paths[0], i) for i in os.listdir(paths[0])]

    for path in paths:
        abs_path = os.path.abspath(path)
        parent = find_tm_disabled_parent(abs_path)
        if parent is None and not args.all:
            continue
        print path,
        if args.parent and parent is not None:
            rel_path = os.path.relpath(parent, abs_path)
            parent = os.path.normpath(os.path.join(path, rel_path))
            print '*' if parent == path else parent,
        print


if __name__ == '__main__':
    main()
