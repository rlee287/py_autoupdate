from __future__ import absolute_import, print_function

import pytest
import os
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_test_file(self, request):
        filebase='test_run_base'
        filecode=filebase+'.py'
        code='import os\n'+'a=os.getpid()\n'+'b=os.getppid()\n'+\
             'c=os.getpid()\n'+'assert a==b\n'+'assert a!=c\n'
        with open(filecode, mode='w') as file:
            file.write(code)
        def teardown():
            os.remove(filecode)
        request.addfinalizer(teardown)
        return self.create_test_file
    
    def test_run(self,create_test_file):
        filebase='codetemp'
        filecode=filebase+'.py'
        l = Launcher(filecode,'')
        l.run()
