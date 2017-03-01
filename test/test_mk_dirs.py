from __future__ import absolute_import, print_function

from ..pyautoupdate.launcher import Launcher
from .pytest_makevers import create_update_dir
import os

def test_mk_dirs(create_update_dir):
    """Test that ensures that downlaods directory is created properly"""
    assert not os.path.isdir(Launcher.updatedir)
    launch = Launcher('MUST_HAVE_SOMETHING','urlurlurl')
    launch._reset_update_files()
    assert os.path.isdir(Launcher.updatedir)
