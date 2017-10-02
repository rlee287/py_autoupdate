Project Structure
=================

Overall Structure
-----------------

The files in the directory tree below are labeled as follows:

+------+-----------------------------+
|Symbol|Meaning                      |
+======+=============================+
|**RE**|Required for each new version|
+------+-----------------------------+
|**RF**|Required the first time      |
+------+-----------------------------+
|**R** |Reserved file names          |
+------+-----------------------------+

.. code-block:: text

  Root directory of project
  ├── <general code files>
  ├── .pyautodownloads/ **R**
  ├── <an entry point file that creates the launcher object>
  ├── filelist.txt **RF**
  ├── project.zip (can be changed) **R**
  ├── version.txt **RE**
  └── version_check.log **R**

The code starts from an entry point file that initializes the
:class:`Launcher` object.

.. note ::
   The entry point file currently cannot be replaced by the update process.
   While this functionality may be added in a future version, please try to
   avoid making changes that would require updating the entry point file.

Special Files
-------------

filelist.txt
************
This file contains the list of files to be removed after the update process.

project.zip (or equivalent)
***************************
This is the downloaded archive containing the new files.

.pyautodownloads/
*****************
This temporary directory contains the downloaded new files. The directory will
be emptied after the update.

version.txt
***********
This file contains a :pep:`440` version number for the code.
The local copy is compared with the server version to check if an update is
necessary.

version_check.log
*****************
This file records when the server was contacted to check for updates.
Each line has one of the following formats::

  |Old <old version number>|New <new version number>|Time <timestamp>
  |Old <old version number>|Up to date|Time <timestamp>
  |Old <old version number>|Server Invalid|Time <timestamp>
