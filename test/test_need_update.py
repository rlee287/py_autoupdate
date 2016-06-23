from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import os

@needinternet
def test_check_vers_update(fixture_update_dir):
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    print("launch.oldcwd:", launch.oldcwd)
    print("os.getcwd:",os.getcwd())
    isnew=launch.check_new()
    assert isnew
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version.txt.old")
    # Make sure existing .old can be removed
    launch.check_new()
