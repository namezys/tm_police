'''
Created on Mar 1, 2015

@author: namezys

Set time machine backup disable flag
'''

import os
from argparse import ArgumentParser
from tm_police.ctrl import enable_tm
from tm_police.ctrl import disable_tm


DESCR = """Set or reset time machine disable flag"""


def main():
    parser = ArgumentParser(description=DESCR)
    parser.add_argument("-e", "--enable", action="store_true",
                        help="Enable TM backup. Otherwise disable")
    parser.add_argument("paths", nargs="+", help="path for check")
    args = parser.parse_args()

    paths = args.paths
    for path in paths:
        if not os.path.exists(path):
            print path, "don't exists"
            return

    for path in paths:
        if args.enable:
            enable_tm(path)
        else:
            disable_tm(path)

if __name__ == '__main__':
    main()
