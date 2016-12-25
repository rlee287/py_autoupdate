Contributing
============

Thank you for taking your time to contribute to Pyautoupdate.
When contributing, please follow the
`PSF Code of Conduct <https://www.python.org/psf/codeofconduct/>`__,
a copy of which is included in ``PSFCodeOfConduct.rst``.

Github's issues are used for bugtracking and feature requests. Please
see the details below:

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
a copy of which has been included in
``DeveloperCertificateOrigin.txt``.

When creating a non-release Pull Request, please include the following:

-  An issue number that this Pull Request addresses **OR**
-  A short description of the problem the Pull Request addresses (please
   file an issue for large problems)
-  A description of the implementation of the bug fix/feature

All code must be compatible with both Python 2 and 3.
To ensure this, all tests on `Travis CI <https://travis-ci.org/>`__
must pass.
This will help to ensure Python 2 and 3 compatibility.

In addition, please make sure that test coverage, as measured on
`CodeCov <https://codecov.io/>`__, does not decrease significantly.

Although exceptions may be made depending on circumstances,
a pull request is less likely to be merged if code coverage decreases
significantly.
