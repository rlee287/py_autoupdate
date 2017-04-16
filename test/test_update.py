from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_skipif import needinternet

from logging import DEBUG
import os
import shutil

import pytest

@pytest.fixture(scope='function')
def fixture_update_setup(request):
    """Sets up and tears down version docs and code files"""
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
        if os.path.isfile(Launcher.queue_update):
            os.remove(Launcher.queue_update)
    request.addfinalizer(teardown)
    with open('version.txt', mode='w') as version_file:
        version_file.write("0.0.1")
    os.mkdir("extradir")
    with open(os.path.join("extradir", "blah.py"), mode='w') as code:
        code.write("import time\n"
                   "import os\n"
                   "print('This is the old version')\n"
                   "q=open('.lck','w')\n"
                   "time.sleep(1)\n"
                   "q.close()\n"
                   "os.remove('.lck')\n")
    with open(os.path.join("extradir","dummy.txt"), mode='w') as extra_file:
        extra_file.write("1984: 2+2=5")
    with open(Launcher.file_list, mode='w') as filelist:
        filelist.write("extradir/blah.py")
    return fixture_update_setup

@pytest.mark.trylast
@needinternet
def test_update(fixture_update_setup):
    """Checks the ability of program to upload new code"""
    assert os.path.isfile(Launcher.file_list)
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing/',
                      'project.zip',DEBUG)
    could_update=launch.update_code()
    assert could_update
    assert not os.path.isfile(Launcher.queue_update)
    assert os.path.isfile("extradir/blah.py")
    with open(os.path.abspath("extradir/blah.py"), "r") as file_code:
        file_text=file_code.read()
    assert "new version" in file_text
    assert os.path.isfile(Launcher.file_list)
    excode=launch.run()
    assert excode==0

@pytest.mark.trylast
@needinternet
def test_run_lock_update(fixture_update_setup):
    """Checks the ability of program to upload new code"""
    assert os.path.isfile(Launcher.file_list)
    launch = Launcher('extradir/blah.py',
                      r'http://rlee287.github.io/pyautoupdate/'
                      '_static/testing/',
                      'project.zip',DEBUG)
    launch.run(True)
    while not launch.process_code_running:
        pass
    could_update_while_run=launch.update_code()
    assert not could_update_while_run
    launch.process_join()
    assert launch.process_exitcode==0
    could_update=launch.update_code()
    assert could_update
    assert not os.path.isfile(Launcher.queue_update)
    assert not os.path.isfile(Launcher.queue_replace)
    assert os.path.isfile("extradir/blah.py")
