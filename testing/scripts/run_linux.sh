#!/bin/sh
echo "Main test"
py.test -vl -r a --cov=pyautoupdate --cov-report=term-missing ./testing
echo "See stderr and stdout to rule out false positives"
py.test -vs
