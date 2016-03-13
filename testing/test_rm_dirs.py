from __future__ import absolute_import, print_function

import pytest
import os
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_update_dir(self, request):
        os.mkdir('downloads')
        files=['tesfeo','fjfesf','fihghg']
        filedir=[os.path.join('downloads',fi) for fi in files]
        for each_file in filedir:
            with open(each_file, mode='w') as file:
                file.write('')
        def teardown():
            for files in filedir:
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        raise AssertionError#fail test if files exist
                except Exception as e:
                    print(e, file=sys.stderr)
        request.addfinalizer(teardown)
        return self.create_update_dir
    
    def test_run(self,create_update_dir):
        l = Launcher('','')
        l._reset_update_dir()
