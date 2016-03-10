from __future__ import absolute_import, print_function

import pytest
import os
from ..launcher import Launcher

class TestRunPID:
    
    @pytest.fixture(scope='class')
    def create_test_file_pid(self, request):
        filebase='test_run_base'
        filecode=filebase+'.py'
        code='import os\n'+'a=os.getpid()\n'+'b=os.getppid()\n'+\
             'c=pid\n'+'print("pid", a)\n'+'print("ppid",b)\n'+\
             'print("LauncherPid",c)\n'+'assert b==c\n'+'assert a!=c\n'
        with open(filecode, mode='w') as file:
            file.write(code)
        def teardown():
            os.remove(filecode)
        request.addfinalizer(teardown)
        return self.create_test_file_pid
    
    def test_run_PID(self,create_test_file_pid):
        filebase='test_run_base'
        filecode=filebase+'.py'
        l = Launcher(filecode,'')
        l.run()
