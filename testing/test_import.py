import sys

class TestImportModules:
    def import_module(self,module_name):
        try:
            print("Importing {}".format(module_name))
            __import__(module_name)
            print("Imported {}".format(module_name))
        except:
            raise AssertionError("Unable to import {}".format(module_name))

    def test_import_all(self):
        module_name='py_autoupdate'
        submodules=[''];
        modulelist=list();
        for submodule in submodules:
            modulelist.append(module_name+submodule)
        for module in modulelist:
            # No need to raise error here
            # It is already raised in the import_module function
            __import__(module)

