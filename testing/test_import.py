from __future__ import absolute_import, print_function

import pytest

class TestImportModules:
    @pytest.mark.tryfirst
    def test_import_all(self):
        module_name='pyautoupdate'
        submodules=['launcher']
        modulelist=[module_name]
        for submodule in submodules:
            modulelist.append(module_name+'.'+submodule)
        for module in modulelist:
            #Attempt to import all modules
            __import__(module)

