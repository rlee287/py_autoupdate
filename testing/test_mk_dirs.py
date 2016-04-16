from __future__ import absolute_import, print_function

from ..launcher import Launcher
import os
import pytest

@pytest.fixture(scope='function')
def create_update_dir(request):
    def teardown():
        if os.path.isdir('downloads'):
            os.rmdir('downloads')
    request.addfinalizer(teardown)
    return create_update_dir

def test_mk_dirs(create_update_dir):
    launch = Launcher('','')
    launch._reset_update_dir()
    assert os.path.isdir('downloads')
