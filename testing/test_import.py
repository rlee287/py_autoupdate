from __future__ import absolute_import, print_function

import sys

class TestImportModules:
    def test_import_all(self):
        module_name='pyautoupdate'
        submodules=['launcher']
        modulelist=[module_name]
        for submodule in submodules:
            modulelist.append(module_name+'.'+submodule)
        for module in modulelist:
            # No need to raise error here
            # It is already raised in the import_module function
            __import__(module)

