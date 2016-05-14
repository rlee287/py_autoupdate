from __future__ import absolute_import, print_function

import os
import pytest
from ..pyautoupdate.launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='class')
    def create_test_file(self, request):
        filebase='test_run_base'
        filecode=filebase+'.py'
        filetext=filebase+'.txt'
        filepid=filebase+'_pid'+'.py'
        filefail=filebase+'_fail'+'.py'
        codebasic='with open("'+filetext+'", mode="w") as number_file:\n'+\
        '    l=[i**2 for i in range(20)]\n'+\
        '    number_file.write(str(l))\n'+\
        'print(update)\n'+\
        'update.set()\n'+\
        'print(update.is_set())\n'+\
        'update.clear()\n'+\
        'print(update.is_set())'
        codepid='import os\n'+'a=os.getpid()\n'+'b=os.getppid()\n'+\
             'c=pid\n'+'print("pid", a)\n'+'print("ppid",b)\n'+\
             'print("LauncherPid",c)\n'+'assert b==c\n'+'assert a!=c\n'
        codefail='nonexistent_eiofjeoifjdoijfkldsjf'
        with open(filecode, mode='w') as code_file:
            code_file.write(codebasic)
        with open(filepid, mode='w') as code_file:
            code_file.write(codepid)
        with open(filefail, mode='w') as code_file:
            code_file.write(codefail)
        def teardown():
            os.remove(filecode)
            os.remove(filetext)
            os.remove(filepid)
            os.remove(filefail)
        request.addfinalizer(teardown)
        return self.create_test_file
    
    def test_run(self,create_test_file):
        filebase = 'test_run_base'
        filecode = filebase+'.py'
        filetext = filebase+'.txt'
        launch = Launcher(filecode,'')
        excode = launch.run()
        assert excode == 0
        with open(filetext,mode="r") as number_file:
            nums = number_file.read()
            assert nums == str([i**2 for i in range(20)])

    def test_run_pid(self,create_test_file):
        filebase = 'test_run_base_pid'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'')
        excode = launch.run()
        assert excode==0

    def test_run_fail(self,create_test_file):
        filebase = 'test_run_base_fail'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'')
        excode = launch.run()
        assert excode != 0

    def test_nofile(self):
        launch = Launcher('does_not_exist_404j958458ryeiu.py','')
        excode = launch.run()
        assert excode != 0

