from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
import os
import pytest

@pytest.fixture(scope='function')
def create_update_dir(request):
    """Fixture that tears down downloads directory"""
    def teardown():
        os.rmdir('downloads')
    request.addfinalizer(teardown)
    return create_update_dir

def test_mk_dirs(create_update_dir):
    """Test that ensures that downlaods directory is created properly"""
    launch = Launcher('MUST_HAVE_SOMETHING','urlurlurl')
    launch._reset_update_dir()
    assert os.path.isdir('downloads')
    print(os.path.abspath('downloads'))
    del launch
