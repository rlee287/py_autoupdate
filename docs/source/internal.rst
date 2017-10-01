Internal Update Procedure
=========================

The method :meth:`pyautoupdate.Launcher.update_code` performs the complete
update automatically. It has three parts: checking for updates,
retrieving the new versions, and applying the update.

Checking for Updates
--------------------

The method :meth:`pyautoupdate.Launcher.check_new` checks to see if an update
is available.

To check for new updates, the program sends a HTTP GET request for
``version.txt`` from the server. This file contains a version number formatted
as described in :pep:`440` and is compared with a locally stored version number.
The new version is saved into the file ``.queue``, and the request is logged
into ``version_check.log`` as described in :doc:`project`.

Retrieving New Versions
-----------------------

The method :meth:`pyautoupdate.Launcher._get_new` downloads the new version from
the server.

If the file ``.queue`` exists, the program sends a HTTP GET request for the
new archive. It then unpacks the archive into the download directory
``.pyautodownloads`` and removes the archive if it was extracted successfully.

Applying Updates
----------------

The method :meth:`pyautoupdate.Launcher._replace_files` replaces the existing
files with the new files from the server.

This method first acquires a lock to ensure that it does not blindly update
files that may be in use by the developer program. Then, it moves the code files
listed in ``filelist.txt`` into a temporary directory. It then copies the files
from ``.pyautodownloads`` into the existing directory and creates a new
``filelist.txt`` based on the new files. Finally, it removes the backups in the
temporary directory and releases the lock.
