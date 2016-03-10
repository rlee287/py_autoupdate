@echo off
echo "Main test"
py.test -vl -r a --cov=py_autoupdate --cov-report=term-missing .\testing
echo "See stderr and stdout to rule out false positives"
py.test -vs

