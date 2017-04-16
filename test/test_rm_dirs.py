from __future__ import absolute_import, print_function

import os
import sys

import pytest
from ..pyautoupdate.launcher import Launcher

@pytest.fixture(scope='function')
def create_update_dir(request):
    """Fixture that populates a downloads folder with a bunch of files,
       including the project.zip file
    """
    os.mkdir(Launcher.updatedir)
    files=['tesfeo','fjfesf','fihghg']
    filedir=[os.path.join(Launcher.updatedir,fi) for fi in files]
    os.mkdir(os.path.join(Launcher.updatedir,'subfolder'))
    filedir.append(os.path.join(Launcher.updatedir,'subfolder','oweigjoewig'))
    if sys.version_info[0]==2:
        empty_zip_data = 'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'+\
                         '\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    else:
        empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00'+\
                         b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    with open('project.zip', 'wb') as zip_file:
        zip_file.write(empty_zip_data)
    for each_file in filedir:
        with open(each_file, mode='w') as new_file:
            new_file.write('')
    def teardown():
        for file_path in filedir:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # Perhaps move into main test?
                raise AssertionError# fail test if files exist
        os.rmdir(Launcher.updatedir)
        os.remove(Launcher.version_check_log)
        if os.path.isfile("project.zip"):
            os.remove("project.zip")
    request.addfinalizer(teardown)
    return create_update_dir

def test_rm_dirs(create_update_dir):
    """Test that ensures that downloads folder is properly emptied"""
    assert os.path.isfile("project.zip")
    launch = Launcher('all work and no play...','all play and no work...')
    launch._reset_update_files()
    assert os.path.isdir(Launcher.updatedir)
    # Check that directory is empty
    assert len(os.listdir(Launcher.updatedir))==0
    assert not os.path.isfile("project.zip")
