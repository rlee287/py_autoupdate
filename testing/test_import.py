from __future__ import absolute_import, print_function

import pytest

@pytest.mark.tryfirst
def test_import_all():
    module_name='pyautoupdate'
    submodules=['launcher']
    modulelist=[module_name]
    for submodule in submodules:
        modulelist.append(module_name+'.'+submodule)
    for module in modulelist:
        #Attempt to import all modules
        __import__(module)

