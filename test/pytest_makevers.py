import os
import shutil
import pytest

from ..pyautoupdate.launcher import Launcher

@pytest.fixture(scope='function')
def fixture_update_dir(request):
    """Fixture that creates and tears down version.txt and log files"""
    def create_update_dir(version="0.0.1"):
        def teardown():
            if os.path.isfile(Launcher.version_check_log):
                os.remove(Launcher.version_check_log)
            if os.path.isfile(Launcher.version_doc):
                os.remove(Launcher.version_doc)
        request.addfinalizer(teardown)
        with open(Launcher.version_doc, mode='w') as version_file:
            version_file.write(version)
        return fixture_update_dir
    return create_update_dir

@pytest.fixture(scope='function')
def create_update_dir(request):
    """Fixture that tears down downloads directory"""
    def teardown():
        shutil.rmtree(Launcher.updatedir)
        os.remove(Launcher.version_check_log)
    request.addfinalizer(teardown)
    return create_update_dir
