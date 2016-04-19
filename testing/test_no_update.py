from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
import os
import pytest

from .pytest_skipif import needinternet

class TestRunProgram:
    @pytest.fixture(scope='class')
    def create_update_dir(self, request):
        def teardown():
            if os.path.isfile('version.txt.old'):
                os.remove('version.txt.old')
            if os.path.isfile('version.txt'):
                os.remove('version.txt')
        request.addfinalizer(teardown)
        with open('version.txt', mode='w') as file:
            file.write("0.2.0")
        return self.create_update_dir
    
    @needinternet
    def test_check_vers_noupdate(self,create_update_dir):
        launch = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing/')
        isnew=launch._check_new()
        assert not isnew
