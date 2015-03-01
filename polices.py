'''
Created on Mar 1, 2015

@author: namezys

Set of Time Machine polices
'''

import json
import os
from tm_police.ctrl import disable_tm
from tm_police.ctrl import enable_tm
from tm_police.ctrl import find_tm_disabled_parent

from logging import getLogger
from matplotlib.font_manager import path

logger = getLogger()

TM_POLICE_FILE = ".tm_police"
TM_POLICE_JSON = ".tm_police.json"


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


def _update_args(args, path):
    def _r_path(key, value, path):
        if 'path' in key and (not value or value[0] != '/'):
            value = os.path.join(path)
        return key, value
    return dict(_r_path(k, v, path) for k, v in args.items())


class DirControl(BasePolice):
    """Search TM police in child directories"""

    def _work_on_path(self, path):
        logger.debug("Check %s", path)
        police_file = os.path.join(path, TM_POLICE_FILE)
        police_json = os.path.join(path, TM_POLICE_JSON)
        if os.path.exists(police_file):
            logger.info("Found TM police %s", police_file)
            if os.path.exists(police_json):
                logger.error("Found %s and %s simultaneously",
                             police_file, police_json)
                return
            module = open(police_file).read().strip()
            logger.info("Use TM police module %s", module)
            args = {'path': path}
        elif os.path.exists(police_json):
            logger.info("Found TM police JSON", police_json)
            cfg = json.load(open(police_json))
            logger.debug("Update args")
            args = _update_args(cfg["args"], path)
            module = cfg["module"]
            logger.debug("Found module %s", module)
        else:
            logger.debug("TM police file not found. Skip %s", path)
            return
        logger.debug("Create module and execute it")
        get_module(module)(**args).work()

    def work(self):
        logger.debug("Search tm police for child dirs of %s", self.path)
        for name in os.listdir(self.path):
            path = os.path.join(self.path, name)
            if not os.path.isdir(path):
                continue
            self._work_on_path(os.path.abspath(path))


MODULES = {
    'list': ListPolice,
    'enable': Enable,
    'disable': Disable,
    'control': DirControl
}


def get_module(name):
    return MODULES.get(name)
