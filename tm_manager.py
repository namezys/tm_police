'''
Created on Mar 1, 2015

@author: namezys
'''

import json
import logging
import os
from argparse import ArgumentParser
from tm_police.polices import get_module

DESCR = "Special time machine backup politics"


def process(config_file):
    all_cfg = json.load(open(config_file))
    for cfg in all_cfg:
        module = get_module(cfg["module"])(**cfg["args"])
        module.work()


def main():
    parser = ArgumentParser(description=DESCR)
    parser.add_argument("-c", "--configurgtion",
                        help="Configuration file",
                        default="~/.tm_police.json")
    parser.add_argument("--log-level",
                        choices=['INFO', 'WARNING', 'DEBUG', 'CRITICAL'],
                        help="Logging level",
                        default='INFO')
    args = parser.parse_args()
    logging.basicConfig(format='%(message)s',
                        level=getattr(logging, args.log_level))
    process(os.path.expanduser(args.configurgtion))


if __name__ == "__main__":
    main()
