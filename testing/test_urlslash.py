from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher

import os

def test_check_vers_update():
    launch = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url
