from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from ..pyautoupdate.exceptions import CorruptedFileWarning

from logging import DEBUG
import os
import shutil
import warnings

import pytest

@pytest.fixture(scope='function')
def fixture_update_setup(request):
    """Sets up and tears down version docs and code files"""
    def update_setup(add_extraneous=False):
        def teardown():
            if os.path.isfile(Launcher.version_check_log):
                os.remove(Launcher.version_check_log)
            if os.path.isfile(Launcher.version_doc):
                os.remove(Launcher.version_doc)
            if os.path.isdir("extradir"):
                shutil.rmtree("extradir")
            if os.path.isfile(Launcher.file_list):
                os.remove(Launcher.file_list)
            if os.path.isdir(Launcher.updatedir):
                shutil.rmtree(Launcher.updatedir)
        request.addfinalizer(teardown)
        # Write old version file
        with open(Launcher.version_doc, mode='w') as version_file:
            version_file.write("0.0.1")
        # Write new version file
        with open(Launcher.queue_update, mode='w') as new_version:
            new_version.write("0.1.0")
        # Create old files
        os.mkdir("extradir")
        os.makedirs(os.path.join(Launcher.updatedir, "extradir"))
        extradir_blah = os.path.join("extradir", "blah.py")
        extradir_dummy = os.path.join("extradir", "dummy.txt")
        downloads_extradir_blah = os.path.join(Launcher.updatedir, "extradir",
                                               "blah.py")
        with open(extradir_blah, mode='w') as code:
            code.write("print('This is the old version')")
        with open(extradir_dummy, mode='w') as extra_file:
            extra_file.write("1984: 2+2=5")
        with open(downloads_extradir_blah, mode='w') as new_code:
            new_code.write("print('This is the new version')")
        # Create old filelist
        list_files = [extradir_blah+"\n", extradir_dummy+"\n"]
        if add_extraneous:
            list_files.append("shine/johnny.txt\n")
        with open(Launcher.file_list, mode='w') as filelist:
            filelist.writelines(list_files)
        return fixture_update_setup
    return update_setup

def test_replace_files(fixture_update_setup):
    """Checks the ability of program to replace the code"""
    package = fixture_update_setup(False)
    assert os.path.isfile(Launcher.file_list)
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/testing/',
                      'project.zip', DEBUG)
    with warnings.catch_warnings():
        warnings.simplefilter("error", category=CorruptedFileWarning)
        # Should not be a warning here
        can_replace = launch._replace_files()
    assert can_replace
    assert os.path.isfile("extradir/blah.py")
    with open(os.path.abspath("extradir/blah.py"), "r") as file_code:
        file_text = file_code.read()
    assert "new version" in file_text
    assert os.path.isfile(Launcher.file_list)
    assert not os.path.isfile(Launcher.queue_update)

def test_replace_files_extraneous(fixture_update_setup):
    """Checks the ability of program to replace the code
       with an extraneous file listed in the old filelist
    """
    package = fixture_update_setup(True)
    assert os.path.isfile(Launcher.file_list)
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/testing/',
                      'project.zip', DEBUG)
    with pytest.warns(CorruptedFileWarning):
        can_replace = launch._replace_files()
    assert can_replace
    assert os.path.isfile("extradir/blah.py")
    with open(os.path.abspath("extradir/blah.py"), "r") as file_code:
        file_text = file_code.read()
    assert "new version" in file_text
    assert os.path.isfile(Launcher.file_list)
    assert not os.path.isfile(Launcher.queue_update)

def test_no_replace_files():
    """Checks that the replace code function returns false when
       there are no files to replace
    """
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/testing/',
                      'project.zip', DEBUG)
    can_replace = launch._replace_files()
    assert not can_replace
