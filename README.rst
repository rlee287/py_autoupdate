|pyautoupdate_logo|

Pyautoupdate is an an API library that provides autoupdate functionality
for Python programmers.

|Build_Status| |Codecov_Status| |LandscapeIO_Status| |Gitter_Badge|

Pyautoupdate allows end users to easily update their software when the
developers release a new version. Developers only need to upload the new
version of the application to their server when it is ready.
Pyautoupdate provides the functionality to check for updates and automatically
download and apply them.

Advantages
----------

-  Pyautoupdate secures its downloads through HTTPS.
-  Updates can be performed
   either upon prompting or automatically in the background.
-  Pyautoupdate is written in pure Python.
   *No C compiler is necessary for installation, simplifying installation for Windows.*
-  Python 2 and 3 are both supported
-  Pyautoupdate also works with pypy and pypy3

Installation
------------

.. code-block:: bash

    $ pip install pyautoupdate

Documentation
-------------
Documentation is available at https://rlee287.github.io/pyautoupdate.

Dependencies
------------
Core Dependencies
~~~~~~~~~~~~~~~~~
-  Python 2.7 or Python 3.4+
-  ``requests`` for retrieving updated versions
-  ``setuptools`` for archive manipulation and version comparison

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~
-  ``pytest`` for running the tests
-  ``coverage.py`` to measure coverage

Optional Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-  ``pylint`` for local code style checks
-  ``sphinx`` for building documentation

Contributing
------------
Please see `this page <https://rlee287.github.io/pyautoupdate/contributing.html>`__ for contributing guidelines.

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
.. |LandscapeIO_Status| image:: https://landscape.io/github/rlee287/pyautoupdate/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/rlee287/pyautoupdate/develop
   :alt: Code Health
.. |Gitter_Badge| image:: https://badges.gitter.im/pyautoupdate_chat/Lobby.svg
   :alt: Join the chat at https://gitter.im/pyautoupdate_chat/Lobby
   :target: https://gitter.im/pyautoupdate_chat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
