Quickstart
==========

The core dependencies are

-  ``requests`` for retrieving updated versions
-  ``setuptools`` for archive manipulation and version comparison

To set up an initial version, you will need the following files:

-  Code file that creates launcher
-  Auxilliary code files passed into launcher
-  ``version.txt`` contains the version number.
-  ``filelist.txt`` contains a list of paths of the code and resource files.

Package these files into your application installer.
This is the initial version on the end user's computer.

To create new versions, copy the code files into a directory
and compress the directory into a
``.zip``, ``.tar.gz``, or a ``.tar.bz2`` archive.

Upload the archive to the server and place a file named ``version.txt``
containing the version number in the same directory as the archive.
The server directory should now look like this:

.. code-block:: text

  server-directory-pointed-to-by-url
  ├── project.zip
  └── version.txt

Pyautoupdate will then download the new version when performing updates
and replace the old code files with the new ones.

More details about the required files can be found in :doc:`project`.

This is a sample application initialization file, including an update check
before code execution.

.. code-block:: python

   import sys
   from pyautoupdate.launcher import Launcher

   # Update files before running
   launch.update()

   # Run code and return with exit code of launched code
   launch=Launcher("code_1.py","https://update-url")
   sys.exit(launch.run())

Replace ``https://update-url`` with the actual url of the folder on the server.
