Quickstart
==========


To set up an initial version, you will need the following files:

-  ``code_1.py``
-  ``code_2.py``
-  ``entry_point.py``
-  ``version.txt``
-  ``filelist.txt``

Install these files into the user's location when first starting.

To create the server versions, take these files:

-  ``code_1.py``
-  ``code_2.py``
-  ``entry_point.py``
-  ``version.txt``

And put them into a ``.zip``, ``.tar.gz``, or a ``.tar.bz2`` archive.

More details about the required files can be found in :doc:`project`.

Upload the archive to your server and make note of the url of its containing folder.

This is a sample ``entry_point.py`` file.py, including an update check before code execution.

.. code-block:: python

   from pyautoupdate.launcher import Launcher

   # Update files before running
   launch.update()

   # Run code
   launch=Launcher("code_1.py","https://update-url")
   excode=launch.run()
