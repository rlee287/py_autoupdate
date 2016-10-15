from __future__ import absolute_import, print_function

import os
import pytest
from ..pyautoupdate.launcher import Launcher

@pytest.fixture(scope='function')
def create_update_dir(request):
    """Fixture that populates a downloads folder with a bunch of files"""
    os.mkdir('downloads')
    files=['tesfeo','fjfesf','fihghg']
    filedir=[os.path.join('downloads',fi) for fi in files]
    os.mkdir(os.path.join('downloads','subfolder'))
    filedir.append(os.path.join('downloads','subfolder','oweigjoewig'))
    for each_file in filedir:
        with open(each_file, mode='w') as new_file:
            new_file.write('')
    def teardown():
        for file_path in filedir:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                raise AssertionError#fail test if files exist
        os.rmdir('downloads')
    request.addfinalizer(teardown)
    return create_update_dir

def test_rm_dirs(create_update_dir):
    """Test that ensures that downloads folder is properly emptied"""
    launch = Launcher('all work and no play...','all play and no work...')
    launch._reset_update_files()
    assert os.path.isdir('downloads')
