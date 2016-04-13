from __future__ import absolute_import, print_function

import pytest
import os
import sys
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_update_dir(self, request):
        def teardown():
            if os.path.isdir('downloads'):
                os.rmdir('downloads')
        request.addfinalizer(teardown)
        return self.create_update_dir
    
    def test_rm_dirs(self,create_update_dir):
        l = Launcher('','')
        l._reset_update_dir()
        assert os.path.isdir('downloads')
