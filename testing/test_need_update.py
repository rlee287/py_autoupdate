from __future__ import absolute_import, print_function

import os
import pytest
from ..pyautoupdate.launcher import Launcher

from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

@needinternet
def test_check_vers_update(fixture_update_dir):
    package=fixture_update_dir("0.0.1")
    launch = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing/')
    isnew=launch.check_new()
    assert isnew