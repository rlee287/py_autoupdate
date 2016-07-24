from __future__ import absolute_import, print_function

import os
import time
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
        fileback=filebase+'_back'+'.py'
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
        codeback='import time\n'+'print("start")\n'+'time.sleep(2)\n'+\
             'print("end")'
        for name,code in zip([filecode, filepid, filefail, fileback],
                             [codebasic, codepid, codefail, codeback]):
            with open(name, mode='w') as code_file:
                code_file.write(code)
        def teardown():
            for name in [filecode, filetext, filepid, filefail, fileback]:
                os.remove(name)
        request.addfinalizer(teardown)
        return self.create_test_file

    @staticmethod
    def test_run(create_test_file):
        filebase = 'test_run_base'
        filecode = filebase+'.py'
        filetext = filebase+'.txt'
        launch = Launcher(filecode,'Must')
        excode = launch.run()
        assert excode == 0
        with open(filetext,mode="r") as number_file:
            nums = number_file.read()
            assert nums == str([i**2 for i in range(20)])

    @staticmethod
    def test_run_pid(create_test_file):
        filebase = 'test_run_base_pid'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'have')
        excode = launch.run()
        assert excode==0

    @staticmethod
    def test_run_fail(create_test_file):
        filebase = 'test_run_base_fail'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'URL')
        excode = launch.run()
        assert excode != 0

    @staticmethod
    def test_nofile():
        launch = Launcher('does_not_exist_404j958458ryeiu.py','(in)sanity')
        excode = launch.run()
        assert excode != 0

#    @staticmethod
#    def test_background():
#        filebase = 'test_run_base'
#        fileback = filebase+'_back'+'.py'
#        launch = Launcher(fileback,'URL')
#        process_handle = launch.run(True)
#        time.sleep(1)
#        assert process_handle.is_alive()
#        time.sleep(2)
#        assert not process_handle.is_alive()
#        process_handle.join()
