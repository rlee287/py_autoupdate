Contributing
============

Thank you for taking your time to contribute to Pyautoupdate.
When contributing, please follow the
`PSF Code of Conduct <https://www.python.org/psf/codeofconduct/>`__,
a copy of which is included in ``PSFCodeOfConduct.rst``.

Github's issues are used for tracking bugs and requesting features,
as explained below.

Environment Setup
-----------------

In addition to the core dependencies in :doc:`quickstart`, development also requires the following packages:

-  ``pytest`` for running the tests
-  ``coverage`` to measure coverage

The following packages are optional for development but recommended:

-  ``pylint`` for local code style checks
-  ``sphinx`` for building documentation

Pyautoupdate uses `pytest <https://docs.pytest.org/en/latest/>`__. To run the unit tests, please run

.. code-block:: none

   pytest .

in the root directory of the repo. The config file is ``pytest.ini``.

The wrapper scripts in ``test/scripts`` use
`coverage.py <https://coverage.readthedocs.io/>`__ to create
a coverage report after running tests.

Filing an Issue
---------------

Reporting Bugs
~~~~~~~~~~~~~~

If you have run into issues with Pyautoupdate,
please ensure that the problem is not with the application that uses
Pyautoupdate.

If you believe there is a genuine problem with Pyautoupdate
that has not been already reported, please file a bug report
including:

-  Python version
-  Operating System
-  Description of the problem

   -  Expected behavior
   -  Actual behavior

-  Instructions to reliably reproduce the problem

**Even if it is a glitch that occurs unreliably, please try to include
some instructions.**

Requesting Features
~~~~~~~~~~~~~~~~~~~

If you would like Pyautoupdate to have a new feature, please include the
following:

-  A detailed description of the new feature
-  Why you think the feature would be useful to others

Please follow the instructions under
`Pull Requests <#pull-requests>`__
if you would like to implement features or fix bugs.

Pull Requests
-------------

The Pyautoupdate project uses `PullApprove <https://pullapprove.com/>`__
to approve pull requests.

Authors of a Pull Request **must** approve it via PullApprove once it is
ready for consideration.
By approving a Pull Request, the author(s) signify that their
contribution satisfies the
`Developer Certificate of Origin <http://developercertificate.org/>`__,
a copy of which has been included in ``DeveloperCertificateOrigin.txt``.

All tests on `Travis CI <https://travis-ci.org/>`__ must pass.
Please explain any new xfailed tests in the Pull Request description.
In addition, all code must be simultaneously compatible with both
Python 2 and 3. The Travis CI build will help to ensure this.

Moreover, please make sure that new code is covered by new tests. Coverage for the project is tracked on `CodeCov <https://codecov.io/>`__.
When creating a Pull Request, please include the following:

-  An issue number that this Pull Request addresses **OR**
-  A short description of the problem the Pull Request addresses
-  A description of the implementation of the bug fix/feature

If you are fixing a new large issue in your Pull Request, please file an issue
concurrently with the Pull Request and link to the issue number in the Pull
Request.
