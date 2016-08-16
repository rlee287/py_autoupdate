.. pyautoupdate documentation master file, created by
   sphinx-quickstart on Wed May 18 10:03:49 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pyautoupdate's documentation!
========================================

Pyautoupdate is a module that allows code to automatically update.
Developers can focus on developing their application and use
Pyautoupdate to easily ensure that the copy of the code on the end
user's computer remains updated.

Example code using Pyautoupdate:

.. code-block:: python

   import pyautoupdate

   # Run code
   launch=Launcher("~/example/application_init.py","https://update-url")
   excode=launch.run()

   # Update files
   launch.update()

Contents:

.. toctree::
   :maxdepth: 2

   pyautoupdate


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
