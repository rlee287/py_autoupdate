import pytest
import os
from ..launcher import Launcher

class TestRunProgram:
    
    @pytest.fixture(scope='module')
    def create_test_file(self, request):
        code='''
        print([i**2 for i in range(20)])
        '''
        filepath=os.path.join('..','test_code.py')
        with open(filepath, mode='w') as file:
            file.write(code)
        def teardown():
            os.remove(filepath)
        request.addfinalizer(teardown)
        return create_test_file
    
    def test_run(self):
        l = Launcher(os.path.join('..','test_code.py'),'')
        l.run()
