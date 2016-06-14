from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet

import pytest

import os
import shutil

@pytest.fixture(scope='function')
def fixture_update_dir(request):
    def teardown():
        if os.path.isfile('version.txt.old'):
            os.remove('version.txt.old')
        if os.path.isfile('version.txt'):
            os.remove('version.txt')
        if os.path.isdir("extradir"):
            shutil.rmtree("extradir")
    request.addfinalizer(teardown)
    with open('version.txt', mode='w') as version_file:
        version_file.write("0.0.1")
    os.mkdir("extradir")
    with open(os.path.join("extradir", "blah.py"), mode='w') as code:
        code.write("print('This is the old version')")
    return fixture_update_dir

@pytest.mark.trylast
@needinternet
def test_check_vers_update(fixture_update_dir):
    launch = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing/')
    launch.update_code()
    with open(os.path.abspath("downloads/extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
