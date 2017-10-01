Quickstart
==========

Installing Dependencies
-----------------------

The core dependencies are

-  ``requests`` for retrieving updated versions
-  ``setuptools`` for archive manipulation and version comparison

Distributing the Application
----------------------------

To set up the installer, you will need the following files:

-  Code file that creates launcher
-  Auxilliary code files passed into launcher
-  ``version.txt`` that contains a :pep:`440` compliant version number
-  ``filelist.txt`` with a list of paths to the code and resource files

See :doc:`project` for a directory tree.

Package these files into your application installer.
This is the initial version on the end user's computer.

Pushing Updates to a Server
---------------------------

To create new versions, copy the code files into a directory
and compress the directory into a
``.zip``, ``.tar.gz``, or a ``.tar.bz2`` archive.

Upload the archive to the update server and place a file named ``version.txt``
containing the version number in the same directory as the archive.
The server directory should now look like this:

.. code-block:: text

  server-directory-pointed-to-by-url
  ├── project.zip
  └── version.txt

Pyautoupdate will then download the new version when performing updates
and replace the old code files with the new ones. It will modify the URL
as follows:

.. code-block:: text

  https://a_sample_website.com/ -> https://a_sample_website.com/project.zip
                                -> https://a_sample_website.com/version.txt

This is a sample application initialization file, including an update check
before code execution.

.. code-block:: python

   import sys
   from pyautoupdate.launcher import Launcher

   # Run code and return with exit code of launched code
   launch=Launcher("code_1.py","https://update-url")

   # Check for update before running
   need_update = launch.check_new()
   if need_update:
       # Prompt user for upgrade
       response = ""
       while response not in "yn":
           response=input("An update is available."
                          "Would you like to update? (y/n)")
       if response == "y":
           # Update code
           launch.update()
   # Run code
   sys.exit(launch.run())

Replace ``https://update-url`` with the actual url of the folder on the server.

.. note::

   You can call OS detection routines in the initialization file and use this
   to have different update URLs for different operating systems. This is
   useful for packaging OS dependent files.
