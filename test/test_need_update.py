from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import os

@needinternet
def test_check_need_update(fixture_update_dir):
    """Test that ensures that updates occur when needed"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    print("launch.oldcwd:", launch.oldcwd)
    print("os.getcwd:",os.getcwd())
    isnew=launch.check_new()
    assert isnew
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version_history.log")
    with open("version_history.log","r") as log_handle:
        log=log_handle.read()
    assert "New" in log
    del launch
    # Make sure log can be appended to
    #launch.check_new()
