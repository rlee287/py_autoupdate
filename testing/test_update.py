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
                if os.path.isfile(os.path.join('downloads','version.txt.old')):
                    os.remove(os.path.join('downloads','version.txt.old'))
                if os.path.isdir('downloads'):
                    os.rmdir('downloads')
            except Exception as e:
                print(e, file=sys.stderr)
                raise AssertionError
        request.addfinalizer(teardown)
        os.mkdir('downloads')
        with open(os.path.join('downloads','version.txt'), mode='w') as file:
            file.write("0.0.1")
        return self.create_update_dir
    
    def test_check_vers(self,create_update_dir):
        l = Launcher('',r'http://rlee287.github.io/py_autoupdate/testing/')
        isnew=l._check_new()
        assert isnew
