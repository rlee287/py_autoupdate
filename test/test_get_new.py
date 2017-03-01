from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir,create_update_dir

import os

@needinternet
def test_check_get_new(fixture_update_dir,create_update_dir):
    """Test that gets new version from internet"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('filling up the boring replacements',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing/')
    launch._get_new()
    with open(os.path.abspath(os.path.join(Launcher.updatedir,
                        "extradir/blah.py")), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
    assert os.path.isdir(Launcher.updatedir)

@needinternet
def test_check_get_invalid_archive(fixture_update_dir):
    """Test that gets new version from internet"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('what file? hahahaha',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing2/',
                      newfiles="project.tar.gz")
    launch._get_new()
    assert os.path.isfile("project.tar.gz.dump")
    assert not os.path.isdir(Launcher.updatedir)
    os.remove("project.tar.gz.dump")
