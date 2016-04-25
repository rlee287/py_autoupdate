import os
import pytest

@pytest.fixture(scope='function')
def fixture_update_dir(request):
    def create_update_dir(version="0.0.1"):
        def teardown():
            if os.path.isfile('version.txt.old'):
                os.remove('version.txt.old')
            if os.path.isfile('version.txt'):
                os.remove('version.txt')
        request.addfinalizer(teardown)
        with open('version.txt', mode='w') as file:
            file.write(version)
        return fixture_update_dir
    return create_update_dir

