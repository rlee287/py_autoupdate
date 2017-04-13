Quickstart
==========

To set up an initial version, you will need the following files:

-  ``code_1.py``
-  ``code_2.py``
-  ``entry_point.py``
-  ``version.txt`` contains the version number.
-  ``filelist.txt`` contains a list of paths of the code and resource files.

Install these files into the user's location when first starting.

To create the server versions, replicate code files and the layout
in a directory and compress the directory into a
``.zip``, ``.tar.gz``, or a ``.tar.bz2`` archive.

Upload the archive to the server and place a ``version.txt``
containing the version number in the same direcotry as the archive.

More details about the required files can be found in :doc:`project`.

This is a sample ``entry_point.py`` file.py, including an update check
before code execution.

.. code-block:: python

   import sys
   from pyautoupdate.launcher import Launcher

   # Update files before running
   launch.update()

   # Run code and return with exit code of launched code
   launch=Launcher("code_1.py","https://update-url")
   sys.exit(launch.run())

Replace the ``https://update-url`` with the actual url of the folder on the server.
