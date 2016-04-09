from __future__ import absolute_import, print_function

import pytest
import os
import sys
from ..launcher import Launcher
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
            file.write("0.0.1")
        return self.create_update_dir
    
    @needinternet
    def test_check_vers_update(self,create_update_dir):
        print(needinternet)
        l = Launcher('',r'http://rlee287.github.io/pyautoupdate/testing/')
        isnew=l._check_new()
        assert isnew
