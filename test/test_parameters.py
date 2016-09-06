from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import CorruptedFileWarning

import os
import warnings

import pytest

def test_check_urlslash():
    """Test that checks that leading slash is properly added to URL"""
    launch = Launcher('not here',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('why do I need to do this',
                       r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url

def test_check_emptyfilepath():
    """Check that error is raised with empty file"""
    with pytest.raises(ValueError):
        Launcher('','a url')

def test_check_emptyURL():
    """Check that error is raised with empty URL"""
    with pytest.raises(ValueError):
        Launcher('a filepath','')

@pytest.fixture(scope="function")
def fixture_corrupt_log(request):
    """Fixture that creates corrupted log"""
    with open("version_history.log","w") as log:
        log.write("invalid!gibberish")
    def teardown():
        if os.path.isfile("version_history.log"):
            os.remove("version_history.log")
    request.addfinalizer(teardown)
    return fixture_corrupt_log

@pytest.fixture(scope="function")
def fixture_corrupt_vers(request):
    """Fixture that creates invalid version file"""
    with open("version.txt","w") as vers_file:
        vers_file.write("invalid?version")
    def teardown():
        if os.path.isfile("version.txt"):
            os.remove("version.txt")
    request.addfinalizer(teardown)
    return fixture_corrupt_vers

def test_check_corrupted_log(fixture_corrupt_log):
    """Test that checks for corrupted log error"""
    with pytest.raises(CorruptedFileWarning):
        with warnings.catch_warnings():
            warnings.simplefilter("error",category=CorruptedFileWarning)
            launch=Launcher("123","456")

def test_check_corrupted_vers(fixture_corrupt_vers):
    """Test that checks for corrupted version error"""
    with pytest.raises(CorruptedFileWarning):
        with warnings.catch_warnings():
            warnings.simplefilter("error",category=CorruptedFileWarning)
            launch=Launcher("123","456")

def test_invalid_updatedir():
    """Test that checks for invalid updatdir with multiple directories"""
    with pytest.raises(ValueError):
        launch=Launcher("123","456",newfiles="project.zip",
                        updatedir='downloads/extradir')

def test_invalid_multdir_newfiles():
    """Test that checks for invalid newfiles with multiple directories"""
    with pytest.raises(ValueError):
        launch=Launcher("123","456",newfiles="project.zip/hahaha")

def test_invalid_ext_newfiles():
    """Test that checks for invalid newfiles with wrong file extension"""
    Launcher("qwe","rty",newfiles='project.txt')

