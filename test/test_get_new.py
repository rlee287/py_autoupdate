from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import os
import sys

import pytest

@pytest.fixture("function")
def create_zip(request):
    def teardown():
        if os.path.isfile("project.zip"):
            os.remove("project.zip")
    request.addfinalizer(teardown)
    if sys.version_info[0]==2:
        empty_zip_data = 'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'+\
                         '\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    else:
        empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'+\
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    with open('project.zip', 'wb') as zip_file:
        zip_file.write(empty_zip_data)


@pytest.mark.trylast
@needinternet
def test_check_vers_update(create_zip, fixture_update_dir):
    package=fixture_update_dir("0.0.1")
    launch = Launcher('filling up the boring replacements',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch._get_new()
    with open(os.path.abspath("downloads/extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
