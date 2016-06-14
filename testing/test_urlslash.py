from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher

import os

def test_check_urlslash():
    launch = Launcher('not here',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('why do I need to do this',
                       r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url
