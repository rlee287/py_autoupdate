from __future__ import absolute_import, print_function

import os
import time
import pytest
from logging import INFO, DEBUG
from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import ProcessRunningException

class TestRunProgram(object):
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
        filelog=filebase+'_log'+'.py'
        codebasic='import pprint\n'+\
        'pprint.pprint(locals())\n'+\
        'with open("'+filetext+'", mode="w") as number_file:\n'+\
        '    l=[i**2 for i in range(20)]\n'+\
        '    number_file.write(str(l))\n'
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
                 'import os\n'+\
                 'open(".lck","w").close()\n'+\
                 'print("start")\n'+\
                 'time.sleep(2)\n'+\
                 'print("end")\n'+\
                 'os.remove(".lck")\n'
        codelog='log.error("This should be an error")\n'
        for name,code in zip([filecode, filepid, filefail,
                              fileback, filelog],
                             [codebasic, codepid, codefail,
                              codeback, codelog]):
            with open(name, mode='w') as code_file:
                code_file.write(code)
        def teardown():
            for name in [filecode, filetext, filepid,
                         filefail, fileback, filelog]:
                if os.path.isfile(name):
                    os.remove(name)
            os.remove(Launcher.version_check_log)
        request.addfinalizer(teardown)
        return self.create_test_file

    def test_run(self,create_test_file):
        """Basic test that confirms that code will run"""
        filebase = 'test_run_base'
        filecode = filebase+'.py'
        filetext = filebase+'.txt'
        launch = Launcher(filecode,'Must','project.zip',DEBUG,
                          "extra_args",extra="extra_kwargs")
        excode = launch.run()
        assert excode == 0
        with open(filetext,mode="r") as number_file:
            nums = number_file.read()
            assert nums == str([i**2 for i in range(20)])

    def test_run_pid(self,create_test_file):
        """Test that attempts to access attributes from the parent object"""
        filecode = 'test_run_base_pid.py'
        launch = Launcher(filecode,'have')
        excode = launch.run()
        assert excode==0

    def test_terminante_notrun(self,create_test_file):
        """Test that attempts to access attributes from the parent object"""
        filecode = 'test_run_base_pid.py'
        launch = Launcher(filecode,'have')
        excode = launch.run()
        assert excode==0
        can_terminate=launch.process_terminate()
        assert not can_terminate

    def test_run_fail(self,create_test_file):
        """Test that runs errored code and checks exit status"""
        filecode = 'test_run_base_fail.py'
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
            launch.run()

    def test_run_log(self):
        """Test that attempts to access attributes from the parent object"""
        filelog = 'test_run_base_log.py'
        launch = Launcher(filelog,'logs made out of wood!')
        excode = launch.run()
        assert excode==0

    def test_terminate_running(self):
        """Test that attempts to terminate process"""
        fileback = "test_run_base_back.py"
        launch = Launcher(fileback,"NonUniform Resource Locator",
                          'project.zip',DEBUG)
        launch.run(True)
        print("Entering busyloop")
        while not launch.process_code_running:
            pass
        print("Exiting busyloop")
        time.sleep(0.5)
        can_terminate=launch.process_terminate()
        os.remove(".lck")
        assert launch.process_exitcode==-15
        assert can_terminate

    @pytest.mark.xfail(reason="Produces none but should be 0")
    def test_terminate_rerun(self):
        """Test that attempts to rerun process after termination"""
        fileback = "test_run_base_back.py"
        launch = Launcher(fileback,"NonUniform Resource Locator",
                          'project.zip',DEBUG)
        launch.run(True)
        print(id(launch._Launcher__process))
        print("Entering busyloop")
        while not launch.process_code_running:
            pass
        print("Exiting busyloop")
        time.sleep(0.5)
        can_terminate=launch.process_terminate()
        os.remove(".lck")
        assert launch.process_exitcode==-15
        assert can_terminate
        exitcode=launch.run(True)
        print(id(launch._Launcher__process))
        launch.process_join()
        assert exitcode==0

    def test_background(self):
        """Test that runs code in the background.
        
        ASCII art depicting timeline shown below:
          0        1        2        3        4 seconds|
        --+--------+--------+--------+--------+--------+
          ^        ^        ^    ^       ^    ^        |Spawned
        "start"    |      "end"  |       |    |        |process
                   |             |Windows|    |        |-------
              "is_alive"         |Kills  | "is_dead"   |Test
                                 |Process|             |Checks
        """
        fileback = 'test_run_base_back.py'
        launch = Launcher(fileback,'URL')
        launch.run(True)
        time.sleep(1)
        assert launch.process_is_alive
        launch.process_join(timeout=5)
        # Really takes up to 5 seconds for windows to kill process
        assert not launch.process_is_alive

    def test_run_twice(self):
        """Test that runs code in the background twice.
        
        ASCII art depicting timeline shown below:
          0        1        2        3        4 seconds|
        --+--------+--------+--------+--------+--------+
          ^        ^        ^    ^       ^    ^        |Spawned
        "start"    |      "end"  |       |    |        |process
                   |             |Windows|    |        |-------
           "try_to_run_fail"     |Kills  | "run_twice" |Test
                                 |Process|             |Checks

        """
        filetwice = 'test_run_base_back.py'
        launch = Launcher(filetwice,'URL')
        launch.run(True)
        time.sleep(1)
        #Process is still alive
        with pytest.raises(ProcessRunningException):
            launch.run(True)
        launch.process_join()
        #Process is dead now, can run again
        launch.run()
