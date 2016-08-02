from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher

import pytest

def test_check_urlslash():
    """Test that checks that leading slash is properly added to URL"""
    launch = Launcher('not here',
                      r'http://rlee287.github.io/pyautoupdate/testing/')
    launch2 = Launcher('why do I need to do this',
                       r'http://rlee287.github.io/pyautoupdate/testing')
    assert launch.url == launch2.url

def test_check_emptyfilepath():
    """Check for error when filepath is missing"""
    with pytest.raises(ValueError):
        Launcher('','a url')

def test_check_emptyURL():
    """Check for error when URL is missing"""
    with pytest.raises(ValueError):
        Launcher('a filepath','')
