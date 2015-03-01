'''
Created on Mar 1, 2015

@author: namezys

Functions for control Time Machine xattr
'''

import os
import subprocess

TIMEMACHINE_EXCLUDE_ATTR = "com.apple.metadata:com_apple_backup_excludeItem"
TIMEMACHINE_EXCLUDE_VALUE = """62 70 6C 69 73 74 30 30 5F 10 11 63 6F 6D 2E 61
70 70 6C 65 2E 62 61 63 6B 75 70 64 08 00 00 00
00 00 00 01 01 00 00 00 00 00 00 00 01 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 1C"""

__check_cache = {}
__find_cache = {}


def is_disabled_tm(path):
    """Check that Time Machine backup is disable for path"""
    output = subprocess.check_output(["xattr", path])
    return TIMEMACHINE_EXCLUDE_ATTR in output


def disable_tm(path):
    """Disable Time Machine backup for path

    Nothing to do if backup've been disabled yet
    """
    output = subprocess.check_output(["xattr", path])
    if TIMEMACHINE_EXCLUDE_ATTR in output:
        return
    subprocess.check_call(["xattr", "-wx", TIMEMACHINE_EXCLUDE_ATTR,
                           TIMEMACHINE_EXCLUDE_VALUE, path])


def enable_tm(path):
    """Enable Time Machine backup for path

    Nothing to do if backup've not been disabled
    """
    output = subprocess.check_output(["xattr", path])
    if TIMEMACHINE_EXCLUDE_ATTR in output:
        subprocess.check_call(["xattr", "-d", TIMEMACHINE_EXCLUDE_ATTR, path])


def find_tm_disabled_parent(path):
    """Search closest parent with disabled TM backup

    Work only with absolute path
    :return: parent path if it've been found or None otherwise"""
    global __find_cache
    assert path == '/' or (path[0] == '/' and path[-1] != '/')
    if path in __find_cache:
        return __find_cache[path]
    if is_disabled_tm(path):
        res_path = path
    elif path == '/':
        res_path = None
    else:
        parent_path, _ = os.path.split(path)
        res_path = find_tm_disabled_parent(parent_path)
    __find_cache[path] = res_path
    return res_path
