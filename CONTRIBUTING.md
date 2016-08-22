# Contributing
Thank you for taking your time to contribute to Pyautoupdate. When contributing, please follow the
[PSF Code of Conduct](https://www.python.org/psf/codeofconduct/).

Github's issues are used for bugtracking and feature requests. Please see the details below:

## Reporting Bugs
If you have run into issues with Pyautoupdate, please ensure that the problem is not with the application
that uses Pyautoupdate.

If you believe there is a genuine problem with Pyautoupdate that has not been already reported, please file a bug report including:
 - Python version
 - Operating System
 - Description of the problem
 - (If possible) instructions to reliably reproduce the problem

## Requesting Features
If you would like Pyautoupdate to have a new feature, please include the following:
 - A detailed description of the new feature
 - Why you think the feature would be useful to others

Please follow the instructions under the [Pull Requests](#pull-requests) header if you would like to implement this feature yourself.

## Pull Requests
The Pyautoupdate project uses [PullApprove](https://pullapprove.com/) to approve pull requests.
If you have an account on PullApprove, please approve your own pull request on PullApprove once it is ready for consideration.

All code must be compatible with both Python 2 and 3. To ensure this, all tests on [Travis CI](https://travis-ci.org/) are required to
pass (which will help to ensure Python 2 and 3 compatibility).

In addition, please make sure that test coverage, as measured on [CodeCov](https://codecov.io/),
does not decrease significantly and that no new significant issues are raised in QuantifiedCode.

Although exceptions may be made depending on circumstances, a pull request is less likely to be merged if code coverage
decreases significantly.
