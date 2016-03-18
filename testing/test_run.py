from __future__ import absolute_import, print_function

import pytest
import os
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_test_file(self, request):
        filebase='test_run_base'
        filecode=filebase+'.py'
        filetext=filebase+'.txt'
        filepid=filebase+'_pid'+'.py'
        code='with open("'+filetext+'", mode="w") as file:\n'+\
        '    l=[i**2 for i in range(20)]\n'+\
        '    file.write(str(l))\n'+\
        'print(locals())'
        codepid='import os\n'+'a=os.getpid()\n'+'b=os.getppid()\n'+\
             'c=pid\n'+'print("pid", a)\n'+'print("ppid",b)\n'+\
             'print("LauncherPid",c)\n'+'assert b==c\n'+'assert a!=c\n'
        with open(filecode, mode='w') as file:
            file.write(code)
        with open(filepid, mode='w') as file:
            file.write(codepid)
        def teardown():
            os.remove(filecode)
            os.remove(filetext)
            os.remove(filepid)
        request.addfinalizer(teardown)
        return self.create_test_file
    
    def test_run(self,create_test_file):
        filebase='test_run_base'
        filecode=filebase+'.py'
        filetext=filebase+'.txt'
        l = Launcher(filecode,'')
        excode=l.run()
        assert excode==0        
        with open(filetext,mode="r") as file:
            s=file.read()
            assert s==str([i**2 for i in range(20)])
    
    def test_run_pid(self,create_test_file):
        filebase='test_run_base_pid'
        filecode=filebase+'.py'
        l = Launcher(filecode,'')
        excode=l.run()
        assert excode==0

