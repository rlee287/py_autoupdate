import pytest
import os
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='session')
    def create_test_file(self, request):
        filebase='codetemp'
        filecode=filebase+'.py'
        filetext=filebase+'.txt'
        code='with open("'+filetext+'", mode="w") as file:\n'+\
        '    l=[i**2 for i in range(20)]\n'+\
        '    file.write(str(l))\n'
        with open(filecode, mode='w') as file:
            file.write(code)
        def teardown():
            try:
                os.remove(filecode)
                os.remove(filetext)
            except (FileNotFoundError, OSError):
                raise AssertionError # fail test here
        request.addfinalizer(teardown)
        return self.create_test_file
    
    def test_run(self,create_test_file):
        filebase='codetemp'
        filecode=filebase+'.py'
        filetext=filebase+'.txt'
        l = Launcher(filecode,'')
        l.run()
        with open(filetext,mode="r") as file:
            s=file.read()
            assert s==str([i**2 for i in range(20)])
