|pyautoupdate_logo|

Pyautoupdate is an auto-update API for Python programs.

|Build_Status| |Codecov_Status| |QuantifiedCode_Status| |LandscapeIO_Status| |Gitter_Badge|

Advantages
----------

-  This module is written in pure python. **No C compiler is necessary for installation, simplifying installation for Windows.**
-  Python 2 and 3 are both supported
-  Pyautoupdate also works with pypy and pypy3

Installation
------------

.. code-block:: bash

    $ pip install pyautoupdate

Documentation
-------------
Documentation is available at http://rlee287.github.io/pyautoupdate.

Dependencies
------------
Core Dependencies
~~~~~~~~~~~~~~~~~
-  Python 2.6+ or Python 3.3+
-  ``requests`` for retrieving updated versions
-  ``setuptools`` for archive manipulation and version comparison

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~
-  ``pytest`` for running the tests
-  ``coverage`` to measure coverage

Optional Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-  ``pylint`` for local code style checks
-  ``sphinx`` for building documentation

License
-------

Pyautoupdate is licensed under the `LGPL 2.1 <https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html>`__.

.. |pyautoupdate_logo| image:: https://rlee287.github.io/pyautoupdate/_static/images/pyautoupdate_logo.svg
   :alt: Pyautoupdate Logo
.. |Build_Status| image:: https://travis-ci.org/rlee287/pyautoupdate.svg?branch=develop
   :target: https://travis-ci.org/rlee287/pyautoupdate
   :alt: Travis CI results
.. |Codecov_Status| image:: http://codecov.io/github/rlee287/pyautoupdate/coverage.svg?branch=develop
   :target: http://codecov.io/github/rlee287/pyautoupdate?branch=develop
   :alt: Codecov Coverage measurements
.. |QuantifiedCode_Status| image:: https://www.quantifiedcode.com/api/v1/project/e70a21e3928a4cce87655a17fd853765/badge.svg
  :target: https://www.quantifiedcode.com/app/project/e70a21e3928a4cce87655a17fd853765
  :alt: QuantifiedCode issues
.. |LandscapeIO_Status| image:: https://landscape.io/github/rlee287/pyautoupdate/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/rlee287/pyautoupdate/develop
   :alt: Code Health
.. |Gitter_Badge| image:: https://badges.gitter.im/pyautoupdate_chat/Lobby.svg
   :alt: Join the chat at https://gitter.im/pyautoupdate_chat/Lobby
   :target: https://gitter.im/pyautoupdate_chat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
