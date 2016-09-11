from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import CorruptedFileWarning
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import os

import pytest
from requests import HTTPError

@needinternet
def test_check_update_needed(fixture_update_dir):
    """Test that ensures that updates occur when needed"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    isnew=launch.check_new()
    assert isnew
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version_history.log")
    with open("version_history.log","r") as log_handle:
        log=log_handle.read()
    assert "New" in log

@needinternet
def test_check_update_notneeded(fixture_update_dir):
    """Test to check update checker when update is not necessary"""
    package=fixture_update_dir('0.2.0')
    launch = Launcher('pypipypipypipypi',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    isnew=launch.check_new()
    assert not isnew
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version_history.log")
    with open("version_history.log","r") as log_handle:
        log=log_handle.read()
    assert "Up to date" in log

@needinternet
def test_check_update_nourl(fixture_update_dir):
    """Test that ensures graceful failure when version.txt is missing"""
    package=fixture_update_dir("0.2.0")
    with pytest.raises(HTTPError):
        #No version.txt at the following url
        launch = Launcher('ANNOYING',
                          r'http://rlee287.github.io/pyautoupdate/')
        launch.check_new()

@pytest.fixture(scope="function")
def remove_dump(request):
    def teardown():
        for glob in glob.iglob("newverdump*"):
            os.remove(glob)
    requests.addfinalizer(teardown)
    return remove_dump

@needinternet
def test_check_update_invalidvers(fixture_update_dir,remove_dump):
    """Test that ensures that updates occur when needed"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/testing2/')
    with pytest.raises(CorruptedFileWarning):
        launch.check_new()
    assert os.path.isfile("version.txt")
    assert os.path.isfile("version_history.log")
    with open("version_history.log","r") as log_handle:
        log=log_handle.read()
    assert "Server Invalid" in log

