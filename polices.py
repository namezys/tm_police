'''
Created on Mar 1, 2015

@author: namezys

Set of Time Machine polices
'''

import os
from tm_police.ctrl import disable_tm
from tm_police.ctrl import enable_tm
from tm_police.ctrl import find_tm_disabled_parent

from logging import getLogger

logger = getLogger()


class BasePolice(object):
    def __init__(self, path=None):
        self.path = os.path.expanduser(path)

    def work(self):
        raise NotImplemented


class ListPolice(BasePolice):
    """Simple police: create directory list and disable backup"""
    def __init__(self, file_path=None, *args, **kwargs):
        BasePolice.__init__(self, *args, **kwargs)
        if file_path:
            self.file_path = os.path.expanduser(file_path)
        else:
            self.file_path = self.path + ".backup_list"

    def work(self):
        abs_path = os.path.abspath(self.file_path)
        if find_tm_disabled_parent(abs_path) == abs_path:
            logger.info("Enable backup for %s", abs_path)
            enable_tm(abs_path)
        assert find_tm_disabled_parent(abs_path) is None, "can't backup list"

        logger.info("Build list for %s, save it to %s", self.path, abs_path)
        objects = os.listdir(self.path)
        with open(abs_path, "w") as f:
            for o in objects:
                if not isinstance(o, unicode):
                    o = o.decode('utf8')
                f.write(o.encode('utf8'))
                f.write("\n")
        logger.info("Disable backup for %s", self.path)
        disable_tm(os.path.abspath(self.path))


class Enable(BasePolice):

    def work(self):
        logger.info("Enable backup for %s", self.path)
        enable_tm(self.path)


class Disable(BasePolice):

    def work(self):
        logger.info("Disable backup for %s", self.path)
        disable_tm(self.path)


MODULES = {
    'list': ListPolice,
    'enable': Enable,
    'disable': Disable,
}


def get_module(name):
    return MODULES.get(name)
