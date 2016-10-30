import os
import shutil
import pytest

from ..pyautoupdate.launcher import Launcher

@pytest.fixture(scope='function')
def fixture_update_dir(request):
    """Fixture that creates and tears down a version.txt file"""
    def create_update_dir(version="0.0.1"):
        def teardown():
            if os.path.isfile('version_history.log'):
                os.remove('version_history.log')
            if os.path.isfile('version.txt'):
                os.remove('version.txt')
        request.addfinalizer(teardown)
        with open('version.txt', mode='w') as version_file:
            version_file.write(version)
        return fixture_update_dir
    return create_update_dir

@pytest.fixture(scope='function')
def create_update_dir(request):
    """Fixture that tears down downloads directory"""
    def teardown():
        shutil.rmtree('downloads')
        os.remove(Launcher.version_check_log)
    request.addfinalizer(teardown)
    return create_update_dir
