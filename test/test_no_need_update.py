from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import os

@needinternet
def test_check_vers_noupdate(fixture_update_dir):
    """Test to check update checker when update is not necessary"""
    package=fixture_update_dir('0.2.0')
    launch = Launcher('pypipypipypipypi',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    isnew=launch.check_new()
    assert not isnew
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version_history.log")
    with open("version_history.log","r") as log_handle:
        log=log_handle.read()
    assert "Up to date" in log
    del launch
