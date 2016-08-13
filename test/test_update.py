from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet

import os
import shutil

import pytest

@pytest.fixture(scope='function')
def fixture_update_setup(request):
    """Sets up and tears down version docs and code files"""
    def teardown():
        if os.path.isfile('version_history.log'):
            os.remove('version_history.log')
        if os.path.isfile('version.txt'):
            os.remove('version.txt')
        if os.path.isdir("extradir"):
            shutil.rmtree("extradir")
        if os.path.isfile("filelist.txt"):
            os.remove("filelist.txt")
        launch = Launcher('extradir/blah.py',
                          r'http://rlee287.github.io/pyautoupdate/testing/')
        launch._reset_update_dir()
        if os.path.isdir("downloads"):
            os.rmdir("downloads")
    request.addfinalizer(teardown)
    with open('version.txt', mode='w') as version_file:
        version_file.write("0.0.1")
    os.mkdir("extradir")
    with open(os.path.join("extradir", "blah.py"), mode='w') as code:
        code.write("print('This is the old version')")
    with open("filelist.txt", mode='w') as filelist:
        filelist.write("extradir/blah.py")
    return fixture_update_setup

@pytest.mark.trylast
@needinternet
def test_check_update(fixture_update_setup):
    """Checks the ability of program to upload new code"""
    assert os.path.isfile("filelist.txt")
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch.update_code()
    assert os.path.isfile("extradir/blah.py")
    with open(os.path.abspath("extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
    assert os.path.isfile("filelist.txt")
