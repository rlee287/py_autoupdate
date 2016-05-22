|pyautoupdate_logo|

``py_autoupdate`` is a python wrapper that allows the wrapped code to
automatically update.

|Build_Status|

**Note: This is pre-alpha code. The update functionality does not work
yet.**

Advantages
----------

-  This module is written in pure python. **This means that there is no
   need to have a C compiler to use this module.**
-  pyautoupdate works with both python 2 and 3
-  pypy and pypy3 can also be used

Dependencies
------------

-  For python 2, python 2.6 or later is required
-  For python 3, python 3.3 or later is required
-  ``requests`` for retrieving updated versions
-  ``pytest`` for running the tests
-  ``pytest_cov`` to measure coverage
-  ``pylint`` for code style checks

License
-------

LGPL 2.1

.. |pyautoupdate_logo| image:: https://cloud.githubusercontent.com/assets/14067959/13902076/25e8305e-edf7-11e5-873c-8a4e0fc2780f.png
.. |Build_Status| image:: https://travis-ci.org/rlee287/pyautoupdate.svg?branch=develop
   :target: https://travis-ci.org/rlee287/pyautoupdate
