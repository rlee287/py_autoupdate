from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import CorruptedFileWarning
from .pytest_skipif import needinternet
from .pytest_makevers import fixture_update_dir

import glob
import os

import pytest
from requests import HTTPError

@needinternet
def test_check_update_needed(fixture_update_dir):
    """Test that ensures that updates occur when needed"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing/')
    #pdb.set_trace()
    isnew=launch.check_new()
    assert isnew
    assert os.path.isfile(Launcher.version_doc)
    assert os.path.isfile(Launcher.version_check_log)
    assert os.path.isfile(Launcher.queue_update)
    os.remove(Launcher.queue_update)
    with open(Launcher.version_check_log,"r") as log_handle:
        log=log_handle.read()
    assert "New" in log

@needinternet
def test_check_update_notneeded(fixture_update_dir):
    """Test to check update checker when update is not necessary"""
    package=fixture_update_dir('0.2.0')
    launch = Launcher('pypipypipypipypi',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing/')
    isnew=launch.check_new()
    assert not isnew
    assert os.path.isfile(Launcher.version_doc)
    assert os.path.isfile(Launcher.version_check_log)
    with open(Launcher.version_check_log,"r") as log_handle:
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
    """Fixture to remove error dump"""
    def teardown():
        for glob_file in glob.iglob("newverdump*"):
            os.remove(glob_file)
    request.addfinalizer(teardown)
    return remove_dump

@needinternet
def test_check_update_invalidvers(fixture_update_dir,remove_dump):
    """Test that ensures that updates occur when needed"""
    package=fixture_update_dir("0.0.1")
    launch = Launcher('blah',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing2/')
    with pytest.raises(CorruptedFileWarning):
        launch.check_new()
    assert os.path.isfile(Launcher.version_doc)
    assert os.path.isfile(Launcher.version_check_log)
    with open(Launcher.version_check_log,"r") as log_handle:
        log=log_handle.read()
    assert "Server Invalid" in log

