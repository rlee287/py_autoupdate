from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher

import os

import pytest

def test_check_urlslash():
    launch = Launcher('not here',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('why do I need to do this',
                       r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url

def test_check_emptyfilepath():
    with pytest.raises(ValueError):
        Launcher('','a url')

def test_check_emptyURL():
    with pytest.raises(ValueError):
        Launcher('a filepath','')

@pytest.fixture(scope="function")
def fixture_corrupt_log(request):
    with open("version_history.log","w") as log:
        log.write("invalid!gibberish")
    def teardown():
        if os.path.isfile("version_history.log"):
            os.remove("version_history.log")
    request.addfinalizer(teardown)
    return fixture_corrupt_log

@pytest.fixture(scope="function")
def fixture_corrupt_vers(request):
    with open("version.txt","w") as vers_file:
        vers_file.write("invalid?version")
    def teardown():
        if os.path.isfile("version.txt"):
            os.remove("version.txt")
    request.addfinalizer(teardown)
    return fixture_corrupt_vers

def test_check_corrupted_log(fixture_corrupt_log):
    launch=Launcher("123","456")

def test_check_corrupted_vers(fixture_corrupt_vers):
    launch=Launcher("123","456")
