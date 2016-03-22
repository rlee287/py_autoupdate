from __future__ import absolute_import, print_function

import pytest
import os
import sys
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_update_dir(self, request):
        def teardown():
            try:
                if os.path.isfile('version.txt.old'):
                    os.remove('version.txt.old')
            except Exception as e:
                print(e, file=sys.stderr)
                raise AssertionError
        request.addfinalizer(teardown)
        with open('version.txt', mode='w') as file:
            file.write("0.0.1")
        return self.create_update_dir
    
    def test_check_vers(self,create_update_dir):
        l = Launcher('',r'http://rlee287.github.io/py_autoupdate/testing/')
        isnew=l._check_new()
        assert isnew
