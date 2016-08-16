from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet

from logging import DEBUG
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
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")
    request.addfinalizer(teardown)
    with open('version.txt', mode='w') as version_file:
        version_file.write("0.0.1")
    os.mkdir("extradir")
    os.makedirs(os.path.join("downloads","extradir"))
    extradir_blah=os.path.join("extradir","blah.py")
    extradir_dummy=os.path.join("extradir","dummy.txt")
    downloads_extradir_blah=os.path.join("downloads","extradir","blah.py")
    with open(extradir_blah, mode='w') as code:
        code.write("print('This is the old version')")
    with open(extradir_dummy, mode='w') as extra_file:
        extra_file.write("1984: 2+2=5")
    with open(downloads_extradir_blah, mode='w') as new_code:
        new_code.write("print('This is the new version')")
    with open("filelist.txt", mode='w') as filelist:
        filelist.write(extradir_blah+"\n")
        filelist.write(extradir_dummy+"\n")
    return fixture_update_setup

@pytest.mark.trylast
def test_check_update(fixture_update_setup):
    """Checks the ability of program to upload new code"""
    assert os.path.isfile("filelist.txt")
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/testing/',
                      'project.zip','downloads',DEBUG)
    launch._replace_files()
    assert os.path.isfile("extradir/blah.py")
    with open(os.path.abspath("extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
    assert os.path.isfile("filelist.txt")
