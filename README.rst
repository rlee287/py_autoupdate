|pyautoupdate_logo|

``pyautoupdate`` is a python wrapper that allows the wrapped code to
automatically update.

|Build_Status| |Codecov_Status| |QuantifiedCode_Status|

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
   :alt: Travis CI results
.. |Codecov_Status| image:: http://codecov.io/github/rlee287/pyautoupdate/coverage.svg?branch=develop
   :target: http://codecov.io/github/rlee287/pyautoupdate?branch=develop
   :alt: Codecov Coverage measurements
.. |QuantifiedCode_Status| image:: https://www.quantifiedcode.com/api/v1/project/e70a21e3928a4cce87655a17fd853765/badge.svg
  :target: https://www.quantifiedcode.com/app/project/e70a21e3928a4cce87655a17fd853765
  :alt: QuantifiedCode issues
