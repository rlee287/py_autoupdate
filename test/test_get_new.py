from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir,create_update_dir

import os
import sys

import pytest

@pytest.fixture("function")
def create_zip(request):
    """Fixture that creates an empty .zip file"""
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
def test_check_get_new(create_zip, fixture_update_dir,create_update_dir):
    """Test that gets new version from internet"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('filling up the boring replacements',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch._get_new()
    with open(os.path.abspath("downloads/extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
    assert os.path.isdir("downloads")

@needinternet
def test_check_get_invalid_archive(fixture_update_dir):
    """Test that gets new version from internet"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('what file? hahahaha',
                      r'http://rlee287.github.io/pyautoupdate/testing2/',
                      newfiles="project.tar.gz")
    launch._get_new()
    assert os.path.isfile("project.tar.gz.dump")
    assert not os.path.isdir("downloads")
    os.remove("project.tar.gz.dump")
