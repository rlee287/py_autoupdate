from __future__ import absolute_import, print_function

import os
import pytest
from requests import HTTPError
from ..launcher import Launcher

from .pytest_skipif import needinternet

@pytest.fixture(scope='function')
def create_update_dir(request):
    def teardown():
        if os.path.isfile('version.txt.old'):
            os.remove('version.txt.old')
        if os.path.isfile('version.txt'):
            os.remove('version.txt')
    request.addfinalizer(teardown)
    with open('version.txt', mode='w') as file:
        file.write("0.2.0")
    return create_update_dir
    
@needinternet
def test_check_vers_nourl(create_update_dir):
    with pytest.raises(HTTPError):
        #No version.txt at the following url
        launch = Launcher('',r'http://rlee287.github.io/pyautoupdate/')
        launch.check_new()
