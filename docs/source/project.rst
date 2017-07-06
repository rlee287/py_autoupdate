Project Structure
=================

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
  ├── <an entry point file that creates the launcher>
  ├── filelist.txt **RF**
  ├── project.zip (can be changed) **R**
  ├── subfolder/
  │   └── code_3.py
  ├── version.txt **RE**
  └── version_history.log **R**

The code starts from an entry point file that initializes the
:class:`Launcher` object.

.. note ::
   The entry point file can be updated via renaming
   while in use. This is in development but is known to be possible.

``version.txt``
***************
This file contains a version number for the code.
It is used to as a comparison to check for newer versions.

``version_history.log``
***********************
This file records when update checking occured.
The format is one of the following::

  |Old <old version number>|New <new version number>|Time <timestamp>
  |Old <old version number>|Up to date|Time <timestamp>
  |Old <old version number>|Server Invalid|Time <timestamp>
