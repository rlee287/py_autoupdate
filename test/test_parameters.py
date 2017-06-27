from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import CorruptedFileWarning
from .pytest_makevers import fixture_update_dir

import os
import warnings

import pytest

@pytest.fixture(scope='function')
def fixture_rm_log(request):
    """Fixture to remove pyautoupdate log on teardown"""
    def teardown():
        os.remove(Launcher.version_check_log)
    request.addfinalizer(teardown)

def test_check_urlslash(fixture_rm_log):
    """Test that checks that leading slash is properly added to URL"""
    launch = Launcher('not here',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('why do I need to do this',
                       r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url

def test_check_url_schema(fixture_rm_log):
    """Test that checks that leading slash is properly added to URL"""
    with pytest.raises(ValueError):
        Launcher('not here',
                 r'sftp://rlee287.github.io/pyautoupdate/testing/')

def test_check_url_noschema(fixture_rm_log):
    """Test that checks that leading slash is properly added to URL"""
    launch = Launcher('not here',
                      r'rlee287.github.io/pyautoupdate/testing/')
    assert launch.url == 'https://rlee287.github.io/pyautoupdate/testing/'

def test_check_emptyfilepath(fixture_rm_log):
    """Check that error is raised with empty file"""
    with pytest.raises(ValueError):
        Launcher('', 'a url')

def test_check_emptyURL(fixture_rm_log):
    """Check that error is raised with empty URL"""
    with pytest.raises(ValueError):
        Launcher('a filepath', '')

def test_check_escape_path(fixture_rm_log):
    """Check that error is raised when the path
       attempts to escape out of the folder"""
    with pytest.raises(ValueError):
        Launcher('../../../sandboxing/undocked/from/security/policies',
                 'wanna.cry.over.random.downloads')

def test_check_empty_version(fixture_update_dir):
    """Check that error is raised with empty version doc"""
    package = fixture_update_dir("")
    assert os.path.isfile(Launcher.version_doc)
    launch = Launcher('a filepath } 404', 'a URL that points nowhere')
    assert not launch.version_doc_validator()

@pytest.fixture(scope="function")
def fixture_corrupt_log(request):
    """Fixture that creates corrupted log"""
    with open(Launcher.version_check_log, "w") as log:
        log.write("invalid!gibberish")
    open(Launcher.version_doc, "w").close()
    def teardown():
        os.remove(Launcher.version_check_log)
        os.remove(Launcher.version_doc)
    request.addfinalizer(teardown)
    return fixture_corrupt_log

@pytest.fixture(scope="function")
def fixture_corrupt_vers(request):
    """Fixture that creates invalid version file"""
    with open(Launcher.version_doc, "w") as vers_file:
        vers_file.write("invalid?version")
    def teardown():
        if os.path.isfile(Launcher.version_doc):
            os.remove(Launcher.version_doc)
    request.addfinalizer(teardown)
    return fixture_corrupt_vers

def test_check_corrupted_log(fixture_corrupt_log):
    """Test that checks for corrupted log error"""
    with pytest.raises(CorruptedFileWarning):
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=CorruptedFileWarning)
            Launcher("123", "456")

def test_check_corrupted_vers(fixture_corrupt_vers):
    """Test that checks for corrupted version error"""
    with pytest.raises(CorruptedFileWarning):
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=CorruptedFileWarning)
            Launcher("123", "456")

def test_invalid_multdir_newfiles(fixture_rm_log):
    """Test that checks for invalid newfiles with multiple directories"""
    with pytest.raises(ValueError):
        Launcher("123", "456", newfiles="project.zip/hahaha")

def test_invalid_ext_newfiles(fixture_rm_log):
    """Test that checks for invalid newfiles with wrong file extension"""
    with pytest.raises(ValueError):
        Launcher("qwe", "rty", newfiles='project.txt')
