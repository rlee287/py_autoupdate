from __future__ import absolute_import, print_function

import os
import time
import pytest
from logging import INFO
from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import ProcessRunningException

class TestRunProgram:
    """Collection of tests that run programs with pyautoupdate"""

    @pytest.fixture(scope='class')
    def create_test_file(self, request):
        """Writes code files for tests and deletes them afterwards"""
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
        codepid='import os\n'+\
                'a=os.getpid()\n'+\
                'b=os.getppid()\n'+\
                'c=pid\n'+\
                'print("pid", a)\n'+\
                'print("ppid",b)\n'+\
                'print("LauncherPid",c)\n'+\
                'assert b==c\n'+\
                'assert a!=c\n'
        codefail='nonexistent_eiofjeoifjdoijfkldsjf'
        codeback='import time\n'+\
                 'print("start")\n'+\
                 'time.sleep(2)\n'+\
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

    def test_run(self,create_test_file):
        """Basic test that confirms that code will run"""
        filebase = 'test_run_base'
        filecode = filebase+'.py'
        filetext = filebase+'.txt'
        launch = Launcher(filecode,'Must','project.zip','downloads',INFO
                          "extra_args",extra="extra_kwargs")
        excode = launch.run()
        assert excode == 0
        with open(filetext,mode="r") as number_file:
            nums = number_file.read()
            assert nums == str([i**2 for i in range(20)])

    def test_run_pid(self,create_test_file):
        """Test that attempts to access attributes from the parent object"""
        filebase = 'test_run_base_pid'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'have')
        excode = launch.run()
        assert excode==0

    def test_run_fail(self,create_test_file):
        """Test that runs errored code and checks exit status"""
        filebase = 'test_run_base_fail'
        filecode = filebase+'.py'
        launch = Launcher(filecode,'URL')
        excode = launch.run()
        assert excode != 0

    def test_nofile(self):
        """Test that checks error thrown when file does not exist"""
        try:
            error_to_raise=FileNotFoundError
        except NameError:
            error_to_raise=IOError
        with pytest.raises(error_to_raise):
            launch = Launcher('does_not_exist_404.py','(in)sanity')
            excode = launch.run()

    def test_background(self):
        """Test that runs code in the background
        ASCII art depicting timeline shown below:
          0        1        2        3        4 seconds|
        --+--------+--------+--------+--------+--------+
          ^        ^        ^    ^       ^    ^        |Spawned
        "start"    |      "end"  |       |    |        |process
                   |             |Windows|    |        |-------
              "is_alive"         |Kills  | "is_dead"   |Test
                                 |Process|             |Checks

        """
        filebase = 'test_run_base'
        fileback = filebase+'_back'+'.py'
        launch = Launcher(fileback,'URL')
        process_handle = launch.run(True)
        time.sleep(1)
        assert launch.process_is_alive
        time.sleep(3)
        #Really takes at least 2 seconds for windows to kill process
        assert not launch.process_is_alive

    def test_run_twice(self):
        """Test that runs code in the background
        ASCII art depicting timeline shown below:
          0        1        2        3        4 seconds|
        --+--------+--------+--------+--------+--------+
          ^        ^        ^    ^       ^    ^        |Spawned
        "start"    |      "end"  |       |    |        |process
                   |             |Windows|    |        |-------
           "try_to_run_fail"     |Kills  | "run_twice" |Test
                                 |Process|             |Checks

        """
        filebase = 'test_run_base'
        fileback = filebase+'_back'+'.py'
        launch = Launcher(fileback,'URL')
        launch.run(True)
        time.sleep(1)
        #Process is still alive
        with pytest.raises(ProcessRunningException):
            launch.run(True)
        launch.process_join()
        #Process is dead now, can run again
        launch.run()
