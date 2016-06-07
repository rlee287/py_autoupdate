Description of tests
====================

-  ``pytest_skipif``: fixture to skip tests that require internet access
-  ``pytest_makevers``: functions to create the version files for tests
-  ``test_mk_dirs``: test that the update mechanism can create a
   downloads folder
-  ``test_rm_dirs``: test that the update mechanism can clean up a
   downloads folder
-  ``test_update``: Check that it can recognize when to update code
-  ``test_no_update``: Check that it won’t update when it doesn’t need
   to
-  ``test_nourl_update``: Check that update operations will fail when
   the target url does not have a version file
-  ``test_run``: Check that wrapped code can be launched successfully
