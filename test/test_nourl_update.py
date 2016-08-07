from __future__ import absolute_import, print_function

import pytest
from requests import HTTPError
from ..pyautoupdate.launcher import Launcher

from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

@needinternet
def test_check_vers_nourl(fixture_update_dir):
    """Test that ensures graceful failure when version.txt is missing"""
    package=fixture_update_dir("0.2.0")
    with pytest.raises(HTTPError):
        #No version.txt at the following url
        launch = Launcher('ANNOYING',
                          r'http://rlee287.github.io/pyautoupdate/')
        launch.check_new()
